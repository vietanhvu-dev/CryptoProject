import customtkinter as ctk
import threading
from .cryptanalysis_core import CryptanalysisCore
from core.attack.caesar_core import CaesarCracker

class AttackView(ctk.CTkFrame):
    def __init__(self, master, algo_name, master_app, **kwargs):
        super().__init__(master, **kwargs)
        self.core = CryptanalysisCore()
        self.caesar_cracker = CaesarCracker()
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

        # Nút bấm gọi hàm điều phối thread
        self.btn_attack = ctk.CTkButton(left_panel, text="START ATTACK", 
                                       fg_color="#d9534f", command=self.start_attack_thread)
        self.btn_attack.pack(pady=10)

        self.output_text = ctk.CTkTextbox(left_panel, height=250)
        self.output_text.pack(fill="x", pady=10)

        # --- RIGHT PANEL (LOG) ---
        right_panel = ctk.CTkFrame(self, fg_color="#1a1a1a", corner_radius=15)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(0, 20), pady=20)
        
        self.log_box = ctk.CTkTextbox(right_panel, fg_color="black", text_color="#00FF00", font=("Consolas", 11))
        self.log_box.pack(fill="both", expand=True, padx=10, pady=10)
        self.log_box.tag_config("highlight", foreground="#FF0000") # Màu đỏ
        self.log_box.tag_config("normal", foreground="#00FF00")    # Màu xanh

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

        self.after(0, lambda: self.btn_attack.configure(state="disabled"))
        self.after(0, lambda: self.output_text.delete("1.0", "end"))
        
        # Danh sách tạm để gom kết quả từ các thread
        self.collected_results = []
    
        # Truyền self.on_result_received làm callback
        t1 = threading.Thread(target=self.caesar_cracker.crack_range, 
                            args=(ciphertext, 1, 14, self.on_result_received))
        t2 = threading.Thread(target=self.caesar_cracker.crack_range, 
                            args=(ciphertext, 14, 27, self.on_result_received))
        
        t1.start()
        t2.start()
        
        # Bắt buộc phải đợi 2 thread này xong thì mới hiện bảng kết quả cuối cùng
        t1.join()
        t2.join()
        
        # Sắp xếp lại danh sách theo Score cao nhất
        self.collected_results.sort(key=lambda x: x['score'], reverse=True)
        
        # Gọi hàm hiển thị Top 5 lên Output chính
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
