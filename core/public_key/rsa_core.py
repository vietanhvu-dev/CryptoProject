from utils.math_helpers import is_prime, gcd, mod_inverse

def rsa_generate_keys(p, q, e):
    """
    BƯỚC 1: Sinh khóa RSA + log dạng list dict cho UI
    """
    logs = []
    logs.append({"content": "--- BƯỚC 1: KHỞI TẠO THÔNG SỐ RSA ---"})

    # --- VALIDATION ---
    if not isinstance(p, int) or not isinstance(q, int) or not isinstance(e, int):
        return None, [{"content": "Lỗi: p, q, e phải là số nguyên!"}]

    if p <= 1 or q <= 1:
        return None, [{"content": "Lỗi: p và q phải > 1!"}]

    if not is_prime(p):
        return None, [{"content": f"Lỗi: p = {p} không phải số nguyên tố!"}]

    if not is_prime(q):
        return None, [{"content": f"Lỗi: q = {q} không phải số nguyên tố!"}]

    if p == q:
        return None, [{"content": "Lỗi: p và q không được trùng nhau!"}]

    logs.append({"content": f"✔ p = {p} là số nguyên tố"})
    logs.append({"content": f"✔ q = {q} là số nguyên tố"})

    # --- TÍNH TOÁN ---
    n = p * q
    phi = (p - 1) * (q - 1)

    logs.append({"content": f"1. n = p * q = {n}"})
    logs.append({"content": f"2. Phi(n) = (p-1)*(q-1) = {phi}"})
    logs.append({"content": f"3. e = {e}"})

    # --- CHECK e ---
    if e <= 1 or e >= phi:
        return None, [{"content": f"Lỗi: e phải nằm trong (1, Phi(n))!"}]

    if gcd(e, phi) != 1:
        return None, [{"content": f"Lỗi: e={e} và Phi(n)={phi} không nguyên tố cùng nhau!"}]

    logs.append({"content": "✔ e hợp lệ với Phi(n)"})

    # --- TÍNH d ---
    try:
        d = mod_inverse(e, phi)

        logs.append({"content": f"4. d = e^(-1) mod Phi(n) = {d}"})
        logs.append({"content": f"👉 PUBLIC KEY: (n={n}, e={e})"})
        logs.append({"content": f"👉 PRIVATE KEY: (n={n}, d={d})"})

        return {
            "n": n,
            "e": e,
            "d": d,
            "phi": phi,
            "logs": logs   # 👈 QUAN TRỌNG
        }, None

    except ValueError:
        return None, [{"content": "Lỗi: Không tìm được nghịch đảo modulo cho e."}]
    
def rsa_process_segmented(text, key_n, key_exponent, mode='encrypt'):
    """
    BƯỚC 2: Xử lý dữ liệu và trả về Log chia nhỏ theo mốc ký tự.
    """
    segmented_logs = []
    current_batch = []
    result_data = []
    milestones = [50, 100, 200] # Giống logic Vigenere
    
    process_title = "MÃ HÓA" if mode == 'encrypt' else "GIẢI MÃ"
    formula = "C = M^e mod n" if mode == 'encrypt' else "M = C^d mod n"
    
    # Chuẩn bị dữ liệu đầu vào
    items = text.strip().split() if mode == 'decrypt' else list(text)
    
    for i, item in enumerate(items):
        try:
            if mode == 'encrypt':
                m = ord(item)
                res_val = pow(m, key_exponent, key_n)
                result_data.append(str(res_val))
                log_entry = f"Ký tự {i+1}: '{item}' (ASCII: {m}) -> {m}^{key_exponent} mod {key_n} = {res_val}"
            else:
                c = int(item)
                res_val = pow(c, key_exponent, key_n)
                res_char = chr(res_val)
                result_data.append(res_char)
                log_entry = f"Khối {i+1}: {c} -> {c}^{key_exponent} mod {key_n} = {res_val} (Ký tự: '{res_char}')"
            
            current_batch.append(log_entry)
        except Exception as e:
            current_batch.append(f"Dòng {i+1}: Lỗi xử lý ({str(e)})")

        # Chia nhỏ log theo mốc
        curr_count = i + 1
        if curr_count in milestones:
            segmented_logs.append({
                "title": f"⚙️ Chi tiết {process_title} ({curr_count} ký tự đầu)",
                "content": f"Công thức dùng: {formula}\n" + "-"*40 + "\n" + "\n".join(current_batch)
            })

    # Log đoạn cuối
    if not segmented_logs or len(items) > (milestones[-1] if milestones else 0):
        segmented_logs.append({
            "title": f"⚙️ Chi tiết {process_title} (Đoạn cuối)",
            "content": f"Tổng số thực hiện: {len(items)}\n" + "-"*40 + "\n" + "\n".join(current_batch)
        })

    final_result = " ".join(result_data) if mode == 'encrypt' else "".join(result_data)
    return final_result, segmented_logs