import streamlit as st

class HomeView:
    def __init__(self, master=None, **kwargs):
        self.master = master

    def render(self):
        # 1. Thêm CSS cho Background động và hiệu ứng Glassmorphism
        st.markdown("""
            <style>
            /* Background động với hiệu ứng Gradient di chuyển */
            .main {
                background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
                background-size: 400% 400%;
                animation: gradient 15s ease infinite;
            }

            @keyframes gradient {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }

            /* Container chính với hiệu ứng kính mờ */
            .glass-card {
                background: rgba(255, 255, 255, 0.85);
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.18);
                padding: 30px;
                margin-bottom: 25px;
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
            }

            /* Tùy chỉnh các tiêu đề */
            .main-title {
                color: #1f538d;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                text-align: center;
                font-weight: 800;
            }

            /* Hiệu ứng cho SVG để nổi bật trên nền kính */
            .alice-bob-svg {
                display: block;
                margin: auto;
                filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.1));
            }
            
            /* Tùy chỉnh Expander của Streamlit */
            .stExpander {
                border: none !important;
                background-color: rgba(255, 255, 255, 0.5) !important;
                border-radius: 10px !important;
                margin-bottom: 10px !important;
            }
            </style>
        """, unsafe_allow_html=True)

        # 2. Header & Sơ đồ Alice & Bob
        with st.container():
            st.markdown(f"""
                <div class="glass-card">
                    <h1 class="main-title">VŨ VIỆT ANH</h1>
                    <p style='text-align: center; color: #495057; font-size: 1.1em;'>Data Engineer | Cryptography Researcher</p>
                    <svg width="100%" height="200" viewBox="0 0 500 200" class="alice-bob-svg">
                        <circle cx="100" cy="100" r="40" fill="#1f538d" opacity="0.9" />
                        <text x="100" y="160" font-family="Arial" font-size="14" font-weight="bold" fill="#1f538d" text-anchor="middle">Alice</text>
                        
                        <circle cx="400" cy="100" r="40" fill="#1f538d" opacity="0.9" />
                        <text x="400" y="160" font-family="Arial" font-size="14" font-weight="bold" fill="#1f538d" text-anchor="middle">Bob</text>
                        
                        <defs>
                            <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="0" refY="3.5" orient="auto">
                                <polygon points="0 0, 10 3.5, 0 7" fill="#1f538d" />
                            </marker>
                        </defs>
                        <path d="M 150 100 Q 250 50 350 100" stroke="#1f538d" stroke-width="3" fill="none" marker-end="url(#arrowhead)" stroke-dasharray="5,5" />
                        
                        <rect x="230" y="110" width="40" height="30" rx="5" fill="#fcc419" />
                        <circle cx="250" cy="110" r="8" fill="none" stroke="#fcc419" stroke-width="3" />
                    </svg>
                </div>
            """, unsafe_allow_html=True)

        # 3. Phần giới thiệu chi tiết với Expander
        st.write("### 🛠 Hệ thống Xử lý & Tính năng")
        
        with st.expander("🔐 Thuật toán Mã hóa (Core Cryptography)"):
            st.markdown("""
            **Cách hệ thống xử lý:**
            * **Input Handling:** Tiếp nhận văn bản thô hoặc file từ người dùng.
            * **Key Generation:** Khởi tạo khóa dựa trên thuật toán được chọn (AES, RSA, Classical Ciphers).
            * **Encryption Process:** Dữ liệu được băm nhỏ và xử lý qua các vòng (Rounds) biến đổi toán học trong RAM.
            * **Output:** Trả về Ciphertext dưới dạng Hex hoặc Base64.
            """)

        with st.expander("📊 Phân tích Dữ liệu (Data Engineering)"):
            st.markdown("""
            **Cách hệ thống xử lý:**
            * **Pipeline:** Trích xuất đặc tính từ các bản mã để thực hiện thám mã (Cryptanalysis).
            * **Visualization:** Sử dụng biểu đồ tần suất (Frequency Analysis) để tìm ra quy luật của các bộ mã cổ điển.
            """)

        with st.expander("🛡 Bảo mật & Quyền riêng tư (Security)"):
            st.markdown("""
            **Cách hệ thống xử lý:**
            * **Stateless Processing:** Hệ thống không lưu trữ trạng thái. Sau khi bạn đóng trình duyệt, mọi biến số trong RAM sẽ bị giải phóng.
            * **No Persistence:** Không sử dụng Database cho dữ liệu người dùng, đảm bảo tính riêng tư tuyệt đối.
            """)

        # 4. Footer thông tin thêm
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.info("🎯 **Mục tiêu:** Nghiên cứu và giáo dục về mật mã học.")
        with col2:
            st.warning("⚠️ **Lưu ý:** Đây là môi trường Cloud, hạn chế upload dữ liệu nhạy cảm.")

        st.markdown(
            """
            <div style="text-align: center; padding: 20px;">
                <small>Giấy phép Apache License 2.0 | Xem chi tiết tại 
                <a href="https://github.com/vietanhvu-dev/CryptoProject" target="_blank" style="color: #1f538d;">GitHub</a></small>
            </div>
            """, 
            unsafe_allow_html=True
        )

# Chạy thử
if __name__ == "__main__":
    HomeView().render()