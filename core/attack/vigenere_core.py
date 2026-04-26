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
        
        # Tính điểm dựa trên Bigrams và Dictionary như cũ
        for bg in common_bigrams:
            score += text_lower.count(bg) * 5 
        
        words = text_lower.split()
        for w in words:
            if len(w) > 3 and w in self.dictionary:
                score += 100

        # --- LOGIC PHẠT ĐIỂM LẶP (PENALTY) ---
        n = len(key)
        repeat_count = 1
        # Tìm chu kỳ ngắn nhất
        for i in range(1, n // 2 + 1):
            if n % i == 0:
                substring = key[:i]
                if substring * (n // i) == key:
                    repeat_count = n // i
                    break # Tìm thấy chu kỳ nhỏ nhất thì dừng
        
        # Chia điểm cho số lần lặp. Ví dụ: 'ABCABC' bị chia 2, 'AAAAAA' bị chia 6
        return score / repeat_count

    def crack_vigenere(self, ciphertext, decrypt_func):
        clean_text = "".join(filter(str.isalpha, ciphertext.upper()))
        if not clean_text: return []

        # 1 & 2. Kasiski
        repeated = self.find_repeated_sequences(clean_text, seq_len=3)
        spacings = self.get_spacings(repeated)
        
        # 3. Tìm key lengths tiềm năng
        kasiski_lengths = self.find_candidate_key_lengths(spacings)
        if not kasiski_lengths:
            kasiski_lengths = range(2, 13)

        final_candidates = []
        for m in kasiski_lengths:
            avg_ic = sum(self.calculate_ic(clean_text[i::m]) for i in range(m)) / m
            final_candidates.append((m, avg_ic))
        
        final_candidates.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        # Duyệt TOÀN BỘ candidates để xem log đầy đủ
        for m, ic_score in final_candidates:
            guessed_key = self.infer_key_by_frequency(clean_text, m)
            decrypted = decrypt_func("Vigenère", ciphertext, guessed_key)
            
            # TRUYỀN THÊM guessed_key VÀO ĐÂY ĐỂ TÍNH PHẠT LẶP
            score = self.frequency_score(decrypted, guessed_key)
            
            results.append({
                "key": guessed_key,
                "key_len": m,
                "text": decrypted,
                "score": score,
                "ic": ic_score
            })
            
        # Sắp xếp lại: Lúc này các Key ngắn sẽ "vượt mặt" các Key lặp lại nhờ điểm Score cao hơn
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
        # Danh sách các chữ cái phổ biến nhất trong tiếng Anh theo thứ tự giảm dần
        # 'E' là phổ biến nhất, sau đó đến 'T', 'A', v.v.
        english_most_common = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
        
        n = len(column)
        if n == 0: return 0
        
        # 1. Đếm số lần xuất hiện của từng chữ trong cột và lấy top phổ biến nhất
        # Ví dụ: [('X', 10), ('Y', 8), ...]
        counts = Counter(column.upper())
        # Lấy các chữ cái xuất hiện trong cột, sắp xếp từ nhiều đến ít
        column_chars_sorted = [item[0] for item in counts.most_common()]
        
        best_shift = 0
        max_matches = -1
        
        # 2. Thử từng shift (0-25)
        for shift in range(26):
            matches = 0
            # Giải mã thử cột với shift này
            # Ví dụ: Nếu shift=1, 'B' thành 'A', 'C' thành 'B'
            
            # Chúng ta chỉ cần kiểm tra 6 chữ cái xuất hiện nhiều nhất trong cột sau khi dịch
            # xem chúng có nằm trong nhóm 6 chữ cái phổ biến nhất của tiếng Anh không.
            for char in column_chars_sorted[:6]: 
                # Dịch ngược chữ cái về nguyên bản
                char_idx = ord(char) - ord('A')
                decrypted_char = chr((char_idx - shift) % 26 + ord('A'))
                
                # Nếu chữ cái sau khi dịch nằm trong top 6 của tiếng Anh (E, T, A, O, I, N)
                # thì ta cộng điểm "trùng khớp"
                if decrypted_char in english_most_common[:6]:
                    matches += 1
            
            # Shift nào có nhiều chữ cái rơi vào nhóm phổ biến nhất thì chọn shift đó
            if matches > max_matches:
                max_matches = matches
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