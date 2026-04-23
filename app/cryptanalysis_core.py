import collections

class CryptanalysisCore:
    @staticmethod
    def get_ic(text):
        """Tính Index of Coincidence"""
        clean_text = "".join(filter(str.isalpha, text.upper()))
        n = len(clean_text)
        if n <= 1: return 0
        
        freqs = collections.Counter(clean_text)
        sum_f = sum(f * (f - 1) for f in freqs.values())
        return sum_f / (n * (n - 1))

    @staticmethod
    def frequency_score(text):
        """Chấm điểm văn bản dựa trên tần suất chữ cái tiếng Anh (ETAOIN)"""
        # Tần suất phổ biến trong tiếng Anh
        english_freqs = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
        clean_text = "".join(filter(str.isalpha, text.upper()))
        if not clean_text: return 0
        
        # Đếm các chữ cái xuất hiện nhiều nhất trong văn bản
        text_counts = collections.Counter(clean_text).most_common(6)
        top_text_letters = "".join([item[0] for item in text_counts])
        
        # Tính điểm cộng nếu các chữ cái phổ biến xuất hiện trong top đầu
        score = 0
        for char in top_text_letters:
            if char in english_freqs[:6]:
                score += 1
        return score

    def crack_caesar(self, ciphertext, decrypt_func):
        results = []
        for shift in range(1, 26):
            decrypted = decrypt_func("Caesar", ciphertext, str(shift))
            score = self.frequency_score(decrypted)
            results.append({
                "key": shift,
                "text": decrypted,
                "score": score
            })
        # Sắp xếp kết quả có khả năng nhất lên đầu
        return sorted(results, key=lambda x: x["score"], reverse=True)

    def crack_vigenere(self, ciphertext):
        # Placeholder cho logic Kasiski/Friedman
        return "Tính năng thám mã Vigenère đang được phát triển..."