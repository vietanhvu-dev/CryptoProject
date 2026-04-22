import customtkinter as ctk

class AttackView(ctk.CTkFrame):
    def __init__(self, master, algo_name, master_app, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent")
        self.algo_name = algo_name
        self.master_app = master_app

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)

        # --- PANEL TRÁI: INPUT & ATTACK ---
        left_panel = ctk.CTkFrame(self, fg_color="transparent")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        ctk.CTkLabel(left_panel, text=f"THÁM MÃ: {algo_name.upper()}", 
                      font=("Segoe UI", 22, "bold"), text_color="#d9534f").pack(anchor="w")
        
        ctk.CTkLabel(left_panel, text="Nhập bản mã cần thám (Ciphertext):").pack(anchor="w", pady=(10, 0))
        self.input_text = ctk.CTkTextbox(left_panel, height=150)
        self.input_text.pack(fill="x", pady=10)

        # Nút bấm thám mã
        self.btn_attack = ctk.CTkButton(left_panel, text="BẮT ĐẦU TẤN CÔNG (BRUTE FORCE)", 
                                         fg_color="#d9534f", hover_color="#c9302c",
                                         command=self.run_attack)
        self.btn_attack.pack(pady=10)

        ctk.CTkLabel(left_panel, text="Kết quả thám mã dự kiến:").pack(anchor="w", pady=(10, 0))
        self.output_text = ctk.CTkTextbox(left_panel, height=150)
        self.output_text.pack(fill="x", pady=10)

        # --- PANEL PHẢI: CHIẾN THUẬT TẤN CÔNG ---
        self.right_panel = ctk.CTkFrame(self, fg_color="#1a1a1a", corner_radius=15)
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=(0, 20), pady=20)
        
        ctk.CTkLabel(self.right_panel, text="ATTACK STRATEGY", font=("Consolas", 12, "bold"), text_color="#ff4444").pack(pady=10)
        self.log_box = ctk.CTkTextbox(self.right_panel, fg_color="black", text_color="#ff4444", font=("Consolas", 11))
        self.log_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def run_attack(self):
        ciphertext = self.input_text.get("1.0", "end-1c")
        self.log_box.delete("1.0", "end")
        
        if self.algo_name == "Caesar":
            self.log_box.insert("end", "> Chiến thuật: Brute Force (26 keys)\n")
            self.log_box.insert("end", "> Đang thử các tổ hợp dịch xoay...\n")
            # Logic: Thử mọi key từ 1-25
            results = []
            for shift in range(1, 26):
                # Gọi hàm decrypt Caesar từ core của bạn
                decrypted = self.master_app.handle_decrypt("Caesar", ciphertext, str(shift))
                results.append(f"Key {shift:02}: {decrypted[:30]}...")
            
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", "\n".join(results))
            
        elif self.algo_name == "Vigenère":
            self.log_box.insert("end", "> Chiến thuật: Kasiski Examination\n")
            self.log_box.insert("end", "> Phân tích tần suất (Frequency Analysis)...\n")
            self.log_box.insert("end", "> Đang dự đoán độ dài từ khóa (Key Length)...\n")
            self.output_text.insert("1.0", "Hệ thống đang phân tích các mẫu lặp lại...")