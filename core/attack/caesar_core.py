import collections 
import time
import os

class CaesarCracker:
    def __init__(self):
        self.ENGLISH_FREQ = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
        # Tải từ điển ngay khi khởi tạo
        self.dictionary = self._load_dictionary()

    def _load_dictionary(self):
        words = set()
        # Tìm file common_words.txt cùng thư mục với file này
        path = os.path.join(os.path.dirname(__file__), "common_words.txt")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    w = line.strip().upper()
                    if w: words.add(w)
        return words

    def _calculate_score(self, text):
        # 1. Tiền xử lý: Giữ lại chữ cái và khoảng trắng để tách từ
        text_upper = text.upper()
        clean_text_only = "".join(filter(str.isalpha, text_upper))
        
        if not clean_text_only: 
            return 0
        
        # Khởi tạo score
        score = 0

        # 2. Kiểm tra nguyên âm (Vowel Check)
        vowels = "AEIOU"
        vowel_count = sum(1 for char in text_upper if char in vowels)
        if len(clean_text_only) > 5 and vowel_count == 0:
            score -= 10

        # 3. Tần suất chữ cái đơn (Frequency Analysis)
        counts = collections.Counter(clean_text_only)
        top_6 = [item[0] for item in counts.most_common(6)]
        score += sum(1 for char in top_6 if char in self.ENGLISH_FREQ[:6])
        
        # 4. Thưởng điểm cho các từ cực phổ biến (Hard-coded Bonus)
        common_fixed = [" THE ", " AND ", " THIS ", " THAT ", " HAVE ", " YOU "]
        for word in common_fixed:
            if word in f" {text_upper} ": 
                score += 5

        # 5. TRA CỨU TỪ ĐIỂN 3 TỪ ĐẦU (Dictionary Lookup)
        # Tách văn bản thành danh sách các từ
        words_list = text_upper.split()
        first_3_words = words_list[:3]
        
        for word in first_3_words:
            # Loại bỏ các ký tự đặc biệt dính vào từ (như dấu phẩy, chấm)
            clean_word = "".join(filter(str.isalpha, word))
            if clean_word in self.dictionary:
                score += 15 # Thưởng rất nặng nếu khớp từ điển

        return score

    def crack_range(self, ciphertext, start_key, end_key, callback):
        try:
            for shift in range(start_key, end_key):
                decrypted = ""
                for char in ciphertext:
                    if char.isalpha():
                        start = ord('A') if char.isupper() else ord('a')
                        decrypted += chr((ord(char) - start - shift) % 26 + start)
                    else:
                        decrypted += char
                
                score = self._calculate_score(decrypted)
                
                # Chuẩn bị dữ liệu gửi về UI
                result_data = {
                    "key": shift,
                    "text": decrypted,
                    "status": "Khả thi" if score >= 3 else "Nhiễu",
                    "eval": "Khả thi" if score >= 3 else "Nhiễu",
                    "score": score
                }
                
                callback(result_data)
                time.sleep(0.05) # Delay một chút để thấy hiệu ứng song song
        except Exception as e:
            print(f"LỖI TRONG THREAD: {e}") # In ra terminal để debug