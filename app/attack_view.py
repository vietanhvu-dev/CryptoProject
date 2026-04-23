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
        
        self.log_box = ctk.CTkTextbox(right_panel, fg_color="black", text_color="#00FF00", font=("Consolas", 11))
        self.log_box.pack(fill="both", expand=True, padx=10, pady=10)

    def log(self, message):
        self.log_box.insert("end", f"> {message}\n")
        self.log_box.see("end")

    def start_attack_thread(self):
        # Chạy thám mã trong thread riêng để không treo UI
        threading.Thread(target=self.run_attack, daemon=True).start()

    def run_attack(self):
        ciphertext = self.input_text.get("1.0", "end-1c").strip()
        if not ciphertext: return

        self.btn_attack.configure(state="disabled")
        self.output_text.delete("1.0", "end")
        self.log("Khởi động engine thám mã...")

        # 1. Nhận diện hệ mật
        ic = self.core.get_ic(ciphertext)
        self.log(f"Chỉ số IC tính toán: {ic:.4f}")
        
        algo = "Caesar" if ic > 0.06 else "Vigenère"
        self.log(f"Dự đoán hệ mật: {algo}")

        # 2. Thực hiện thám mã
        if algo == "Caesar":
            self.log("Đang Brute-force và chấm điểm tần suất...")
            results = self.core.crack_caesar(ciphertext, self.master_app.handle_decrypt)
            
            for res in results:
                status = "Khả thi cao" if res["score"] > 0 else "Nhiễu"
                line = f"Key {res['key']:02d} | {res['text'][:30]}... | [{status}]\n"
                self.output_text.insert("end", line)
        else:
            self.output_text.insert("end", self.core.crack_vigenere(ciphertext))

        self.log("Hoàn tất.")
        self.btn_attack.configure(state="normal")