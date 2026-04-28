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
        if text is None: return -999999
        
        text_lower = text.lower()
        score = 0
        
        # 1. Thưởng cực nặng cho các từ cực ngắn nhưng phổ biến (if, he, had, to, in, it)
        common_short_words = {'if', 'he', 'had', 'to', 'in', 'it', 'is', 'was', 'the', 'that'}
        words = text_lower.split()
        
        for w in words:
            clean_word = "".join(filter(str.isalpha, w))
            if clean_word in common_short_words:
                score += 150 # Thưởng rất cao để kéo đúng Key
            elif len(clean_word) > 3 and clean_word in self.dictionary:
                score += 100

        # 2. Bigrams
        common_bigrams = ['th', 'he', 'in', 'er', 'an', 're', 'nd', 'at', 'on', 'nt']
        for bg in common_bigrams:
            score += text_lower.count(bg) * 10 

        # 3. Logic phạt lặp cũ của bạn
        n = len(key)
        repeat_count = 1
        for i in range(1, n // 2 + 1):
            if n % i == 0 and key[:i] * (n // i) == key:
                repeat_count = n // i
                break
        
        return score / repeat_count

    def crack_vigenere(self, ciphertext, decrypt_func, log_callback=None):
        def emit(msg):
            if log_callback: 
                # Đảm bảo mỗi dòng log kết thúc bằng một dấu xuống dòng thực thụ
                log_callback(str(msg) + "\n")

        emit("🔍 BẮT ĐẦU QUÁ TRÌNH THÁM MÃ ..")
        
        clean_text = "".join(filter(str.isalpha, ciphertext.upper()))
        if not clean_text:
            emit("❌ Lỗi: Bản mã không chứa ký tự chữ cái nào.")
            return []
            
        emit(f"📝 Văn bản làm sạch: {clean_text[:50]}... ({len(clean_text)} ký tự) \n")


        # 1 & 2. Kasiski Examination
        emit("👉 BƯỚC 1: TÌM CHUỖI LẶP VÀ KHOẢNG CÁCH")

        repeated = self.find_repeated_sequences(clean_text, seq_len=3)
        
        if not repeated:
            emit("   - Không tìm thấy chuỗi lặp. Thử m từ 2 đến 12.")

        else:
            emit(f"   - Tìm thấy {len(repeated)} nhóm lặp.")
    
            for seq, pos in list(repeated.items())[:5]: # Chỉ in 5 mẫu đầu cho gọn
                emit(f"     + Chuỗi '{seq}': Vị trí {pos}")
  
        
        spacings = self.get_spacings(repeated)
        emit(f"   - Khoảng cách đo được: {spacings[:10]}...")
        emit("\n")

        # 3. Tìm key lengths tiềm năng
        emit("👉 BƯỚC 2: PHÂN TÍCH ĐỘ DÀI KHÓA (m)")
        kasiski_lengths = self.find_candidate_key_lengths(spacings)
        if not kasiski_lengths:
            kasiski_lengths = list(range(2, 13))
            emit("   - Kasiski không cho kết quả. Thử mặc định m = [2..12]")
        else:
            emit(f"   - m tiềm năng từ Kasiski: {kasiski_lengths}")

        # Tính toán IC để xếp hạng các m
        final_candidates = []
        emit("   - Kiểm định chỉ số trùng khớp (IC) từng m:")
        for m in kasiski_lengths:
            avg_ic = sum(self.calculate_ic(clean_text[i::m]) for i in range(m)) / m
            emit(f"     + m={m:02d} | IC trung bình: {avg_ic:.4f}")
            final_candidates.append((m, avg_ic))
        
        # Sắp xếp m theo IC giảm dần
        final_candidates.sort(key=lambda x: x[1], reverse=True)
        emit("\n")

        # 4. Giải mã thử và Chấm điểm
        emit("👉 BƯỚC 3: GIẢI MÃ THỬ VÀ CHẤM ĐIỂM (PHẠT LẶP) \n")        
        results = []
        for m, ic_score in final_candidates:
            # Tìm key dựa trên tần suất (Caesar shift từng cột)
            guessed_key = self.infer_key_by_frequency(clean_text, m)
            
            try:
                decrypted = decrypt_func("Vigenère", ciphertext, guessed_key)
                
                # Tính điểm Score (Hàm này đã có logic phạt repeat_count)
                score = self.frequency_score(decrypted, guessed_key)
                
                # Logic lấy repeat_count để log (phục vụ mô phỏng giải tay)
                r_count = 1
                for i in range(1, len(guessed_key) // 2 + 1):
                    if len(guessed_key) % i == 0 and guessed_key[:i] * (len(guessed_key) // i) == guessed_key:
                        r_count = len(guessed_key) // i
                        break
                
                log_entry = f"🔑 THỬ KEY: '{guessed_key}' (m={m})"
                if r_count > 1:
                    log_entry += f" -> [PHẠT LẶP x{r_count}]"
                log_entry += f" | Score: {score:.1f}"
                emit(log_entry)
                
                results.append({
                    "key": guessed_key,
                    "key_len": m,
                    "text": decrypted,
                    "score": score,
                    "ic": ic_score
                })
            except Exception as e:
                emit(f"   ⚠️ Lỗi khi thử key '{guessed_key}': {e}\n")
            
   
        emit("🏁 HOÀN TẤT: Đã tìm ra ứng viên tốt nhất.")
        
        # Sắp xếp lại kết quả cuối cùng theo Score
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