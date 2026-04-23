import customtkinter as ctk
import time
from .home_view import HomeView
from .crypto_view import CryptoView
from .attack_view import AttackView

class CryptoGui:
    def __init__(self, master):
        self.master = master
        
        # Sidebar
        self.sidebar = ctk.CTkFrame(self.master, width=240, fg_color="#F8F9FA", corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        ctk.CTkLabel(self.sidebar, text="🛡️ CRYPTO ENGINE", font=("Segoe UI", 20, "bold")).pack(pady=35)

        # Nơi chứa nội dung thay đổi
        self.container = ctk.CTkFrame(self.master, fg_color="transparent")
        self.container.pack(side="right", fill="both", expand=True)

        self.current_view = None
        self.create_menu()
        self.show_welcome()

    def create_menu(self):
        menus = [
            ("🏠 Giới thiệu", self.show_welcome),
            ("🔒 Hệ mật Caesar", lambda: self.show_crypto_ui("Caesar")),
            ("🔐 Hệ mật Vigenère", lambda: self.show_crypto_ui("Vigenère")),
            ("🔑 Hệ mật RSA", lambda: self.show_crypto_ui("RSA")),
            ("🔑 Thám mã", lambda: self.show_attack_ui("Thám mã"))
        ]
        
        # PHẢI có vòng lặp này ở ĐÂY để render các nút bấm lên Sidebar
        for name, cmd in menus:
            ctk.CTkButton(
                self.sidebar, 
                text=name, 
                fg_color="transparent", 
                text_color="#333333",
                hover_color="#E9ECEF", # Thêm hover cho đẹp
                anchor="w", 
                command=cmd
            ).pack(fill="x", padx=15, pady=5)

    def show_attack_ui(self, name):
        if self.current_view:
            self.current_view.destroy()
        # Đảm bảo AttackView có kế thừa từ ctk.CTkFrame
        self.current_view = AttackView(self.container, algo_name=name, master_app=self.master)
        self.current_view.pack(fill="both", expand=True, padx=20, pady=20)
    def show_welcome(self):
        if self.current_view: self.current_view.destroy()
        self.current_view = HomeView(self.container)
        self.current_view.pack(fill="both", expand=True, padx=20, pady=20)

    def show_crypto_ui(self, name):
        if self.current_view: self.current_view.destroy()
        self.current_view = CryptoView(self.container, algo_name=name, master_app=self.master)
        self.current_view.pack(fill="both", expand=True, padx=20, pady=20)