import math
from collections import Counter
import os

class VigenereCracker:
    def __init__(self, dictionary_path=None):
        self.dictionary = self.load_dictionary(dictionary_path)

    def load_dictionary(self, path):
        path = os.path.join(os.path.dirname(__file__), "dictionary.txt")
        try:
            if path:
                with open(path, 'r', encoding='utf-8') as f:
                    return set(line.strip().lower() for line in f)
        except:
            return set()
        return set()

    def find_repeated_sequences(self, text, seq_len=3):
        """
        Bước 1: Tìm tất cả các chuỗi lặp lại có độ dài seq_len (mặc định là 3 ký tự).
        Trả về dictionary: { chuỗi: [danh_sách_vị_trí_xuất_hiện] }
        """
        sequences = {}
        for i in range(len(text) - seq_len + 1):
            seq = text[i:i + seq_len]
            if seq in sequences:
                sequences[seq].append(i)
            else:
                sequences[seq] = [i]
        
        # Chỉ giữ lại các chuỗi xuất hiện từ 2 lần trở lên
        return {s: pos for s, pos in sequences.items() if len(pos) > 1}

    def get_spacings(self, repeated_seqs):
        """
        Bước 2: Tính khoảng cách giữa các lần xuất hiện của cùng một chuỗi.
        """
        spacings = []
        for seq, positions in repeated_seqs.items():
            for i in range(len(positions) - 1):
                spacings.append(positions[i+1] - positions[i])
        return spacings

    def find_candidate_key_lengths(self, spacings, max_key_len=20):
        factors = []
        for space in spacings:
            for i in range(2, max_key_len + 1):
                if space % i == 0:
                    factors.append(i)
        
        # Lấy tất cả, không dùng .most_common(5)
        counts = Counter(factors)
        # Sắp xếp theo tần suất giảm dần nhưng lấy hết
        return [item[0] for item in counts.most_common()]

    def frequency_score(self, text, key):
        common_bigrams = ['th', 'he', 'in', 'er', 'an', 're', 'nd', 'at', 'on', 'nt']
        text_lower = text.lower()
        score = 0
        
        # 1. Tính điểm thô (Raw Score)
        for bg in common_bigrams:
            score += text_lower.count(bg) * 5 
        
        words = text_lower.split()
        for w in words:
            if len(w) > 3 and w in self.dictionary:
                score += 50 

        # 2. Xử lý giảm điểm dựa trên số lần lặp của Key
        repeat_count = self.get_repeat_count(key)
        
        # Công thức: Điểm cuối = Điểm gốc / Số lần lặp
        # Nếu key là 'ABC', repeat_count = 1 -> Giữ nguyên điểm
        # Nếu key là 'ABCABC', repeat_count = 2 -> Điểm bị chia đôi
        final_score = score / repeat_count
        
        return final_score

    def crack_vigenere(self, ciphertext, decrypt_func):
        clean_text = "".join(filter(str.isalpha, ciphertext.upper()))
        if not clean_text: return []

        # 1 & 2. Kasiski
        repeated = self.find_repeated_sequences(clean_text, seq_len=3)
        spacings = self.get_spacings(repeated)
        
        # 3. Kết hợp IC để chọn candidate_lengths tốt nhất
        kasiski_lengths = self.find_candidate_key_lengths(spacings)
        if not kasiski_lengths:
            kasiski_lengths = range(2, 13) # Thử từ 2 đến 12 nếu Kasiski tịt ngòi

        # Lọc lại m bằng IC: m chuẩn sẽ có IC các cột xấp xỉ 0.06x
        final_candidates = []
        for m in kasiski_lengths:
            avg_ic = sum(self.calculate_ic(clean_text[i::m]) for i in range(m)) / m
            final_candidates.append((m, avg_ic))
        
        # Sắp xếp theo IC giảm dần
        final_candidates.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        # Thử 5 độ dài khóa có IC cao nhất
        for m, ic_score in final_candidates:
            guessed_key = self.infer_key_by_frequency(clean_text, m)
            decrypted = decrypt_func("Vigenère", ciphertext, guessed_key)
            score = self.frequency_score(decrypted)
            
            results.append({
                "key": guessed_key,
                "key_len": m,
                "text": decrypted,
                "score": score,
                "ic": ic_score # Để hiển thị thêm thông tin nếu cần
            })
            
        return sorted(results, key=lambda x: x["score"], reverse=True)

    def infer_key_by_frequency(self, clean_text, m):
        """
        Tìm key bằng cách chia bản mã thành m cột và phá Caesar cho từng cột.
        """
        key = ""
        for i in range(m):
            column = clean_text[i::m]
            # Tìm shift tối ưu cho cột này (giả sử là thám mã Caesar cho cột)
            best_shift = self.find_best_caesar_shift(column)
            key += chr(best_shift + ord('A'))
        return key

    def find_best_caesar_shift(self, column):
        english_freqs = [
            0.0817, 0.0149, 0.0278, 0.0425, 0.1270, 0.0223, 0.0202, 0.0609, 0.0697, 
            0.0015, 0.0077, 0.0403, 0.0241, 0.0675, 0.0751, 0.0193, 0.0010, 0.0599, 
            0.0633, 0.0906, 0.0276, 0.0098, 0.0236, 0.0015, 0.0197, 0.0007
        ]
        
        best_shift = 0
        min_chi_sq = float('inf')
        n = len(column)
        
        # Đếm tần suất thực tế của các chữ cái trong cột một lần duy nhất
        # Điều này giúp tăng tốc vòng lặp 26 lần bên dưới
        column_counts = Counter([(ord(c) - ord('A')) for c in column])

        for shift in range(26):
            chi_sq = 0
            for i in range(26):
                # Vị trí thực tế sau khi dịch chuyển ngược (shift)
                actual_char_index = (i + shift) % 26
                observed = column_counts[actual_char_index]
                expected = n * english_freqs[i]
                
                if expected > 0:
                    chi_sq += ((observed - expected) ** 2) / expected
            
            if chi_sq < min_chi_sq:
                min_chi_sq = chi_sq
                best_shift = shift
        
        return best_shift
    
    def calculate_ic(self, text):
        """Tính chỉ số trùng khớp của một chuỗi văn bản"""
        n = len(text)
        if n <= 1: return 0
        freqs = Counter(text)
        numerator = sum(f * (f - 1) for f in freqs.values())
        denominator = n * (n - 1)
        return numerator / denominator

    def get_repeat_count(self, key):
        """
        'ABCABC' -> returns 2 (vì ABC lặp 2 lần)
        'AAAAAA' -> returns 6 (vì A lặp 6 lần)
        'HELLO'  -> returns 1 (không lặp)
        """
        n = len(key)
        for i in range(1, n // 2 + 1):
            if n % i == 0:
                substring = key[:i]
                if substring * (n // i) == key:
                    return n // i
        return 1