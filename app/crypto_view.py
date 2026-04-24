import customtkinter as ctk
from tkinter import filedialog, messagebox
import time

class CryptoView(ctk.CTkFrame):
    def __init__(self, master, algo_name, master_app, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent")
        self.algo_name = algo_name
        self.master_app = master_app 
        self.params = {}

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)

        # --- PANEL TRÁI: INPUT/OUTPUT ---
        self.left_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # Header với nút Import File
        header_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 5))
        
        ctk.CTkLabel(header_frame, text=f"Hệ mật: {algo_name}", font=("Segoe UI", 22, "bold"), text_color="#1f538d").pack(side="left")
        ctk.CTkButton(header_frame, text="📁 Tải File", width=80, height=26, font=("Segoe UI", 12), command=self.import_file).pack(side="right")
        
        self.input_text = ctk.CTkTextbox(self.left_panel, height=120)
        self.input_text.pack(fill="x", pady=(0, 10))

        # KHU VỰC THAM SỐ ĐỘNG
        self.param_frame = ctk.CTkFrame(self.left_panel, fg_color="#E9ECEF", corner_radius=10)
        self.param_frame.pack(fill="x", pady=10, ipady=5)
        self._setup_params()

        # NÚT BẤM THỰC THI
        btn_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="MÃ HÓA", command=lambda: self.process("encrypt")).grid(row=0, column=0, padx=10)
        ctk.CTkButton(btn_frame, text="GIẢI MÃ", fg_color="#912c2c", command=lambda: self.process("decrypt")).grid(row=0, column=1, padx=10)

        # Kết quả với nút Export File
        result_header = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        result_header.pack(fill="x", pady=(10, 5))
        ctk.CTkLabel(result_header, text="Kết quả:", font=("Segoe UI", 13, "bold")).pack(side="left")
        ctk.CTkButton(result_header, text="💾 Xuất File", width=80, height=26, font=("Segoe UI", 12), command=self.export_file).pack(side="right")

        self.output_text = ctk.CTkTextbox(self.left_panel, height=120)
        self.output_text.pack(fill="x", pady=0)

        # --- PANEL PHẢI: LOG ---
        self.right_panel = ctk.CTkFrame(self, fg_color="#1a1a1a", corner_radius=15)
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=(0, 20), pady=20)
        ctk.CTkLabel(self.right_panel, text="PROCESSOR LOG", font=("Consolas", 12, "bold"), text_color="#00FF00").pack(pady=10)
        self.log_box = ctk.CTkTextbox(self.right_panel, fg_color="black", text_color="#00FF00", font=("Consolas", 11))
        self.log_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _setup_params(self):
        for widget in self.param_frame.winfo_children():
            widget.destroy()
            
        if self.algo_name == "Caesar":
            self._add_field("Độ dịch (Shift):", "shift_key", "Ví dụ: 3")
        elif self.algo_name == "Vigenère":
            self._add_field("Từ khóa (Key):", "vigenere_key", "Ví dụ: VIETANH")
        elif self.algo_name == "RSA":
            self._add_field("Số nguyên tố p:", "p_key", "Nhập p...")
            self._add_field("Số nguyên tố q:", "q_key", "Nhập q...")
            self._add_field("Số e (Public):", "e_key", "Thường là 65537")

    def _add_field(self, label, key, placeholder):
        """Tạo field có nút Ẩn/Hiện"""
        row = ctk.CTkFrame(self.param_frame, fg_color="transparent")
        row.pack(fill="x", padx=10, pady=4)
        
        ctk.CTkLabel(row, text=label, width=110, anchor="w").pack(side="left")
        
        # Mặc định dùng show="*" để ẩn
        entry = ctk.CTkEntry(row, placeholder_text=placeholder, show="*")
        entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        # Nút con mắt để ẩn/hiện
        show_btn = ctk.CTkButton(row, text="👁️", width=30, fg_color="transparent", 
                                  text_color="gray", hover_color="#D1D1D1",
                                  command=lambda e=entry: self._toggle_pass(e))
        show_btn.pack(side="right")
        
        self.params[key] = entry

    def _toggle_pass(self, entry):
        """Xử lý ẩn hiện ký tự"""
        if entry.cget("show") == "*":
            entry.configure(show="")
        else:
            entry.configure(show="*")

    def import_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    self.input_text.delete("1.0", "end")
                    self.input_text.insert("end", f.read())
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể đọc file: {e}")

    def export_file(self):
        content = self.output_text.get("1.0", "end-1c")
        if not content.strip():
            messagebox.showwarning("Cảnh báo", "Kết quả trống, không có gì để xuất!")
            return
            
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                messagebox.showinfo("Thành công", "Đã xuất file thành công!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu file: {e}")

    def process(self, action):
        data = self.input_text.get("1.0", "end-1c")
        current_params = {k: v.get() for k, v in self.params.items()}
        
        self.log_box.insert("end", f"> Engine: {self.algo_name} | Action: {action.upper()}\n")
        
        # Gọi MainApp xử lý
        result = self.master_app.handle_encrypt(self.algo_name, data, current_params) if action == "encrypt" else \
                 self.master_app.handle_decrypt(self.algo_name, data, current_params)
            
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", result)
        self.log_box.insert("end", "> Xử lý hoàn tất.\n")
        self.log_box.see("end")