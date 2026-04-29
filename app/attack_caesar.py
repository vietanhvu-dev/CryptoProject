import streamlit as st
import os, io
from core.attack.caesar_core import CaesarCracker

class AttackCaesar: # Phải có Class này
    def __init__(self, master, algo_name, master_app, **kwargs):
        self.master = master
        self.algo_name = algo_name
        self.master_app = master_app

    def render(self):
        # --- KHỞI TẠO CORE ---
        # Sử dụng st.cache_resource để không phải load lại class mỗi lần F5
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

        left_col, right_col = st.columns([3, 2])

        with left_col:
            # A. Input Section
            uploaded_file = st.file_uploader("📁 Upload Cipher File", type=['txt'])
            
            # Nếu có file upload, ưu tiên lấy nội dung file, không thì cho nhập tay
            default_text = ""
            if uploaded_file is not None:
                default_text = uploaded_file.read().decode("utf-8")
            
            input_ciphertext = st.text_area("📋 Bản mã đầu vào (Ciphertext):", 
                                            value=default_text, 
                                            height=150)

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
            st.markdown("### 🖥️ PROCESSOR LOG")
            
            # CHỈ CẦN DÒNG NÀY: Nối các chuỗi HTML đã có sẵn trong logs
            log_content = "".join(st.session_state.logs) if st.session_state.logs else "Ready..."
            
            st.markdown(
                f"""
                <div style="
                    background-color: #000000; color: #00FF00; padding: 15px; 
                    border-radius: 5px; font-family: 'Courier New', monospace;
                    height: 800px; overflow-y: auto; border: 1px solid #333; font-size: 13px;
                ">
                    {log_content}
                </div>
                """,
                unsafe_allow_html=True
            )
            # Nút xóa Log bên dưới
            st.write("") # Tạo khoảng cách nhỏ
            if st.button("Xóa Log & Dữ Liệu", use_container_width=True):
                st.session_state.logs = []
                st.session_state.current_result = ""
                st.rerun()
# --- BOTTOM CONTROL BAR ---
        st.divider()
        c1, c2, c3 = st.columns([1, 1, 1])

        with c1:
            # Mục 1: Chọn key tối ưu
            selected_key = st.text_input(
                label="🔑 Chọn Key tối ưu (ID):", 
                placeholder="Ví dụ: 3"
            )

        # Xử lý logic bóc tách dữ liệu
        result = self.handle_export_st(input_ciphertext, selected_key)
        final_content = result[0] 
        error_msg = result[1]

        with c2:
            # Mục 2: Nhãn "Tải xuống" để đều với cột 1
            st.markdown("<label style='font-size: 14px; font-weight: 400;'>💾 Xuất file:</label>", unsafe_allow_html=True)
            
            if final_content:
                st.download_button(
                    label="📄 Tải xuống (.txt)",
                    data=str(final_content),
                    file_name=f"cryptanalysis_{self.algo_name}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            else:
                st.button("📄 Tải xuống (.txt)", disabled=True, use_container_width=True)

        with c3:
            # Mục 3: Nhãn "Thông báo" để đều với cột 1
            st.markdown("<label style='font-size: 14px; font-weight: 400;'>🔔 Trạng thái:</label>", unsafe_allow_html=True)
            
            if not selected_key:
                st.info("ℹ️ Nhập Key để xuất")
            elif error_msg:
                st.error(f"❌ {error_msg}")
            else:
                st.success("✅ Sẵn sàng!")
               
    # Giả định hàm on_result_received_st để gom kết quả
    def on_result_received_st(self, data):
        if "collected_results" in st.session_state:
            st.session_state.collected_results.append(data)
        
        # 1. Xác định trạng thái và màu sắc
        status = "KHỚP TỪ ĐIỂN" if data['score'] >= 15 else "Khả thi" if data['score'] >= 3 else "Nhiễu"
        color = "#FF3131" if data['score'] >= 15 else "#D4A017" if data['score'] >= 3 else "#1CCE1C"
        
        # 2. Xử lý nội dung văn bản: Thay thế các dấu xuống dòng bằng <br> để HTML hiểu
        full_text_html = data['text'].replace("\n", "<br>")
        
        # 3. Sử dụng cấu trúc HTML <details> để tạo hiệu ứng "Mở rộng"
        # Summary là phần hiển thị ngắn gọn, nội dung bên trong là phần khi bấm vào mới hiện ra
        log_line = f"""
        <details style="margin-bottom: 5px; border-bottom: 1px solid #333;">
            <summary style="cursor: pointer; list-style: none; outline: none;">
                <span style="color: #00FF00;">[Key {data['key']}]</span> 
                "{data['text'][:15]}..." | 
                <span style="color: #00FFFF;">Score: {data['score']}</span> | 
                <span style="color: {color}; font-weight: bold;">{status}</span>
                <span style="color: #666; font-size: 10px; margin-left: 10px;">(Xem thêm >>)</span>
            </summary>
            <div style="
                margin-top: 5px; 
                padding: 10px; 
                background-color: #252525; 
                border-left: 3px solid {color};
                color: #e0e0e0;
                font-family: monospace;
            ">
                <b>Nội dung đầy đủ:</b><br>
                {full_text_html}
            </div>
        </details>
        """
        
        st.session_state.logs.append(log_line)

    def execute_logic_st(self, ciphertext):
        if not ciphertext:
            return

        # 1. Reset kết quả
        st.session_state.collected_results = []
        
        # 2. Thống nhất logs là list các CHUỖI (String)
        st.session_state.logs = ["<span style='color: #5bc0de;'>[INFO] > Bắt đầu phân tích hệ mật Caesar...</span>"]
        
        with st.spinner("🚀 Đang thực hiện phá mã (Cryptanalysis)..."):
            # Gọi core logic - Các hàm này sẽ gọi on_result_received_st
            # Hãy đảm bảo on_result_received_st cũng đẩy vào logs dạng STRING
            st.session_state.caesar_cracker.crack_range(ciphertext, 1, 14, self.on_result_received_st)
            st.session_state.caesar_cracker.crack_range(ciphertext, 14, 27, self.on_result_received_st)
            
            # 3. Sắp xếp kết quả chính
            st.session_state.collected_results.sort(key=lambda x: x['score'], reverse=True)
            
            # 4. Thêm dòng kết thúc dạng STRING
            st.session_state.logs.append("<span style='color: #5cb85c;'>[SUCCESS] ✅ Đã hoàn tất trích xuất 26 trường hợp.</span>")

        # 5. Rerun để cập nhật UI
        st.rerun()
        

    def display_final_output_st(self):
        # 1. Kiểm tra nếu chưa có kết quả thì thoát
        if not st.session_state.collected_results:
            return

        st.markdown("### 📋 Kết quả trích xuất (Top Candidates)")
        
        # 2. Khởi tạo danh sách để chứa các dòng HTML
        output_lines = []
        
        # Header in đậm (Style chuyên nghiệp)
        header = f"<b>{'HẠNG':<8} | {'KEY':<6} | {'ĐIỂM':<6} | {'NỘI DUNG GIẢI MÃ'}</b>"
        output_lines.append(header)
        output_lines.append("<hr style='margin: 5px 0; border: 0.5px solid #ddd;'>")

        # 3. QUAN TRỌNG: Lặp qua collected_results (List các Dictionary gốc)
        # Sắp xếp điểm cao nhất lên đầu
        sorted_results = sorted(st.session_state.collected_results, key=lambda x: x['score'], reverse=True)[:7]

        for i, res in enumerate(sorted_results):
            rank = f"#{i + 1}"
            
            # Xác định màu sắc dựa trên score
            color = "#FF3131" if res['score'] >= 15 else "#D4A017" if res['score'] >= 3 else "#555"
            is_reliable = f" <b style='color: #FF3131;'>✅ </b>" if res['score'] >= 15 else ""

           # Cắt lấy 15 ký tự đầu tiên và thêm dấu ... để biết là còn tiếp
            text_preview = res['text'][:40] + ".." if len(res['text']) > 15 else res['text']
            
            line = (
                f"<b style='color: {color};'>{rank:<8}</b> | "
                f"<b>Key {res['key']}</b> | "
                f"<b style='color: #1f538d;'>{res['score']:<6}</b> | "
                f"{text_preview}{is_reliable}"
            )
            
            output_lines.append(line)
            output_lines.append("<hr style='margin: 5px 0; border: 0.1px solid #eee;'>")

        # 4. Nối lại bằng thẻ xuống dòng HTML
        final_content = "<br>".join(output_lines)

        # 5. Hiển thị vào box cố định chiều ngang, cuộn dọc
        st.markdown(
            f"""
            <div style="
                background-color: #ffffff;
                color: #212529;
                padding: 15px;
                height: 500px;
                overflow-y: auto;
                overflow-x: hidden;
                white-space: pre-wrap; 
                border-radius: 10px;
                border: 1px solid #dee2e6;
                font-family: 'Courier New', Courier, monospace;
                font-size: 13px;
                line-height: 1.8;
            ">
                {final_content}
            </div>
            """,
            unsafe_allow_html=True
        )

    def handle_export_st(self, ciphertext, selected_key_val):
        # Trường hợp chưa nhập gì: không coi là lỗi, chỉ là chưa sẵn sàng
        if not ciphertext or selected_key_val == "":
            return None, "Vui lòng nhập Ciphertext và chọn Key ID!"

        try:
            key_val = int(selected_key_val)
            decrypted_text = ""
            for char in ciphertext:
                if char.isalpha():
                    start = ord('A') if char.isupper() else ord('a')
                    decrypted_text += chr((ord(char) - start - key_val) % 26 + start)
                else:
                    decrypted_text += char
            
            final_content = f"--- KẾT QUẢ GIẢI MÃ (KEY: {key_val}) ---\n\n{decrypted_text}"
            return final_content, None # Thành công, không có lỗi
            
        except ValueError:
            return None, "Key ID phải là một con số!"