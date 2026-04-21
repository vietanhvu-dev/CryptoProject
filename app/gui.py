import customtkinter as ctk
import time

class CryptoGui:
    def __init__(self, master):
        self.master = master
        # Thiết lập giao diện sáng, hiện đại
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # --- Sidebar (Menu bên trái) ---
        self.sidebar = ctk.CTkFrame(self.master, width=240, fg_color="#F8F9FA", corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        
        self.logo = ctk.CTkLabel(self.sidebar, text="🛡️ CRYPTO ENGINE v2.0", 
                                font=("Segoe UI", 20, "bold"), text_color="#1f538d")
        self.logo.pack(pady=35)

        self.create_menu()

        # --- Content Area (Bên phải) ---
        self.main_view = ctk.CTkFrame(self.master, fg_color="#F1F3F5", corner_radius=20)
        self.main_view.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        self.show_welcome()

    def create_menu(self):
        # Danh sách menu với Icon
        menus = [
            ("🏠 Giới thiệu", self.show_welcome),
            ("🔒 Hệ mật Caesar", lambda: self.show_crypto_ui("Caesar")),
            ("🔐 Hệ mật Vigenère", lambda: self.show_crypto_ui("Vigenère")), # Thêm dòng này
            ("🔑 Hệ mật RSA", lambda: self.show_crypto_ui("RSA")),
            ("📊 Phân tích dữ liệu", lambda: self.show_analysis_ui()),
            ("🎯 Thám mã (Attack)", lambda: self.show_crypto_ui("Thám mã"))
        ]
        for name, cmd in menus:
            # Sử dụng font "normal" để tránh lỗi hệ thống nhưng vẫn giữ Segoe UI đẹp
            btn = ctk.CTkButton(self.sidebar, text=name, fg_color="transparent",
                                 text_color="#333333", hover_color="#E9ECEF",
                                 font=("Segoe UI", 14, "normal"), anchor="w", 
                                 height=45, command=cmd)
            btn.pack(fill="x", padx=15, pady=5)

    def clear_main_view(self):
        for widget in self.main_view.winfo_children():
            widget.destroy()

    def show_welcome(self):
        """Trang giới thiệu cá nhân với sơ đồ toán học"""
        self.clear_main_view()

        # Thông tin cá nhân
        title = ctk.CTkLabel(self.main_view, text="VŨ VIỆT ANH", 
                             font=("Segoe UI", 28, "bold"), text_color="#1f538d")
        title.pack(pady=(20, 5))
        
        info = "Data Engineer | FPT Software\n\nPhần mềm mô phỏng các thuật toán mật mã và phân tích dữ liệu"
        ctk.CTkLabel(self.main_view, text=info, font=("Segoe UI", 14), text_color="#495057").pack()

    def show_crypto_ui(self, name):
        self.clear_main_view()
        
        # Layout chia 2 cột: Thao tác | Log
        self.main_view.grid_columnconfigure(0, weight=3)
        self.main_view.grid_columnconfigure(1, weight=2)
        
        left_panel = ctk.CTkFrame(self.main_view, fg_color="transparent")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        ctk.CTkLabel(left_panel, text=f"Hệ mật: {name}", font=("Segoe UI", 22, "bold"), text_color="#1f538d").pack(anchor="w")
        
        # 1. Input Text
        ctk.CTkLabel(left_panel, text="Dữ liệu đầu vào:").pack(anchor="w", pady=(10, 0))
        self.input_text = ctk.CTkTextbox(left_panel, height=120, font=("Segoe UI", 13))
        self.input_text.pack(fill="x", pady=5)

        # 2. KHU VỰC THAM SỐ BIẾN ĐỔI
        param_frame = ctk.CTkFrame(left_panel, fg_color="#E9ECEF", corner_radius=10)
        param_frame.pack(fill="x", pady=10, ipady=5)
        
        self.params = {} 
        if name == "Caesar":
            self._add_param_field(param_frame, "Độ dịch (Shift):", "shift_key", "Nhập số (vd: 3)")
        elif name == "Vigenère":
            self._add_param_field(param_frame, "Từ khóa (Keyword):", "vigenere_key", "Nhập chữ (vd: FPT)")
        elif name == "RSA":
            self._add_param_field(param_frame, "Số p:", "p_key", "Số nguyên tố p")
            self._add_param_field(param_frame, "Số q:", "q_key", "Số nguyên tố q")
        else:
            ctk.CTkLabel(param_frame, text="Thuật toán này không cần tham số phụ.").pack()

        # 3. Nút bấm
        btn_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="MÃ HÓA", command=lambda: self._animate_process(name, "encrypt")).grid(row=0, column=0, padx=10)
        ctk.CTkButton(btn_frame, text="GIẢI MÃ", fg_color="#912c2c", command=lambda: self._animate_process(name, "decrypt")).grid(row=0, column=1, padx=10)

        # 4. Kết quả
        ctk.CTkLabel(left_panel, text="Kết quả:").pack(anchor="w", pady=(10, 0))
        self.output_text = ctk.CTkTextbox(left_panel, height=120, font=("Segoe UI", 13))
        self.output_text.pack(fill="x", pady=5)

        # --- Cột phải: Log toán học ---
        self._create_log_panel()

    def _add_param_field(self, parent, label_text, key_name, placeholder):
        """Hàm phụ để tạo nhanh các dòng nhập tham số"""
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=15, pady=2)
        ctk.CTkLabel(row, text=label_text, width=120, anchor="w").pack(side="left")
        entry = ctk.CTkEntry(row, placeholder_text=placeholder)
        entry.pack(side="left", fill="x", expand=True)
        self.params[key_name] = entry # Lưu lại để truy xuất

    def _create_log_panel(self):
        """Tạo khung log màu đen bên phải"""
        right_panel = ctk.CTkFrame(self.main_view, fg_color="#1a1a1a", corner_radius=15)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(0, 20), pady=20)
        ctk.CTkLabel(right_panel, text="PROCESSOR LOG", font=("Consolas", 12, "bold"), text_color="#00FF00").pack(pady=10)
        self.log_box = ctk.CTkTextbox(right_panel, fg_color="black", text_color="#00FF00", font=("Consolas", 11))
        self.log_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
    def _animate_process(self, algo, action):
        data = self.input_text.get("1.0", "end-1c")
        
        # Lấy tham số tùy theo thuật toán
        param_value = ""
        if algo == "Caesar":
            param_value = self.params["shift_key"].get()
        elif algo == "Vigenère":
            param_value = self.params["vigenere_key"].get()
        elif algo == "RSA":
            # Ví dụ lấy p, q rồi ghép lại hoặc xử lý riêng
            p = self.params["p_key"].get()
            q = self.params["q_key"].get()
            param_value = f"{p},{q}"

        # Cập nhật LOG cho sinh động
        self.log_box.delete("1.0", "end")
        self.log_box.insert("end", f"> Khởi chạy engine: {algo}\n")
        if algo == "Vigenère":
            self.log_box.insert("end", f"> Sử dụng từ khóa: '{param_value}'\n")
            self.log_box.insert("end", "> Đang tạo bảng Vigenère Square...\n")
            self.log_box.insert("end", "> Áp dụng phép cộng Modulo 26 theo keyword...\n")
        
        self.log_box.insert("end", "> Hoàn tất.\n")

        # Gọi xuống main.py
        if action == "encrypt":
            result = self.master.handle_encrypt(algo, data, param_value)
        else:
            result = self.master.handle_decrypt(algo, data, param_value)
            
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", result)
        # Lấy dữ liệu văn bản
        data = self.input_text.get("1.0", "end-1c")
        
        # Lấy tham số tương ứng
        key_value = ""
        if algo == "Caesar":
            key_value = self.params["shift_key"].get()
        elif algo == "Vigenère":
            key_value = self.params["vigenere_key"].get()
        # Đối với RSA, bạn có thể lấy p = self.params["p_key"].get(),...

        self.log_box.delete("1.0", "end")
        self.log_box.insert("end", f"> Engine: {algo}\n> Action: {action.upper()}\n")
        self.log_box.insert("end", f"> Parameter: {key_value}\n")
        
        # Gửi sang main.py xử lý (truyền thêm key_value)
        if action == "encrypt":
            result = self.master.handle_encrypt(algo, data, key_value)
        else:
            result = self.master.handle_decrypt(algo, data, key_value)
            
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", result)

    def show_analysis_ui(self):
        self.clear_main_view()
        ctk.CTkLabel(self.main_view, text="PHÂN TÍCH TẦN SUẤT DỮ LIỆU", font=("Segoe UI", 22, "bold"), text_color="#1f538d").pack(pady=20)
        placeholder = ctk.CTkFrame(self.main_view, height=300, fg_color="#E9ECEF", corner_radius=15)
        placeholder.pack(fill="x", padx=40)
        ctk.CTkLabel(placeholder, text="[ Biểu đồ thống kê ]", text_color="gray").place(relx=0.5, rely=0.5, anchor="center")