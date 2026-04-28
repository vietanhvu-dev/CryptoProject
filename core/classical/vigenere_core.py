# core/classical/vigenere_core.py

def vigenere_cipher_segmented(text, key, mode='encrypt'):
    """
    Xử lý Vigenère và trả về (Kết quả, Danh sách các đoạn log).
    """
    if not key:
        return text, [{"title": "Lỗi", "content": "Key không được để trống!"}]

    result = ""
    key = key.upper()
    key_length = len(key)
    key_index = 0
    
    milestones = [50, 100, 200, 500, 1000]
    segmented_logs = []
    current_batch = []
    
    # Hướng tính toán
    direction = 1 if mode == 'encrypt' else -1

    for i, char in enumerate(text):
        if char.isalpha():
            # 1. Xác định thông số chữ cái gốc
            is_upper = char.isupper()
            orig_idx = ord(char.upper()) - ord('A')
            
            # 2. Xác định ký tự khóa tương ứng
            current_key_char = key[key_index % key_length]
            key_shift = ord(current_key_char) - ord('A')
            
            # 3. Tính toán vị trí mới: (M + K) mod 26 hoặc (C - K) mod 26
            new_idx = (orig_idx + (direction * key_shift)) % 26
            new_char = chr(new_idx + ord('A'))
            
            # Giữ nguyên định dạng hoa/thường
            res_char = new_char if is_upper else new_char.lower()
            
            # Log chi tiết: Chữ gốc + Chữ khóa -> Chữ mới
            current_batch.append(
                f"Ký tự {i+1}: '{char}' | Key: '{current_key_char}' (+{key_shift}) -> '{res_char}'"
            )
            
            key_index += 1 # Chỉ tăng index key khi gặp chữ cái
        else:
            res_char = char
            current_batch.append(f"Ký tự {i+1}: '{char}' (Ký tự đặc biệt - Bỏ qua key)")
        
        result += res_char
        curr_idx = i + 1

        # Đóng gói khi chạm mốc milestone
        if curr_idx in milestones:
            header = f"--- VIGENÈRE REPORT: MỐC {curr_idx} KÝ TỰ ---\n"
            header += f"KEY ĐANG DÙNG: {key}\n" + "-"*40 + "\n"
            segmented_logs.append({
                "title": f"🔍 Chi tiết {curr_idx} ký tự đầu tiên",
                "content": header + "\n".join(current_batch)
            })

    # Gói đoạn cuối cùng
    processed_counts = [m for m in milestones if m <= len(text)]
    if not segmented_logs or len(text) > (processed_counts[-1] if processed_counts else 0):
        header = f"--- VIGENÈRE FINAL REPORT: TỔNG {len(text)} KÝ TỰ ---\n"
        segmented_logs.append({
            "title": f"🔍 Đoạn cuối (Tổng {len(text)} ký tự)",
            "content": header + "\n".join(current_batch)
        })

    return result, segmented_logs