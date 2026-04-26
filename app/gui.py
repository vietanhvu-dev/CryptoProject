import streamlit as st
from .home_view import HomeView
from .crypto_view import CryptoView
from app.attack_caesar import AttackCaesar
from app.attack_vi import AttackVi

class CryptoGui:
    def __init__(self, master):
        self.master = master
        
        if "view_name" not in st.session_state:
            st.session_state.view_name = "welcome"
        if "algo_name" not in st.session_state:
            st.session_state.algo_name = ""

        self.create_menu()
        self.render_current_view()

    def create_menu(self):
        with st.sidebar:
            st.markdown("## 🛡️ CRYPTO ENGINE")
            
            if st.button("🏠 Giới thiệu", use_container_width=True, icon="🏠"):
                self.show_welcome()
            st.write("---")
            st.markdown("### ⚡ Hệ mật")
            
            if st.button("🔒 Hệ mật Caesar", use_container_width=True, icon="🔒"):
                self.show_crypto_ui("Caesar")
                
            if st.button("🔐 Hệ mật Vigenère", use_container_width=True, icon="🔐"):
                self.show_crypto_ui("Vigenère")
                
            if st.button("🔑 Hệ mật RSA", use_container_width=True, icon="🔑"):
                self.show_crypto_ui("RSA")
            
            st.write("---")
            st.markdown("### ⚡ Thám mã")
            
            # Sửa lại ở đây: gọi cụ thể từng view mới
            if st.button("⚡ Thám mã Caesar", use_container_width=True):
                self.show_attack_caesar()

            if st.button("⚡ Thám mã Vigenère", use_container_width=True):
                self.show_attack_vi()

    # --- Các hàm điều hướng mới ---
    def show_attack_caesar(self):
        st.session_state.view_name = "attack_caesar"
        st.session_state.algo_name = "Caesar"
        st.rerun()

    def show_attack_vi(self):
        st.session_state.view_name = "attack_vi"
        st.session_state.algo_name = "Vigenère"
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
        view = st.session_state.view_name
        name = st.session_state.algo_name

        if view == "welcome":
            home = HomeView(self.master)
            home.render() 
            
        elif view == "crypto":
            crypto = CryptoView(None, algo_name=name, master_app=self.master)
            crypto.render()
            
        elif view == "attack_caesar":
            # Thêm algo_name=name vào đây
            attack = AttackCaesar(None, algo_name=name, master_app=self.master)
            attack.render()

        elif view == "attack_vi":
            # Tương tự cho Vigenère nếu class đó cũng yêu cầu algo_name
            attack = AttackVi(None, algo_name=name, master_app=self.master)
            attack.render()