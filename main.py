import streamlit as st
import sys
import os

# Đảm bảo import được các folder app, core
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.gui import CryptoGui

class MainApp:
    def __init__(self):
        # Thiết lập cấu hình trang cho trình duyệt
        st.set_page_config(
            page_title="Advanced Cryptosystem Demo Platform",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Tương tự self.crypto_engines = {}
        self.crypto_engines = {} 

        # Khởi tạo UI và truyền 'self' (MainApp) vào làm master
        # Trong Streamlit, việc khởi tạo này sẽ chạy lại mỗi khi tương tác
        self.ui = CryptoGui(self) 
        
    def handle_encrypt(self, algo_name, data, key_input):
        # Giữ nguyên logic xử lý của bạn
        return f"Đang giả lập mã hóa {algo_name}: {data}"


# --- PHẦN KHỞI CHẠY (Thay thế cho app.mainloop) ---
if __name__ == "__main__":
    # Trong Streamlit, ta dùng session_state để duy trì object MainApp
    if "app_instance" not in st.session_state:
        st.session_state.app_instance = MainApp()
    else:
        # Nếu đã có instance, chỉ cần gọi lại UI để render
        # (Streamlit sẽ tự động chạy lại __init__ của MainApp nếu bạn muốn đơn giản)
        MainApp()