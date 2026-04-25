import streamlit as st
from .home_view import HomeView
from .crypto_view import CryptoView
from .attack_view import AttackView

class CryptoGui:
    def __init__(self, master):
        # master ở đây trong ngữ cảnh Web sẽ là đối tượng chứa các hàm xử lý logic (handle_encrypt...)
        self.master = master
        
        # Streamlit không có khái niệm self.container.pack()
        # Chúng ta dùng session_state để giả lập việc lưu trữ "current_view"
        if "view_name" not in st.session_state:
            st.session_state.view_name = "welcome"
        if "algo_name" not in st.session_state:
            st.session_state.algo_name = ""

        self.create_menu()
        self.render_current_view()

    def create_menu(self):
        # Sidebar của Streamlit
        with st.sidebar:
            st.markdown("## 🛡️ CRYPTO ENGINE")
            st.write("---")
            
            # Thay vì dùng Button với command, ta dùng nút bấm Streamlit 
            # để cập nhật trạng thái view
            if st.button("🏠 Giới thiệu", use_container_width=True, icon="🏠"):
                self.show_welcome()
            
            if st.button("🔒 Hệ mật Caesar", use_container_width=True, icon="🔒"):
                self.show_crypto_ui("Caesar")
                
            if st.button("🔐 Hệ mật Vigenère", use_container_width=True, icon="🔐"):
                self.show_crypto_ui("Vigenère")
                
            if st.button("🔑 Hệ mật RSA", use_container_width=True, icon="🔑"):
                self.show_crypto_ui("RSA")
                
            if st.button("⚡ Thám mã", use_container_width=True, icon="⚡"):
                self.show_attack_ui("Thám mã")

    def show_attack_ui(self, name):
        # Thay vì .destroy(), ta chỉ cần cập nhật trạng thái để Streamlit vẽ lại
        st.session_state.view_name = "attack"
        st.session_state.algo_name = name
        st.rerun()

    def show_welcome(self):
        st.session_state.view_name = "welcome"
        st.session_state.algo_name = ""
        st.rerun()

    def show_crypto_ui(self, name):
        st.session_state.view_name = "crypto"
        st.session_state.algo_name = name
        st.rerun()

    def render_current_view(self):
        """
        Phương thức này đóng vai trò thay thế cho self.container.
        Nó sẽ kiểm tra trạng thái và gọi hàm render từ các View tương ứng.
        """
        view = st.session_state.view_name
        name = st.session_state.algo_name

        if view == "welcome":
            # Giả định HomeView của bạn có hàm render() đã được chuyển đổi
            home = HomeView(None) # master = None hoặc self.master
            home.render() 
            
        elif view == "crypto":
            # Khởi tạo và chạy CryptoView
            crypto = CryptoView(None, algo_name=name, master_app=self.master)
            crypto.render() # Bạn sẽ copy code CryptoView đã chuyển đổi vào hàm render này
            
        elif view == "attack":
            # Khởi tạo và chạy AttackView
            attack = AttackView(None, algo_name=name, master_app=self.master)
            attack.render()