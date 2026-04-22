import customtkinter as ctk
import time

class CryptoView(ctk.CTkFrame):
    def __init__(self, master, algo_name, master_app, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent")
        self.algo_name = algo_name
        self.master_app = master_app # Tham chiếu đến MainApp để xử lý logic

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)

        # --- PANEL TRÁI: INPUT/OUTPUT ---
        self.left_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        ctk.CTkLabel(self.left_panel, text=f"Hệ mật: {algo_name}", font=("Segoe UI", 22, "bold"), text_color="#1f538d").pack(anchor="w")
        
        self.input_text = ctk.CTkTextbox(self.left_panel, height=120)
        self.input_text.pack(fill="x", pady=10)

        # KHU VỰC THAM SỐ ĐỘNG
        self.param_frame = ctk.CTkFrame(self.left_panel, fg_color="#E9ECEF", corner_radius=10)
        self.param_frame.pack(fill="x", pady=10, ipady=5)
        self.params = {}
        self._setup_params()

        # NÚT BẤM
        btn_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="MÃ HÓA", command=lambda: self.process("encrypt")).grid(row=0, column=0, padx=10)
        ctk.CTkButton(btn_frame, text="GIẢI MÃ", fg_color="#912c2c", command=lambda: self.process("decrypt")).grid(row=0, column=1, padx=10)

        self.output_text = ctk.CTkTextbox(self.left_panel, height=120)
        self.output_text.pack(fill="x", pady=10)

        # --- PANEL PHẢI: LOG ---
        self.right_panel = ctk.CTkFrame(self, fg_color="#1a1a1a", corner_radius=15)
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=(0, 20), pady=20)
        ctk.CTkLabel(self.right_panel, text="PROCESSOR LOG", font=("Consolas", 12, "bold"), text_color="#00FF00").pack(pady=10)
        self.log_box = ctk.CTkTextbox(self.right_panel, fg_color="black", text_color="#00FF00", font=("Consolas", 11))
        self.log_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _setup_params(self):
        # Xóa sạch các param cũ nếu có
        for widget in self.param_frame.winfo_children():
            widget.destroy()
            
        if self.algo_name == "Caesar":
            self._add_field("Độ dịch (Shift):", "shift_key", "Ví dụ: 3")
        elif self.algo_name == "Vigenère":
            self._add_field("Từ khóa (Key):", "vigenere_key", "Ví dụ: VIETANH")
        elif self.algo_name == "RSA":
            # RSA cần nhiều ô nhập hơn
            self._add_field("Số nguyên tố p:", "p_key", "Nhập p...")
            self._add_field("Số nguyên tố q:", "q_key", "Nhập q...")
            self._add_field("Số e (Public):", "e_key", "Thường là 65537")

    def _add_field(self, label, key, placeholder):
        row = ctk.CTkFrame(self.param_frame, fg_color="transparent")
        row.pack(fill="x", padx=10, pady=2)
        ctk.CTkLabel(row, text=label, width=100, anchor="w").pack(side="left")
        entry = ctk.CTkEntry(row, placeholder_text=placeholder)
        entry.pack(side="left", fill="x", expand=True)
        self.params[key] = entry

    def process(self, action):
        data = self.input_text.get("1.0", "end-1c")
        
        # Đóng gói toàn bộ params thành một dictionary
        current_params = {k: v.get() for k, v in self.params.items()}
        
        self.log_box.insert("end", f"> Đang xử lý {self.algo_name}...\n")
        
        # Truyền cả dictionary params này vào hàm xử lý của MainApp
        if action == "encrypt":
            result = self.master_app.handle_encrypt(self.algo_name, data, current_params)
        else:
            result = self.master_app.handle_decrypt(self.algo_name, data, current_params)
            
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", result)