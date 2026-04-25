import streamlit as st
import os, io
# Giữ lại các core logic của bạn
from .cryptanalysis_core import CryptanalysisCore
from core.attack.caesar_core import CaesarCracker

class AttackView: # Phải có Class này
    def __init__(self, master, algo_name, master_app, **kwargs):
        self.master = master
        self.algo_name = algo_name
        self.master_app = master_app

    def render(self):
        # --- KHỞI TẠO CORE ---
        # Sử dụng st.cache_resource để không phải load lại class mỗi lần F5
        if 'core' not in st.session_state:
            st.session_state.core = CryptanalysisCore()
        if 'caesar_cracker' not in st.session_state:
            st.session_state.caesar_cracker = CaesarCracker()
        
        # Biến lưu trữ kết quả tạm thời
        if 'collected_results' not in st.session_state:
            st.session_state.collected_results = []
        if 'logs' not in st.session_state:
            st.session_state.logs = []

        # --- UI HEADER ---
        st.markdown(
            f"<h1 style='color: #d9534f; margin-bottom: 0px; padding-bottom: 0px;'>📊 PHÂN TÍCH: {self.algo_name.upper()}</h1>", 
            unsafe_allow_html=True
        )

        left_col, right_col = st.columns([2, 2])

        with left_col:
            # A. Input Section
            uploaded_file = st.file_uploader("📁 Upload Cipher File", type=['txt'])
            
            # Nếu có file upload, ưu tiên lấy nội dung file, không thì cho nhập tay
            default_text = ""
            if uploaded_file is not None:
                default_text = uploaded_file.read().decode("utf-8")
            
            input_ciphertext = st.text_area("Bản mã đầu vào (Ciphertext):", 
                                            value=default_text, 
                                            height=150)
            st.write(f"Dữ liệu nhận được: {input_ciphertext}")

            # B. Action Button
            if st.button("⚡ START CRYPTANALYSIS", use_container_width=True, type="primary"):
               self.execute_logic_st(input_ciphertext)
               st.divider()

            # C. Output Section
            if st.session_state.collected_results:
                self.display_final_output_st() 
            else:
                st.info("Chưa có kết quả phân tích.")
        with right_col:
            st.markdown("### 🖥️ SYSTEM LOG")
            log_content = "\n".join(st.session_state.logs) if st.session_state.logs else "Ready..."
            
            # Sử dụng Markdown với HTML/CSS để đổi màu
            st.markdown(
                f"""
                <div style="
                    background-color: #000000; 
                    color: #00FF00; 
                    padding: 10px; 
                    border-radius: 5px; 
                    font-family: 'Courier New', Courier, monospace;
                    height: 400px;
                    overflow-y: auto;
                    white-space: pre-wrap;
                    border: 1px solid #333;
                ">
                {log_content}
                </div>
                """,
                unsafe_allow_html=True
            )

        # --- BOTTOM CONTROL BAR ---
        st.divider()
        c1, c2, c3 = st.columns([2, 2, 2])
        
        with c1:
            selected_key = st.text_input("🔑 Chọn Key tối ưu (ID):", placeholder="Ví dụ: 3")
        
        with c2:
            # 1. Lấy dữ liệu xuất (hàm này có thể trả về None)
            final_output = self.handle_export_st(input_ciphertext, selected_key)
            
            # 2. CHỈ hiển thị nút download nếu có dữ liệu
            if final_output is not None:
                st.download_button(
                    label="📥 Tải xuống (.txt)",
                    data=final_output,
                    file_name=f"cryptanalysis_{self.algo_name}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            else:
                # Nếu chưa có dữ liệu, hiển thị nút bị vô hiệu hóa để tránh lỗi
                st.info("Nhập Key để xuất file")

    # Giả định hàm on_result_received_st để gom kết quả
    def on_result_received_st(self, data):
        if "collected_results" in st.session_state:
             st.session_state.collected_results.append(data)
        # Tạo dòng log tương tự bản cũ
        status = "KHỚP TỪ ĐIỂN" if data['score'] >= 15 else "Khả thi" if data['score'] >= 3 else "Nhiễu"
        log_line = f"> [Key {data['key']:02d}] {data['text'][:15]}... | Score: {data['score']} | {status}"
        st.session_state.logs.append(log_line)

    def execute_logic_st(self, ciphertext):
        if not ciphertext:
            return

        # Reset kết quả
        st.session_state.collected_results = []
        st.session_state.logs = ["> Bắt đầu phân tích..."]
        
        # Thực hiện crack (Thay vì dùng thread, gọi trực tiếp tuần tự hoặc xử lý mảng)
        with st.spinner("🚀 Đang thực hiện phá mã (Cryptanalysis)..."):
            # Gọi trực tiếp core logic của bạn
            st.session_state.caesar_cracker.crack_range(ciphertext, 1, 14, self.on_result_received_st)
            st.session_state.caesar_cracker.crack_range(ciphertext, 14, 27, self.on_result_received_st)
            # Sắp xếp kết quả theo Score giảm dần
            st.session_state.collected_results.sort(key=lambda x: x['score'], reverse=True)
            st.session_state.logs.append(f"Đã hoàn tất trích xuất kết quả.")

        st.rerun()  # Cập nhật UI sau khi có kết quả mới
    def display_final_output_st(self):
        if not st.session_state.collected_results:
            return

        st.markdown("### 📋 Kết quả trích xuất (Top Candidates)")
        
        # Tạo header cho bảng giả lập giống giao diện cũ
        output_lines = []
        header = f"{'HẠNG':<8} | {'KEY':<6} | {'ĐIỂM':<6} | {'NỘI DUNG GIẢI MÃ'}"
        output_lines.append(header)
        output_lines.append("-" * 85)

        printed_count = 0
        last_score = -1
        max_results = 5

        for res in st.session_state.collected_results:
            if printed_count >= max_results and res['score'] < last_score:
                break
            
            if res['score'] > 0:
                rank = f"#{printed_count + 1}"
                is_reliable = " ✅ [TIN CẬY CAO]" if res['score'] > 15 else ""
                line = f"{rank:<8} | Key {res['key']:02d} | {res['score']:<6} | {res['text']}{is_reliable}"
                output_lines.append(line)
                output_lines.append("-" * 85)
                
                last_score = res['score']
                printed_count += 1

        if printed_count == 0:
            st.error(">>> Không tìm thấy kết quả khả thi nào trong 26 trường hợp.")
        else:
            # Hiển thị toàn bộ bảng trong một vùng code cho đẹp
            st.code("\n".join(output_lines), language="text")

    def handle_export_st(self, ciphertext, selected_key_val):
        if not ciphertext or selected_key_val == "":
            st.error("Vui lòng nhập Ciphertext và chọn Key ID!")
            return None

        try:
            key_val = int(selected_key_val)
            decrypted_text = ""
            for char in ciphertext:
                if char.isalpha():
                    start = ord('A') if char.isupper() else ord('a')
                    decrypted_text += chr((ord(char) - start - key_val) % 26 + start)
                else:
                    decrypted_text += char
            
            # Chuẩn bị file nội dung để tải về (thay thế filedialog.asksaveasfilename)
            final_content = f"--- KẾT QUẢ GIẢI MÃ (KEY: {key_val}) ---\n\n{decrypted_text}"
            return final_content
        except ValueError:
            st.error("Key ID phải là một con số!")
            return None