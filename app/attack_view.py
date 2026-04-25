import customtkinter as ctk
import threading
from .cryptanalysis_core import CryptanalysisCore
from core.attack.caesar_core import CaesarCracker
from tkinter import filedialog
import os

class AttackView(ctk.CTkFrame):
    def __init__(self, master, algo_name, master_app, **kwargs):
        super().__init__(master, **kwargs)
        self.core = CryptanalysisCore()
        self.caesar_cracker = CaesarCracker()
        self.master_app = master_app
        self.algo_name = algo_name
        self._setup_ui()
    def _setup_ui(self):
        # 1. Cấu hình lưới chính cho AttackView
        self.grid_columnconfigure(0, weight=3) # Vùng làm việc chính
        self.grid_columnconfigure(1, weight=1) # Vùng Log
        self.grid_rowconfigure(0, weight=1)    # Nội dung co giãn
        self.grid_rowconfigure(1, weight=0)    # Thanh công cụ cố định

        # --- LEFT PANEL (Vùng làm việc) ---
        left_panel = ctk.CTkFrame(self, fg_color="transparent")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # A. Header: Tiêu đề + Nút Upload
        header_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(header_frame, text=f"📊 PHÂN TÍCH: {self.algo_name.upper()}", 
                     font=("Segoe UI", 22, "bold"), text_color="#d9534f").pack(side="left")
        
        self.btn_upload = ctk.CTkButton(header_frame, text="📁 Upload Cipher", width=120,
                                         command=self.import_input_file, fg_color="#2f455c",
                                         hover_color="#2c3e50")
        self.btn_upload.pack(side="right")

        # B. Input Section
        ctk.CTkLabel(left_panel, text="Bản mã đầu vào (Ciphertext):", font=("Segoe UI", 13)).pack(anchor="w")
        self.input_text = ctk.CTkTextbox(left_panel, height=120, border_width=1)
        self.input_text.pack(fill="x", pady=(5, 15))

        # C. Action Button
        # Thay vì command=self.execute_logic
        self.btn_attack = ctk.CTkButton(left_panel, text="⚡ START CRYPTANALYSIS", 
                                 font=("Segoe UI", 15, "bold"), height=45,
                                 fg_color="#d9534f", hover_color="#c9302c",
                                 command=self.start_attack_thread) # Gọi hàm bọc thread
        self.btn_attack.pack(fill="x", pady=(0, 15))

        # D. Output Section
        ctk.CTkLabel(left_panel, text="Kết quả trích xuất (Top Candidates):", font=("Segoe UI", 13)).pack(anchor="w")
        self.output_text = ctk.CTkTextbox(left_panel, fg_color="#F5F5F5", text_color="#000000", font=("Consolas", 12))
        self.output_text.pack(fill="both", expand=True)

        # --- RIGHT PANEL (Nhật ký Log) ---
        right_panel = ctk.CTkFrame(self, fg_color="#1a1a1a", corner_radius=15)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(0, 20), pady=20)
        
        ctk.CTkLabel(right_panel, text="SYSTEM LOG", font=("Consolas", 12, "bold")).pack(pady=10)
        self.log_box = ctk.CTkTextbox(right_panel, fg_color="black", text_color="#00FF00", font=("Consolas", 11))
        self.log_box.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tags cho màu sắc log
        self.log_box.tag_config("highlight", foreground="#FF4444")
        self.log_box.tag_config("normal", foreground="#00FF00")

        # --- BOTTOM CONTROL BAR (Thanh điều khiển xuất file) ---
        # Sử dụng fg_color để tạo điểm nhấn cho thanh công cụ
        self.control_frame = ctk.CTkFrame(self, fg_color="#B19999", height=60, corner_radius=0)
        self.control_frame.grid(row=1, column=0, columnspan=2, sticky="ew")

        # Gom nhóm các widget vào giữa thanh control bằng một inner frame
        inner_control = ctk.CTkFrame(self.control_frame, fg_color="transparent")
        inner_control.pack(expand=True)

        ctk.CTkLabel(inner_control, text="Chọn Key tối ưu:", font=("Segoe UI", 12)).pack(side="left", padx=10)
        self.selected_key_entry = ctk.CTkEntry(inner_control, width=80, placeholder_text="ID...")
        self.selected_key_entry.pack(side="left", padx=5)

        self.btn_export = ctk.CTkButton(inner_control, text="📥 Tải xuống (.txt)", 
                                         command=self.export_to_txt, fg_color="#2c3e50",
                                         hover_color="#1a252f", width=150)
        self.btn_export.pack(side="left", padx=15)
        
    def log(self, message):
        # Hàm hỗ trợ ghi log an toàn từ Thread
        self.after(0, lambda: self._internal_log(message))

    def _internal_log(self, message):
        self.log_box.insert("end", f"> {message}\n")
        self.log_box.see("end")

    def start_attack_thread(self):
        # Khởi chạy luồng chính để không treo UI khi tính toán IC
        threading.Thread(target=self.execute_logic, daemon=True).start()

    def on_result_received(self, data):
        # Ghi nhận kết quả vào danh sách tổng để sau này sắp xếp Top 5
        self.collected_results.append(data)
        
        # 1. TẠO THÔNG TIN LOG CHI TIẾT
        key_info = f"Key {data['key']:02d}"
        preview = f"'{data['text'][:15]}...'"
        score_info = f"Score: {data['score']}"
        
        # Đánh giá trạng thái để chọn màu log
        # Giả sử điểm > 15 là có khớp từ điển (do chúng ta cộng 15 điểm ở Core)
        if data['score'] >= 15:
            status = "KHỚP TỪ ĐIỂN"
            tag = "highlight" # Màu đỏ
        elif data['score'] >= 3:
            status = "Khả thi"
            tag = "highlight" # Hoặc màu cam nếu bạn cấu hình thêm tag
        else:
            status = "Nhiễu"
            tag = "normal"    # Màu xanh

        log_line = f"> [{key_info}] {preview} | {score_info} | {status}\n"

        # 2. ĐẨY VÀO LOG NGAY LẬP TỨC (Real-time)
        self.after(0, lambda: self.log_box.insert("end", log_line, tag))
        self.after(0, lambda: self.log_box.see("end"))

    def execute_logic(self):
        ciphertext = self.input_text.get("1.0", "end-1c").strip()
        if not ciphertext: return

        # UI updates an toàn từ thread
        self.after(0, lambda: self.btn_attack.configure(state="disabled"))
        self.after(0, lambda: self.output_text.delete("1.0", "end"))
        
        self.collected_results = []
    
        t1 = threading.Thread(target=self.caesar_cracker.crack_range, 
                            args=(ciphertext, 1, 14, self.on_result_received))
        t2 = threading.Thread(target=self.caesar_cracker.crack_range, 
                            args=(ciphertext, 14, 27, self.on_result_received))
        
        t1.start()
        t2.start()
        
        # Đợi các luồng hoàn thành (Lúc này an toàn vì execute_logic đang chạy trong threading.Thread)
        t1.join()
        t2.join()
        
        self.collected_results.sort(key=lambda x: x['score'], reverse=True)
        self.after(0, self.display_final_output)

    def display_final_output(self):
        # Tiêu đề bảng
        header = f"{'HẠNG':<8} | {'KEY':<6} | {'ĐIỂM':<6} | {'NỘI DUNG GIẢI MÃ'}\n"
        self.output_text.insert("end", header)
        self.output_text.insert("end", " " + "="*85 + "\n\n")
        
        printed_count = 0
        last_score = -1
        max_results = 5 # Giới hạn cứng 5 kết quả đầu tiên

        for i, res in enumerate(self.collected_results):
            # Điều kiện dừng: 
            # Nếu đã in đủ 5 cái VÀ điểm của thằng hiện tại thấp hơn thằng trước đó
            if printed_count >= max_results and res['score'] < last_score:
                break
            
            # Chỉ in những kết quả có giá trị (Score > 0)
            if res['score'] > 0:
                # Tính toán hạng (nếu bằng điểm thì cùng hạng)
                if res['score'] != last_score:
                    rank_display = f"#{printed_count + 1}"
                else:
                    rank_display = f"#{printed_count}" # Hoặc dùng " -" để chỉ đồng hạng
                
                rank_display = f"#{printed_count + 1}"
                
                # Highlight đặc biệt cho các kết quả khớp từ điển (Score cao)
                is_reliable = " [TIN CẬY CAO]" if res['score'] > 15 else ""
                
                line = f"{rank_display:<8} | Key {res['key']:02d} | {res['score']:<6} | {res['text']}{is_reliable}\n"
                
                self.output_text.insert("end", line)
                self.output_text.insert("end", " " + "-"*85 + "\n\n")
                
                last_score = res['score']
                printed_count += 1

        if printed_count == 0:
            self.output_text.insert("end", ">>> Không tìm thấy kết quả khả thi nào trong 26 trường hợp.\n")
        else:
            self.log(f"Đã trích xuất {printed_count} kết quả tối ưu nhất.")
            
        self.btn_attack.configure(state="normal")
        # ui/attack_view.py (trong display_final_output)
    
    def import_input_file(self):
        from tkinter import filedialog
        import os
        file_path = filedialog.askopenfilename(filetypes=[("Text", "*.txt")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                self.input_text.delete("1.0", "end")
                self.input_text.insert("end", f.read())
            self.log(f"Đã nạp: {os.path.basename(file_path)}")

    def export_to_txt(self):
        from tkinter import filedialog
        import os

        # 1. Lấy Key từ ô nhập liệu
        try:
            key_val = int(self.selected_key_entry.get().strip())
        except ValueError:
            self.log("Lỗi: Vui lòng nhập số Key hợp lệ vào ô ID!")
            return

        # 2. Lấy bản mã gốc từ ô Input
        ciphertext = self.input_text.get("1.0", "end-1c").strip()
        if not ciphertext:
            self.log("Lỗi: Không có bản mã để giải mã!")
            return

        # 3. Thực hiện giải mã toàn bộ nội dung với Key đã chọn
        # Bạn có thể dùng hàm decrypt của CaesarCracker nếu có, 
        # hoặc viết nhanh logic ở đây:
        decrypted_text = ""
        for char in ciphertext:
            if char.isalpha():
                start = ord('A') if char.isupper() else ord('a')
                # Caesar decrypt: (x - k) % 26
                decrypted_text += chr((ord(char) - start - key_val) % 26 + start)
            else:
                decrypted_text += char

        # 4. Mở hộp thoại lưu file (Mô phỏng Download)
        f_path = filedialog.asksaveasfilename(
            defaultextension=".txt", 
            initialfile=f"decrypted_key_{key_val}.txt",
            filetypes=[("Text files", "*.txt")]
        )
        
        if f_path:
            try:
                with open(f_path, "w", encoding="utf-8") as f:
                    f.write(f"--- KẾT QUẢ GIẢI MÃ (KEY: {key_val}) ---\n\n")
                    f.write(decrypted_text)
                self.log(f"Đã xuất bản dịch Key {key_val} thành công!")
            except Exception as e:
                self.log(f"Lỗi khi lưu file: {e}")
    