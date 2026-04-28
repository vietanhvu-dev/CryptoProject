# core/public_key/rsa_core.py
from utils.math_helpers import is_prime, gcd, mod_inverse
def rsa_cipher_segmented(text, p, q, e, mode='encrypt'):
    """
    Xử lý RSA và trả về (Kết quả, Danh sách log phân đoạn).
    """
    segmented_logs = []
    step1_logs = []
    
    # --- BƯỚC 1: KHỞI TẠO HỆ THỐNG (Luôn ghi vào log đầu tiên) ---
    step1_logs.append("--- BƯỚC 1: KHỞI TẠO THÔNG SỐ RSA ---")
    n = p * q
    phi = (p - 1) * (q - 1)
    
    step1_logs.append(f"1. Số nguyên tố: p = {p}, q = {q}")
    step1_logs.append(f"2. Tính n = p * q = {n}")
    step1_logs.append(f"3. Tính Phi(n) = (p-1)*(q-1) = {phi}")
    step1_logs.append(f"4. Số công khai e: {e}")
    
    # Kiểm tra e hợp lệ
    if gcd(e, phi) != 1:
        return None, [{"title": "Lỗi", "content": f"e={e} và Phi(n)={phi} không nguyên tố cùng nhau!"}]
    
    # Tính d (Private Key)
    d = mod_inverse(e, phi)
    step1_logs.append(f"5. Tính d (Số nghịch đảo modulo e mod Phi(n)): {d}")
    step1_logs.append(f"\n=> PUBLIC KEY: (n={n}, e={e})")
    step1_logs.append(f"=> PRIVATE KEY: (n={n}, d={d})")
    
    segmented_logs.append({
        "title": "🔐 Bước 1: Khởi tạo và Tính toán Khóa",
        "content": "\n".join(step1_logs)
    })

    # --- BƯỚC 2: XỬ LÝ DỮ LIỆU ---
    process_logs = []
    process_logs.append(f"--- BƯỚC 2: {'MÃ HÓA' if mode == 'encrypt' else 'GIẢI MÃ'} DỮ LIỆU ---")
    
    result_data = []
    
    if mode == 'encrypt':
        # Mã hóa: C = M^e mod n
        process_logs.append("Công thức: Cipher = (Plaintext_ASCII)^e mod n\n")
        for i, char in enumerate(text):
            m = ord(char)
            c = pow(m, e, n)
            result_data.append(str(c))
            if i < 20: # Chỉ log 20 ký tự đầu để tránh quá tải
                process_logs.append(f"{i+1:03d}: '{char}' (ASCII: {m}) -> {m}^{e} mod {n} = {c}")
        
        final_result = " ".join(result_data) # Kết quả RSA thường là dãy số cách nhau
        
    else:
        # Giải mã: M = C^d mod n
        process_logs.append("Công thức: Plaintext = (Cipher_Value)^d mod n\n")
        # Giả định đầu vào giải mã là dãy số cách nhau bởi dấu cách
        try:
            cipher_values = text.strip().split()
            for i, val in enumerate(cipher_values):
                c = int(val)
                m = pow(c, d, n)
                res_char = chr(m)
                result_data.append(res_char)
                if i < 20:
                    process_logs.append(f"{i+1:03d}: {c} -> {c}^{d} mod {n} = {m} (Char: '{res_char}')")
            
            final_result = "".join(result_data)
        except Exception as err:
            return None, [{"title": "Lỗi", "content": f"Dữ liệu giải mã không hợp lệ: {err}"}]

    if len(text) > 20:
        process_logs.append(f"\n... và {len(text)-20} ký tự khác.")

    segmented_logs.append({
        "title": f"⚙️ Bước 2: Quá trình xử lý {mode.upper()}",
        "content": "\n".join(process_logs)
    })

    return final_result, segmented_logs