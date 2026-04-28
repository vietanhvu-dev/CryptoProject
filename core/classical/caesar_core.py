def caesar_cipher_segmented(text, shift, mode='encrypt'):
    result = ""
    direction = 1 if mode == 'encrypt' else -1
    final_shift = (shift * direction) % 26
    
    milestones = [50, 100, 200, 500, 1000]
    segmented_logs = []
    current_batch = []
    
    for i, char in enumerate(text):
        curr_idx = i + 1
        # Logic xử lý ký tự
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            res_char = chr((ord(char) - start + final_shift) % 26 + start)
            # Log khi xử lý chữ cái
            current_batch.append(f"Ký tự {curr_idx:03d}: '{char}' -> '{res_char}'")
        else:
            res_char = char
            # Log khi gặp ký tự đặc biệt
            current_batch.append(f"Ký tự {curr_idx:03d}: '{char}' -> (Bỏ qua - Không phải chữ cái)")
        
        result += res_char
        
        # Nếu chạm mốc milestone, đóng gói batch hiện tại vào log
        if curr_idx in milestones:
            chunk_content = f"--- BÁO CÁO CHI TIẾT MỐC {curr_idx} KÝ TỰ ---\n" + "\n".join(current_batch)
            segmented_logs.append({
                "title": f"🔍 Chi tiết {curr_idx} ký tự đầu tiên",
                "content": chunk_content
            })

    # Gói đoạn còn lại cuối cùng
    if not segmented_logs or len(text) not in milestones:
        final_content = f"--- BÁO CÁO HOÀN TẤT: TỔNG {len(text)} KÝ TỰ ---\n" + "\n".join(current_batch)
        segmented_logs.append({
            "title": f"🔍 Tổng {len(text)} ký tự",
            "content": final_content
        })

    return result, segmented_logs