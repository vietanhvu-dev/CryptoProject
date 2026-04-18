import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import customtkinter as ctk
from app.gui import CryptoGui
# from core.public_key.rsa import RSACryptosystem
# from core.classical.caesar import CaesarCipher 

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Advanced Cryptosystem Demo Platform")
        self.geometry("1100x700")
        
        # Tạm thời để dict trống
        self.crypto_engines = {} 

        self.ui = CryptoGui(self) 
        
    def handle_encrypt(self, algo_name, data, key_input):
        return f"Đang giả lập mã hóa {algo_name}: {data}"

    def handle_decrypt(self, algo_name, data, key_input):
        return f"Đang giả lập giải mã {algo_name}: {data}"
    

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()