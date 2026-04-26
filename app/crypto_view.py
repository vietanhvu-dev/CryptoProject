import streamlit as st
class CryptoView:
    def __init__(self, master, algo_name, master_app, **kwargs):
        self.master = master
        self.algo_name = algo_name
        self.master_app = master_app

    def render(self): 
        st.markdown(f"<h1 style='color: #1f538d;'>Hệ mật: {self.algo_name}</h1>", unsafe_allow_html=True)

        # Chia cột chính (Trái: Xử lý | Phải: Log)
        left_col, right_col = st.columns([3, 2])

        with left_col:
            # 1. KHU VỰC INPUT
            st.write("### 📥 Đầu vào")
            uploaded_file = st.file_uploader("📁 Tải File (.txt)", type=['txt'], key=f"upload_{self.algo_name}")
            
            input_data = ""
            if uploaded_file:
                input_data = uploaded_file.read().decode("utf-8")
            
            input_text = st.text_area("Nhập văn bản cần xử lý:", value=input_data, height=150)

            # 2. THAM SỐ ĐỘNG
            st.write("### ⚙️ Tham số")
            params = {}
            
            with st.container():
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
                    params['vigenere_key'] = st.text_input("Từ khóa (Key):", placeholder="Ví dụ: VIETANH", type="password")
                elif self.algo_name == "RSA":
                    c1, c2 = st.columns(2)
                    with c1:
                        params['p_key'] = st.text_input("Số nguyên tố p:", type="password")
                        params['q_key'] = st.text_input("Số nguyên tố q:", type="password")
                    with c2:
                        params['e_key'] = st.text_input("Số e (Public):", value="65537", type="password")
                        
                        # --- Gợi ý số nguyên tố ---
                        import os
                        import random
                        try:
                            file_path = os.path.join("app", "primes.txt")
                            
                            if os.path.exists(file_path):
                                with open(file_path, "r") as f:
                                    # Đọc từng dòng, strip khoảng trắng và chỉ lấy các số > 100
                                    all_primes = [line.strip() for line in f if line.strip() and int(line.strip()) > 100]
                                
                                if all_primes:
                                    if 'rsa_suggestions' not in st.session_state:
                                        st.session_state.rsa_suggestions = random.sample(all_primes, min(5, len(all_primes)))

                                    # Tạo 2 cột nhỏ để hiển thị ngang hàng
                                    col_text, col_btn = st.columns([0.85, 0.15])

                                    with col_text:
                                        primes_str = "  |  ".join(st.session_state.rsa_suggestions)
                                        
                                        # Sử dụng text_input nhưng khóa lại (disabled) để tạo giao diện đồng nhất
                                        st.text_input(
                                            label="Gợi ý (p, q):", 
                                            value=primes_str, 
                                            label_visibility="visible"
                                        )

                                    with col_btn:
                                        if st.button("🔄", help="Đổi số gợi ý"):
                                            st.session_state.rsa_suggestions = random.sample(all_primes, min(5, len(all_primes)))
                                            st.rerun()
                                else:
                                    st.caption("*(File primes.txt trống hoặc không chứa số hợp lệ)*")
                            else:
                                st.caption(f"*(Không tìm thấy file tại: {file_path})*")
                                    
                        except Exception as e:
                            st.caption(f"*(Lỗi đọc file: {str(e)})*")

            # 3. NÚT BẤM THỰC THI
            col_btn1, col_btn2 = st.columns(2)
            action_clicked = None

            if col_btn1.button("🔒 MÃ HÓA", use_container_width=True, type="primary"):
                action_clicked = "encrypt"
            if col_btn2.button("🔓 GIẢI MÃ", use_container_width=True):
                action_clicked = "decrypt"

            if action_clicked:
                if not input_text.strip():
                    st.error("Vui lòng nhập dữ liệu đầu vào!")
                else:
                    st.session_state.logs.append(f"> Engine: {self.algo_name} | Action: {action_clicked.upper()}")
                    with st.spinner("Đang xử lý..."):
                        if action_clicked == "encrypt":
                            result = self.master_app.handle_encrypt(self.algo_name, input_text, params)
                        else:
                            result = self.master_app.handle_decrypt(self.algo_name, input_text, params)
                    
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
            st.text_area("Văn bản sau xử lý:", value=current_out, height=200)

        with right_col:
            # --- PANEL PHẢI: LOG TERMINAL ---
            st.markdown("### 🖥️ PROCESSOR LOG")
            
            if 'logs' not in st.session_state:
                st.session_state.logs = []
            
            # Chuyển list log thành chuỗi văn bản
            log_text = "\n".join(st.session_state.logs) if st.session_state.logs else "Ready to process..."

            # Tạo giao diện Terminal bằng HTML/CSS
            terminal_html = f"""
                <div style="
                    background-color: #000000; 
                    color: #00FF00; 
                    font-family: 'Courier New', Courier, monospace; 
                    padding: 15px; 
                    border-radius: 5px; 
                    height: 850px; 
                    overflow-y: auto; 
                    white-space: pre-wrap;
                    border: 1px solid #333;
                    font-size: 13px;
                    line-height: 1.5;
                ">
{log_text}
                </div>
            """
            st.markdown(terminal_html, unsafe_allow_html=True)
            
            # Nút xóa Log bên dưới
            st.write("") # Tạo khoảng cách nhỏ
            if st.button("Xóa Log", use_container_width=True):
                st.session_state.logs = []
                st.session_state.current_result = ""
                st.rerun()