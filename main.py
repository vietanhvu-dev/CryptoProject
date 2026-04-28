import streamlit as st
import sys
import os

# Đảm bảo import được các folder app, core
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.gui import CryptoGui

class MainApp:
    def __init__(self):
        # 1. Thiết lập cấu hình trang (Phải là lệnh Streamlit đầu tiên)
        st.set_page_config(
            page_title="Cryptosystem Demo Platform",
            layout="wide",
            initial_sidebar_state="expanded",
            menu_items={
                'Get Help': 'https://www.extremely-helpful-docs.com',
                'Report a bug': "https://github.com/vietanhvu-dev/CryptoProject/issues",
                'About': "# Web-App \nĐây là ứng dụng demo các hệ mật mã cổ điển và khóa công khai."
            }
        )
        
               
        # --- CSS TỰ ĐỘNG LÀM NỔI BẬT WIDGET ---
        st.markdown("""
            <style>
            /* 1. Hiệu ứng nền động cũ */
            @keyframes gradient {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }

            .stApp {
                background: linear-gradient(-45deg, #F7F4E6, #E3FAF3, #E3E7FA, #FAF9E3, #C2EDCA);
                background-size: 400% 400%;
                animation: gradient 15s ease infinite;
            }

            /* 2. Tự động làm trắng và nổi bật tất cả Expander & Input Boxes */
            /* Nhắm vào các thẻ div chứa expander, text area, input và container */
            .stExpander, div[data-testid="stForm"], .stTextInput, .stTextArea, .stNumberInput {
                background-color: rgba(255, 255, 255, 0.9) !important; /* Trắng 90% để vẫn hơi thấy nền nhẹ */
                border-radius: 15px !important;
                border: none !important;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important; /* Đổ bóng tạo độ nổi */
                margin-bottom: 15px !important;
            }

            /* Làm Header của Expander đậm và rõ hơn */
            .stExpander details summary {
                font-weight: bold !important;
                color: #1f538d !important;
            }

            /* Fix màu chữ trong các ô nhập liệu để không bị chìm */
            input, textarea {
                color: #000000 !important;
            }
            </style>
            """, unsafe_allow_html=True)
        self.crypto_engines = {} 

        # 3. Khởi tạo UI
        self.ui = CryptoGui(self) 

# --- PHẦN KHỞI CHẠY ---
if __name__ == "__main__":
    # Trong Streamlit, mỗi khi người dùng tương tác, toàn bộ script sẽ chạy lại từ đầu.
    # Việc khởi tạo trực tiếp MainApp() là cách chuẩn để đảm bảo UI luôn được render mới nhất.
    MainApp()