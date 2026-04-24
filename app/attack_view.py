import customtkinter as ctk
import threading
from .cryptanalysis_core import CryptanalysisCore

class AttackView(ctk.CTkFrame):
    def __init__(self, master, algo_name, master_app, **kwargs):
        super().__init__(master, **kwargs)
        self.core = CryptanalysisCore()
        self.master_app = master_app
        self.algo_name = algo_name
        self._setup_ui()

    def _setup_ui(self):
        self.configure(fg_color="transparent")
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)

        # --- LEFT PANEL ---
        left_panel = ctk.CTkFrame(self, fg_color="transparent")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        ctk.CTkLabel(left_panel, text=f"CRYPTANALYSIS: {self.algo_name.upper()}", 
                     font=("Segoe UI", 22, "bold"), text_color="#d9534f").pack(anchor="w")
        
        self.input_text = ctk.CTkTextbox(left_panel, height=150)
        self.input_text.pack(fill="x", pady=10)

        self.btn_attack = ctk.CTkButton(left_panel, text="START ATTACK", 
                                       fg_color="#d9534f", command=self.start_attack_thread)
        self.btn_attack.pack(pady=10)

        self.output_text = ctk.CTkTextbox(left_panel, height=200)
        self.output_text.pack(fill="x", pady=10)

        # --- RIGHT PANEL (LOG) ---
        right_panel = ctk.CTkFrame(self, fg_color="#1a1a1a", corner_radius=15)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(0, 20), pady=20)
        
        ctk.CTkLabel(self.right_panel, text="ATTACK STRATEGY", font=("Consolas", 12, "bold"), text_color="#ff4444").pack(pady=10)
        self.log_box = ctk.CTkTextbox(self.right_panel, fg_color="black", text_color="#ff4444", font=("Consolas", 11))
        self.log_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def identify_cipher(self, text):
        # Loại bỏ ký tự không phải chữ cái và chuyển sang uppercase
        clean_text = "".join(filter(str.isalpha, text.upper()))
        if not clean_text:
            return "Unknown"
        
        # Tính toán Index of Coincidence (IC)
        n = len(clean_text)
        frequency = {}
        for char in clean_text:
            frequency[char] = frequency.get(char, 0) + 1
        
        sum_f = sum(f * (f - 1) for f in frequency.values())
        ic = sum_f / (n * (n - 1)) if n > 1 else 0
        
        self.log_box.insert("end", f"> Chỉ số trùng khớp (IC): {ic:.4f}\n")
        
        # Ngưỡng phân loại (Threshold)
        if ic > 0.060:
            return "Caesar"
        else:
            return "Vigenère"

    def run_attack(self):
        ciphertext = self.input_text.get("1.0", "end-1c").strip()
        if not ciphertext: 
            return

        self.log_box.delete("1.0", "end")
        self.output_text.delete("1.0", "end")

        # 1. BƯỚC DÒ ĐOÁN HỆ MẬT
        detected_algo = self.identify_cipher(ciphertext)
        self.log_box.insert("end", f"> Dự đoán hệ mật: {detected_algo}\n", "highlight")

        # 2. BƯỚC PHÁ MÃ (CRACKING)
        if detected_algo == "Caesar":
            self.log_box.insert("end", "> Chiến thuật: Brute Force (26 keys)\n")
            results = []
            for shift in range(1, 26):
                decrypted = self.master_app.handle_decrypt("Caesar", ciphertext, str(shift))
                results.append(...)
                # Cập nhật log ngay lập tức để người dùng thấy app vẫn đang chạy
                self.log_box.insert("end", f"* Đang thử Key {shift}\n")
                self.log_box.see("end") # Tự động cuộn xuống dưới
                self.update_idletasks() # Cập nhật UI ngay lập tức
            
            self.output_text.insert("1.0", "\n".join(results))
            
        elif detected_algo == "Vigenère": # Sửa lỗi self.detected_algo thành detected_algo
            self.log_box.insert("end", "> Chiến thuật: Kasiski & Frequency Analysis\n")
            # Ở đây bạn sẽ gọi logic phá mã Vigenère thực tế
            self.output_text.insert("1.0", "Đang phân tích chu kỳ từ khóa...")