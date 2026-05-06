import streamlit as st
import os
from core.classical.caesar_core import caesar_cipher_segmented

class CryptoView:
    def __init__(self, master, algo_name, master_app, **kwargs):
        self.master = master
        self.algo_name = algo_name
        self.master_app = master_app

    def render(self): 
            # --- KHỞI TẠO SESSION STATE ---
        if 'logs' not in st.session_state:
            st.session_state.logs = []
        if 'segmented_logs' not in st.session_state:
            st.session_state.segmented_logs = []
        if 'current_result' not in st.session_state:
            st.session_state.current_result = ""
        st.markdown(f"<h1 style='color: #1f538d;'>Hệ mật: {self.algo_name}</h1>", unsafe_allow_html=True)
        st.markdown("""
            <style>
                /* 1. Phóng to và làm đậm tiêu đề Tab */
                button[data-baseweb="tab"] {
                    height: 60px !important; /* Tăng chiều cao Tab */
                }
                
                button[data-baseweb="tab"] div {
                    font-size: 22px !important; /* Chỉnh cỡ chữ to hẳn lên */
                    font-weight: 800 !important; /* Độ đậm cực đại */
                    font-family: 'Source Sans Pro', sans-serif !important;
                }

                /* 2. Hiệu ứng khi Hover (di chuột qua) */
                button[data-baseweb="tab"]:hover {
                    color: #1f538d !important;
                    background-color: rgba(31, 83, 141, 0.05) !important;
                    transition: 0.3s;
                }

                /* 3. Style riêng cho Tab đang được chọn (Active) */
                button[data-baseweb="tab"][aria-selected="true"] {
                    border-bottom: 4px solid #1f538d !important; /* Đường kẻ dưới chân đậm hơn */
                    background-color: rgba(31, 83, 141, 0.1) !important;
                }
            </style>
        """, unsafe_allow_html=True)
        # Chia cột chính (Trái: Xử lý | Phải: Log)
        left_col, right_col = st.columns([3, 2])

        with left_col:
            # 1. KHU VỰC INPUT
            st.write("### 📥 Đầu vào")
            uploaded_file = st.file_uploader("📁 Tải File (.txt)", type=['txt'], key=f"upload_{self.algo_name}")
            
            input_data = ""
            if uploaded_file:
                input_data = uploaded_file.read().decode("utf-8")
            
            input_text = st.text_area("📋 Nhập văn bản cần xử lý:", value=input_data, height=150)
            # 2. THAM SỐ ĐỘNG
            params = {}

            # Nếu KHÔNG PHẢI RSA thì hiện tiêu đề và info kiểu cũ
            if self.algo_name != "RSA":
                st.write("### ⚙️ Tham số")
            
            with st.container():
                if self.algo_name != "RSA":
                    st.info("Nhập các khóa bảo mật bên dưới")
                if self.algo_name == "Caesar":
                    params['shift_key'] = st.text_input("**🔑 Độ dịch (Shift):**", placeholder="Ví dụ: 3")
                    
                    # Chuẩn bị dữ liệu
                    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
                    shift = 0
                    if params['shift_key']:
                        try:
                            shift = int(params['shift_key']) % 26
                        except ValueError:
                            shift = 0
                    shifted_alphabet = alphabet[shift:] + alphabet[:shift]

                    # Tạo các hàng cho bảng (mỗi chữ cái vào một ô <td>)
                    row_orig = "".join([f"<td style='padding: 8px; border: 1px solid #ddd; color: #1f538d;'>{c}</td>" for c in alphabet])
                    row_shift = "".join([f"<td style='padding: 8px; border: 1px solid #ddd; color: #e63946;'>{c}</td>" for c in shifted_alphabet])

                    st.write("")
                    st.markdown("**🔄 BẢNG ĐỐI CHIẾU CHUYỂN DỊCH**")

                    # Vẽ bảng bằng HTML
                    st.markdown(f"""
                        <div style="overflow-x: auto;">
                            <table style="
                                width: 100%; 
                                border-collapse: collapse; 
                                text-align: center; 
                                font-family: 'Courier New', monospace; 
                                font-size: 20px; 
                                font-weight: bold;
                                background-color: white;
                            ">
                                <tr style="background-color: #f1f3f6;">{row_orig}</tr>
                                <tr>{row_shift}</tr>
                            </table>
                        </div>
                    """, unsafe_allow_html=True)
                elif self.algo_name == "Vigenère":
                    params['vigenere_key'] = st.text_input("📍 Từ khóa (Key):", placeholder="Ví dụ: VIETANH", type="password")
                elif self.algo_name == "RSA":
    # Chia giao diện thành 2 Tab chính
                    tab_setup, tab_process = st.tabs(["🔑 Thiết lập khóa từ p, q, e", "⚙️ Thực thi RSA"])

                    with tab_setup:
                        c1, c2 = st.columns(2)
                        with c1:
                            params['p_key'] = st.text_input("📍 Số nguyên tố p:", type="password", key="rsa_p_input")
                            params['q_key'] = st.text_input("📍 Số nguyên tố q:", type="password", key="rsa_q_input")
                        with c2:
                            params['e_key'] = st.text_input("📍 Số e (Public):", value="65537", type="password", key="rsa_e_input")
                            
                            # --- Gợi ý số nguyên tố (Logic giữ nguyên của bạn) ---
                            import os
                            import random

                            @st.cache_data
                            def load_primes():
                                file_path = os.path.join("app", "primes.txt")
                                if os.path.exists(file_path):
                                    with open(file_path, "r") as f:
                                        return [line.strip() for line in f if line.strip() and int(line.strip()) > 100]
                                return []

                            all_primes = load_primes()

                            if all_primes:
                                if 'rsa_suggestions' not in st.session_state or not st.session_state.rsa_suggestions:
                                    st.session_state.rsa_suggestions = random.sample(all_primes, min(5, len(all_primes)))

                                col_text, col_btn = st.columns([0.85, 0.15])

                                with col_text:
                                    primes_str = "  |  ".join(st.session_state.rsa_suggestions)
                                    st.text_input(
                                        "📍 Gợi ý (p, q):",
                                        value=primes_str,
                                    )

                                with col_btn:
                                    if st.button("🔄", type="tertiary", help="Gợi ý mới"):
                                        new_sample = random.sample(all_primes, min(5, len(all_primes)))
                                        while new_sample == st.session_state.rsa_suggestions and len(all_primes) > 5:
                                            new_sample = random.sample(all_primes, 5)

                                        st.session_state.rsa_suggestions = new_sample

                        # Nút để kích hoạt việc sinh khóa
                        if st.button("🚀 Sinh Khóa ", use_container_width=True):
                            if params['p_key'] and params['q_key']:
                                try:
                                    p = int(params['p_key'])
                                    q = int(params['q_key'])
                                    e = int(params['e_key'])
                                    
                                    from core.public_key.rsa_core import rsa_generate_keys
                                    key_data, error_logs = rsa_generate_keys(p, q, e)
                                    
                                    if key_data:
                                        # 1. Lưu bộ khóa để dùng cho Tab 2
                                        st.session_state['rsa_key_data'] = key_data
                                        
                                        # 2. CHUẨN BỊ NỘI DUNG CHO EXPANDER RIÊNG
                                        rsa_logs_raw = key_data.get('logs', [])
                                        # Gộp các dòng log thành một chuỗi duy nhất, có thể thêm màu sắc bằng ANSI hoặc ký tự
                                        full_log_content = ""
                                        for log in rsa_logs_raw:
                                            content = log.get('content', '') if isinstance(log, dict) else str(log)
                                            full_log_content += f"{content}\n"

                                        # 3. ĐẨY VÀO SEGMENTED_LOGS (Nó sẽ tự tạo một Expander mới bên phải)
                                        new_segment = {
                                            "title": f"🔑 RSA KEY GENERATION",
                                            "content": full_log_content.strip()
                                        }
                                        # Thêm vào đầu danh sách để Expander này hiện lên trên cùng bên cột phải
                                        st.session_state.segmented_logs.insert(0, new_segment)
                                        
                                        # 4. Xóa session cũ của widget để cập nhật giá trị mới
                                        for k in ["rsa_n_exec_field", "rsa_e_exec_field", "rsa_d_exec_field"]:
                                            if k in st.session_state:
                                                del st.session_state[k]
                                        
                                        st.success("✅ Đã tạo khóa! Chi tiết hiện ở Processor Log.")
                                        st.rerun() 
                                    else:
                                        # Nếu lỗi, cũng tạo một Expander lỗi riêng bên phải
                                        error_content = "\n".join([log.get('content', '') for log in error_logs])
                                        st.session_state.segmented_logs.insert(0, {
                                            "title": "❌ RSA KEY GEN ERROR",
                                            "content": error_content
                                        })
                                        st.rerun()

                                except ValueError:
                                    st.error("❌ Vui lòng nhập số hợp lệ.")

                        # --- Phần hiển thị Log (Giữ nguyên logic của bạn nhưng thêm bọc Expander cho gọn) ---
                        if st.session_state.get('rsa_key_logs'):
                            with st.expander("📝 Chi tiết quá trình sinh khóa", expanded=False):
                                for log in st.session_state['rsa_key_logs']:
                                    content = log.get('content', '') if isinstance(log, dict) else str(log)
                                    # Trang trí một chút cho dễ nhìn
                                    if "✔" in content:
                                        st.markdown(f":green[{content}]")
                                    elif "Lỗi" in content:
                                        st.markdown(f":red[{content}]")
                                    else:
                                        st.text(content)

                    with tab_process:
                        st.markdown("<p style='font-size: 18px; font-weight: bold; margin-bottom: 5px;'>⚙️ Cấu hình tham số thực thi</p>", unsafe_allow_html=True)
                        # Lấy dữ liệu nguồn từ Tab 1
                        k_source = st.session_state.get('rsa_key_data', {})
                        
                        # NÚT BẤM CẬP NHẬT
                        if k_source:
                            if st.button("📥 Lấy cặp khóa từ Tab bên", use_container_width=True):
                                # Ép giá trị của Widget bằng cách ghi đè trực tiếp vào Session State của Key đó
                                st.session_state["rsa_n_exec_field"] = str(k_source.get('n', ''))
                                st.session_state["rsa_e_exec_field"] = str(k_source.get('e', ''))
                                st.session_state["rsa_d_exec_field"] = str(k_source.get('d', ''))
                                st.rerun()

                        col_n, col_e, col_d = st.columns(3)
                        
                        with col_n:
                            params['n_exec'] = st.text_input(
                                "📍 Modulus (n):", 
                                key="rsa_n_exec_field", # Key này phải trùng với key bị ghi đè ở trên
                                type="password"
                            )
                            
                        with col_e:
                            params['e_exec'] = st.text_input(
                                "📢 Public Exponent (e):", 
                                key="rsa_e_exec_field",
                                type="password"
                            )

                        with col_d:
                            params['d_exec'] = st.text_input(
                                "🔐 Private Exponent (d):", 
                                key="rsa_d_exec_field",
                                type="password"
                            )
    # 3. NÚT BẤM THỰC THI
            col_btn1, col_btn2 = st.columns(2)
            action_clicked = None

            if col_btn1.button("🔓 MÃ HÓA", use_container_width=True, type="primary"):
                action_clicked = "encrypt"
            if col_btn2.button("🔑 GIẢI MÃ", use_container_width=True):
                action_clicked = "decrypt"

            if action_clicked:
                if not input_text.strip():
                    st.error("Vui lòng nhập dữ liệu đầu vào!")
                else:
                    st.session_state.logs.append(f"> Engine: {self.algo_name} | Action: {action_clicked.upper()}")
                    with st.spinner("Đang xử lý..."):
                        if action_clicked == "encrypt":
                            result = self.handle_encrypt(self.algo_name, input_text, params)
                        else:
                            result = self.handle_decrypt(self.algo_name, input_text, params)
                    
                    st.session_state.current_result = result
                    st.session_state.logs.append("> Xử lý hoàn tất.")

            # 4. KHU VỰC OUTPUT
           
            # Dùng col để đưa nút Tải xuống lên ngang hàng với chữ "Kết quả"
            out_header_col, btn_download_col = st.columns([2, 1])
            
            with out_header_col:
                st.write("### 📤 Kết quả")
            
            current_out = st.session_state.get('current_result', '')
            
            with btn_download_col:
                # Đẩy nút xuống một chút để bằng với tiêu đề h3
                st.markdown("<p style='margin-bottom: 25px;'></p>", unsafe_allow_html=True)
                if current_out:
                    st.download_button(
                        label="📄 Tải xuống .txt",
                        data=str(current_out),
                        file_name=f"{self.algo_name}_result.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                else:
                    st.button("📄 Tải xuống .txt", disabled=True, use_container_width=True)
            # Ô hiển thị văn bản kết quả
            st.text_area(" 📤 Văn bản sau xử lý:", value=current_out, height=200)

        with right_col:
            st.markdown("### 🖥️ PROCESSOR LOG")
            # Kiểm tra nếu có log phân đoạn thì hiển thị
            if st.session_state.segmented_logs:
                for i, chunk in enumerate(st.session_state.segmented_logs):
                    # Đoạn đầu tiên (i == 0) sẽ luôn mở, các đoạn sau sẽ đóng
                    is_first = (i == 0)
                    
                    with st.expander(chunk['title'], expanded=is_first):
                        terminal_html = f"""
                            <div style="
                                background-color: #000000; 
                                color: #00FF00; 
                                font-family: 'Courier New', Courier, monospace; 
                                padding: 12px; 
                                border-radius: 5px; 
                                font-size: 13px; 
                                line-height: 1.5;
                                max-height: 550px; 
                                overflow-y: auto;
                                border: 1px solid #333;
                                white-space: pre-wrap;
                            ">
            {chunk['content']}
                            </div>
                        """
                        st.markdown(terminal_html, unsafe_allow_html=True)
            else:
                st.info("Chưa có tiến trình chi tiết.")

            # Nút xóa log
            if st.button("Xóa Log & Dữ Liệu", use_container_width=True):
                st.session_state.segmented_logs = []
                st.rerun()

    def handle_encrypt(self, algo_name, text, params):
        if algo_name == "Caesar":
            try:
                # Ép kiểu an toàn
                shift_val = params.get('shift_key', 0)
                shift = int(shift_val) if str(shift_val).isdigit() else 0
                
                # Gọi hàm core trả về (kết quả, danh sách logs)
                from core.classical import caesar_cipher_segmented
                res, logs = caesar_cipher_segmented(text, shift, mode='encrypt')
                
                # Cập nhật vào session_state
                st.session_state.segmented_logs = logs
                return res
            except Exception as e:
                st.error(f"Lỗi mã hóa Caesar: {e}")
                return ""
        elif algo_name == "Vigenère":
            try:
                v_key = params.get('vigenere_key', '').strip()
                if not v_key:
                    st.error("Vui lòng nhập Key cho Vigenère!")
                    return ""
                
                from core.classical.vigenere_core import vigenere_cipher_segmented
                res, logs = vigenere_cipher_segmented(text, v_key, mode='encrypt')
                
                st.session_state.segmented_logs = logs
                return res
            except Exception as e:
                st.error(f"Lỗi Vigenère: {e}")
                return ""
        elif algo_name == "RSA":
            try:
                # Lấy trực tiếp n và e từ các ô nhập liệu ở Tab 2
                n = params.get('n_exec', '').strip()
                e = params.get('e_exec', '').strip()
                
                if not n or not e:
                    st.error("❌ Thiếu thông số Modulus (n) hoặc Public Exponent (e) để mã hóa!")
                    return ""
                
                # Ép kiểu sang int để tính toán
                n = int(n)
                e = int(e)
                
                from core.public_key.rsa_core import rsa_process_segmented
                # Lưu ý: Truyền n và e vào hàm xử lý. 
                res, logs = rsa_process_segmented(text, n, e, mode='encrypt')
                
                if res is None:
                    st.error(logs[0]['content'] if logs else "Lỗi mã hóa RSA")
                    return ""
                    
                st.session_state.segmented_logs = logs
                return res
            except ValueError:
                st.error("❌ Modulus (n) và Public Exponent (e) phải là số nguyên!")
                return ""        

    def handle_decrypt(self, algo_name, text, params):
        if algo_name == "Caesar":
            try:
                shift_val = params.get('shift_key', 0)
                shift = int(shift_val) if str(shift_val).isdigit() else 0
                
                from core.classical import caesar_cipher_segmented
                res, logs = caesar_cipher_segmented(text, shift, mode='decrypt')
                
                st.session_state.segmented_logs = logs
                return res
            except Exception as e:
                st.error(f"Lỗi giải mã Caesar: {e}")
                return ""
        if algo_name == "Vigenère":
            v_key = params.get('vigenere_key', '').strip()
            from core.classical.vigenere_core import vigenere_cipher_segmented
            res, logs = vigenere_cipher_segmented(text, v_key, mode='decrypt')
            st.session_state.segmented_logs = logs
            return res
        elif algo_name == "RSA":
            try:
                # Lấy trực tiếp n và d từ các ô nhập liệu ở Tab 2
                n = params.get('n_exec', '').strip()
                d = params.get('d_exec', '').strip()
                
                if not n or not d:
                    st.error("❌ Thiếu thông số Modulus (n) hoặc Private Exponent (d) để giải mã!")
                    return ""
                
                # Ép kiểu sang int
                n = int(n)
                d = int(d)
                
                from core.public_key.rsa_core import rsa_process_segmented
                # Giải mã sử dụng n và d
                res, logs = rsa_process_segmented(text, n, d, mode='decrypt')
                
                if res is None:
                    st.error(logs[0]['content'] if logs else "Lỗi giải mã RSA")
                    return ""
                    
                st.session_state.segmented_logs = logs
                return res
            except ValueError:
                st.error("❌ Modulus (n) và Private Exponent (d) phải là số nguyên!")
                return ""