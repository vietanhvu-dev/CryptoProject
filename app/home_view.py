import customtkinter as ctk

class HomeView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#F1F3F5", corner_radius=20)

        # Vẽ sơ đồ Alice & Bob
        self.canvas = ctk.CTkCanvas(self, width=500, height=250, bg="#F1F3F5", highlightthickness=0)
        self.canvas.pack(pady=(40, 0))
        
        # Vẽ Alice
        self.canvas.create_oval(50, 80, 120, 150, fill="#1f538d", outline="") 
        self.canvas.create_text(85, 165, text="Alice", font=("Segoe UI", 12, "bold"), fill="#1f538d")
        
        # Vẽ Bob
        self.canvas.create_oval(380, 80, 450, 150, fill="#1f538d", outline="")
        self.canvas.create_text(415, 165, text="Bob", font=("Segoe UI", 12, "bold"), fill="#1f538d")

        # Mũi tên & Khóa
        self.canvas.create_line(130, 115, 370, 115, arrow="last", width=3, fill="#adb5bd")
        self.canvas.create_rectangle(230, 120, 270, 150, fill="#fcc419", outline="")

        # Thông tin cá nhân
        ctk.CTkLabel(self, text="VŨ VIỆT ANH", font=("Segoe UI", 28, "bold"), text_color="#1f538d").pack(pady=(20, 5))
        ctk.CTkLabel(self, text="Data Engineer | FPT Software", font=("Segoe UI", 14), text_color="#495057").pack()