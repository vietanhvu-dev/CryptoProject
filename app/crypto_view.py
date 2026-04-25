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
            # Nút nạp file (Streamlit xử lý việc đọc file rất gọn)
            uploaded_file = st.file_uploader("📁 Tải File (.txt)", type=['txt'], key=f"upload_{self.algo_name}")
            
            input_data = ""
            if uploaded_file:
                input_data = uploaded_file.read().decode("utf-8")
            
            # Ô nhập văn bản
            input_text = st.text_area("Nhập văn bản cần xử lý:", value=input_data, height=150)

            # 2. THAM SỐ ĐỘNG (Dynamic Params)
            st.write("### ⚙️ Tham số")
            params = {}
            
            # Thay thế _setup_params bằng logic điều kiện của Streamlit
            with st.container():
                st.info("Nhập các khóa bảo mật bên dưới")
                if self.algo_name == "Caesar":
                    params['shift_key'] = st.text_input("Độ dịch (Shift):", placeholder="Ví dụ: 3", type="password")
                elif self.algo_name == "Vigenère":
                    params['vigenere_key'] = st.text_input("Từ khóa (Key):", placeholder="Ví dụ: VIETANH", type="password")
                elif self.algo_name == "RSA":
                    c1, c2 = st.columns(2)
                    with c1:
                        params['p_key'] = st.text_input("Số nguyên tố p:", type="password")
                        params['q_key'] = st.text_input("Số nguyên tố q:", type="password")
                    with c2:
                        params['e_key'] = st.text_input("Số e (Public):", value="65537", type="password")

            # 3. NÚT BẤM THỰC THI
            st.write("---")
            col_btn1, col_btn2 = st.columns(2)
            
            result = ""
            action_clicked = None

            if col_btn1.button("🔒 MÃ HÓA", use_container_width=True, type="primary"):
                action_clicked = "encrypt"
            
            if col_btn2.button("🔓 GIẢI MÃ", use_container_width=True):
                action_clicked = "decrypt"

            # Xử lý Logic khi nhấn nút
            if action_clicked:
                if not input_text.strip():
                    st.error("Vui lòng nhập dữ liệu đầu vào!")
                else:
                    # Ghi Log
                    st.session_state.logs.append(f"> Engine: {self.algo_name} | Action: {action_clicked.upper()}")
                    
                    # Gọi logic từ Master App (Giả định hàm xử lý của bạn)
                    with st.spinner("Đang xử lý..."):
                        if action_clicked == "encrypt":
                            result = self.master_app.handle_encrypt(self.algo_name, input_text, params)
                        else:
                            result = self.master_app.handle_decrypt(self.algo_name, input_text, params)
                    
                    st.session_state.current_result = result
                    st.session_state.logs.append("> Xử lý hoàn tất.")

            # 4. KHU VỰC OUTPUT
            st.write("### 📤 Kết quả")
            output_area = st.text_area("Kết quả trả về:", value=st.session_state.get('current_result', ''), height=150)

            # Xuất file (Download)
            if st.session_state.get('current_result'):
                st.download_button(
                    label="💾 Xuất File kết quả",
                    data=st.session_state.current_result,
                    file_name=f"{self.algo_name}_result.txt",
                    mime="text/plain"
                )

        with right_col:
            # --- PANEL PHẢI: LOG ---
            st.markdown("### 🖥️ PROCESSOR LOG")
            # Hiển thị log từ session_state
            if 'logs' not in st.session_state:
                st.session_state.logs = []
            
            log_text = "\n".join(st.session_state.logs)
            st.code(log_text if log_text else "Chờ lệnh...", language="bash")
            
            if st.button("Xóa Log"):
                st.session_state.logs = []
                st.rerun()