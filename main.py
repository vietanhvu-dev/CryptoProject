import streamlit as st
import sys
import os

# Đảm bảo import được các folder app, core
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.gui import CryptoGui

class MainApp:
    def __init__(self):
        # 1. Thiết lập cấu hình trang
        st.set_page_config(
            page_title="Cryptosystem Demo Platform",
            layout="wide",
            initial_sidebar_state="expanded",
            menu_items={
                'Get Help': 'https://www.extremely-helpful-docs.com',
                # Thay link GitHub bằng link tài liệu hoặc None
                'Report a bug': "https://www.extremely-helpful-docs.com",
                'About': "# CRYPTO SYSTEM PLATFORM \nThis is a demo platform for classical cryptography and public key systems."
            }
        )

        # 2. Dùng CSS để ẩn Footer, Header và Menu ba chấm
        st.markdown("""
            <style>
                /* Ẩn dòng chữ 'Made with Streamlit' ở cuối trang */
                footer {visibility: hidden;}

            </style>
        """, unsafe_allow_html=True)

        # 2. HIỆU ỨNG MỞ MÀN (SPLASH SCREEN) VÀ CSS GIAO DIỆN
        st.markdown("""
            <div id="splash-overlay">
                <div class="bubble splash-b"></div><div class="bubble splash-b"></div>
                <div class="bubble splash-b"></div><div class="bubble splash-b"></div>
                <div class="bubble splash-b"></div><div class="bubble splash-b"></div>
                <div class="bubble splash-b"></div><div class="bubble splash-b"></div>
                <div class="bubble splash-b"></div><div class="bubble splash-b"></div>
                <div class="bubble splash-b"></div><div class="bubble splash-b"></div>
                <div class="bubble splash-b"></div><div class="bubble splash-b"></div>
                <div class="bubble splash-b"></div>
            </div>

            <style>
                /* Style cho Splash Screen */
                #splash-screen {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100vw;
                    height: 100vh;
                    background: linear-gradient(45deg, #667eea , #764ba2 100%);
                    z-index: 9999999;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    overflow: hidden;
                    /* Hiệu ứng biến mất hoàn toàn sau 4 giây */
                    animation: fadeOutSplash 1s ease-in-out 15s forwards;
                }

                @keyframes fadeOutSplash {
                    from { opacity: 1; visibility: visible; }
                    to { opacity: 0; visibility: hidden; }
                }

                @keyframes textFocus {
                    0% { filter: blur(12px); opacity: 0; transform: scale(0.8); }
                    100% { filter: blur(0px); opacity: 1; transform: scale(1); }
                }

                /* Hiệu ứng Bong bóng */
                .bubble {
                    position: absolute;
                    bottom: -150px;
                    background: rgba(39, 77, 255, 0.1);
                    border-radius: 50%;
                    animation: rise 0.5s infinite ease-in;
                }

                /* Cấu hình chi tiết cho 15 bong bóng */
                .bubble.splash-b:nth-child(2)  { left: 5%;  width: 90px;  height: 90px;  animation-duration: 4.2s; animation-delay: 0.1s; }
                .bubble.splash-b:nth-child(3)  { left: 12%; width: 40px;  height: 40px;  animation-duration: 0.8s; animation-delay: 0.5s; }
                .bubble.splash-b:nth-child(4)  { left: 18%; width: 110px; height: 110px; animation-duration: 3.5s; animation-delay: 0.2s; }
                .bubble.splash-b:nth-child(5)  { left: 25%; width: 60px;  height: 60px;  animation-duration: 1.5s; animation-delay: 0.8s; }
                .bubble.splash-b:nth-child(6)  { left: 32%; width: 30px;  height: 30px;  animation-duration: 0.9s; animation-delay: 0.3s; }
                .bubble.splash-b:nth-child(7)  { left: 40%; width: 130px; height: 130px; animation-duration: 3.2s; animation-delay: 0.0s; }
                .bubble.splash-b:nth-child(8)  { left: 48%; width: 50px;  height: 50px;  animation-duration: 2.1s; animation-delay: 1.2s; }
                .bubble.splash-b:nth-child(9)  { left: 55%; width: 85px;  height: 85px;  animation-duration: 1.8s; animation-delay: 0.4s; }
                .bubble.splash-b:nth-child(10) { left: 62%; width: 45px;  height: 45px;  animation-duration: 1.7s; animation-delay: 0.9s; }
                .bubble.splash-b:nth-child(11) { left: 70%; width: 100px; height: 100px; animation-duration: 2.0s; animation-delay: 0.1s; }
                .bubble.splash-b:nth-child(12) { left: 78%; width: 55px;  height: 55px;  animation-duration: 1.3s; animation-delay: 0.6s; }
                .bubble.splash-b:nth-child(13) { left: 84%; width: 35px;  height: 35px;  animation-duration: 0.8s; animation-delay: 1.5s; }
                .bubble.splash-b:nth-child(14) { left: 90%; width: 120px; height: 120px; animation-duration: 2.8s; animation-delay: 0.2s; }
                .bubble.splash-b:nth-child(15) { left: 95%; width: 70px;  height: 70px;  animation-duration: 1.4s; animation-delay: 0.7s; }
                .bubble.splash-b:nth-child(16) { left: 2%;  width: 25px;  height: 25px;  animation-duration: 1.0s; animation-delay: 1.1s; }
                @keyframes rise {
                    0% { bottom: -150px; transform: translateX(0); opacity: 0; }
                    20% { opacity: 0.7; }
                    100% { bottom: 120%; transform: translateX(100px); opacity: 0; }
                }

                /* 3. CSS CHO GIAO DIỆN CHÍNH (STREAMLIT) */
                header[data-testid="stHeader"] {
                    background: rgba(0,0,0,0) !important;
                }

                .stApp {
                    background: linear-gradient(-45deg, #F7F4E6, #F0AD99, #F0F5A9, #C0FFB8, #F8BF63);
                    background-size: 400% 400%;
                    animation: mainGradient 15s ease infinite;
                }

                @keyframes mainGradient {
                    0% { background-position: 0% 50%; }
                    50% { background-position: 100% 50%; }
                    100% { background-position: 0% 50%; }
                }

                /* Glassmorphism cho các Widget */
                .stExpander, div[data-testid="stForm"], .stTextInput, .stTextArea, .stNumberInput {
                    background-color: rgba(255, 255, 255, 0.85) !important;
                    border-radius: 15px !important;
                    border: 1px solid rgba(255, 255, 255, 0.3) !important;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1) !important;
                    backdrop-filter: blur(4px);
                    margin-bottom: 1rem;
                }

                section[data-testid="stSidebar"] {
                    background-color: rgba(255, 255, 255, 0.5) !important;
                    backdrop-filter: blur(10px);
                }
            </style>
        """, unsafe_allow_html=True)

        self.crypto_engines = {} 

        # 4. Khởi tạo UI
        self.ui = CryptoGui(self) 

# --- PHẦN KHỞI CHẠY ---
if __name__ == "__main__":
    MainApp()