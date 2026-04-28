import streamlit as st
import os, io
# Giữ lại các core logic của bạn
from core.attack.vigenere_core import VigenereCracker

class AttackVigenere: # Phải có Class này
    def __init__(self, master, algo_name, master_app, **kwargs):
        self.master = master
        self.algo_name = algo_name
        self.master_app = master_app

    def render(self):
        # --- KHỞI TẠO CORE ---
        # Sử dụng st.cache_resource để không phải load lại class mỗi lần F5
        if 'vigenere_cracker' not in st.session_state:
            st.session_state.vigenere_cracker = VigenereCracker()
        
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
            
            input_ciphertext = st.text_area("Bản mã đầu vào (Ciphertext):", 
                                            value=default_text, 
                                            height=150)

            # ... (Phần input ciphertext giữ nguyên)

            # B. Action Button
            if st.button("⚡ START CRYPTANALYSIS", use_container_width=True, type="primary"):
                # --- BƯỚC QUAN TRỌNG: Xóa sạch dữ liệu cũ trong State ngay khi bấm ---
                st.session_state.collected_results = [] 
                # Nếu bạn có biến lưu logs riêng trong session_state, hãy reset nó ở đây luôn
                # st.session_state.system_logs = [] 
                
                self.execute_logic_st(input_ciphertext)
                st.rerun() # Buộc Streamlit vẽ lại giao diện để đảm bảo tính đồng bộ

            st.divider()

            # C. Output Section (Vùng này sẽ bị trống sau khi reset ở trên)
            output_container = st.empty() 
            with output_container.container():
                if st.session_state.collected_results:
                    self.display_final_output_st() 
                else:
                    st.info("Chưa có kết quả phân tích.")
        with right_col:
            st.markdown("### 🖥️ SYSTEM LOG")
            
            # --- PHẦN 1: TERMINAL LOG (Quá trình thám mã) ---
            log_content = "".join(st.session_state.logs) if st.session_state.logs else "Ready..."
            st.markdown(
                f"""
                <div style="
                    background-color: #000000; color: #00FF00; padding: 15px; 
                    border-radius: 5px; font-family: 'Courier New', monospace;
                    height: 350px; overflow-y: auto; border: 1px solid #333; 
                    font-size: 13px; white-space: pre-wrap; line-height: 1.5;
                ">
                    {log_content}
                </div>
                """,
                unsafe_allow_html=True
            )
            # --- PHẦN 2: BOX BAO TOÀN BỘ KẾT QUẢ (Có thanh cuộn) ---
            # Sử dụng st.container kết hợp với CSS để khống chế chiều cao
            # Chúng ta dùng "with" để bao toàn bộ expanders vào một khối
            # CSS để biến container này thành một box có scrollbar
            st.markdown("""
                <style>
                    .results-container {
                        background-color: #000000;
                        border: 1px solid #333;
                        border-radius: 5px;
                        padding: 10px;
                        height: 400px; /* Giới hạn chiều cao như bạn muốn */
                        overflow-y: auto;
                    }
                </style>
            """, unsafe_allow_html=True)

            # Bắt đầu container chứa các Expander
            # Lưu ý: Streamlit chưa hỗ trợ class trực tiếp cho container, 
            # nên ta sẽ dùng một thủ thuật bọc HTML xung quanh nếu cần, 
            # nhưng cách an toàn nhất cho widget là dùng st.container và CSS selector
            
            result_box = st.container(height=350) 
            with result_box:
                if st.session_state.collected_results:
                    for idx, res in enumerate(st.session_state.collected_results):
                        # --- LOGIC TÔ MÀU TỪ ON_RESULT_RECEIVED_ST ---
                        score = res['score']
                        if score >= 5000:
                            status, color, icon = "KHỚP MẠNH", "#FF3131", "🔴" 
                        elif score >= 1000:
                            status, color, icon = "KHẢ THI", "#D4A017", "🟡"
                        else:
                            status, color, icon = "NHIỄU", "#434B43", "⚪"

                        full_key = str(res['key'])
                        display_key = (full_key[:8] + "..") if len(full_key) > 10 else full_key
                        
                        # Tạo label có màu sắc sử dụng Markdown lồng trong Expander
                        # Streamlit cho phép dùng màu trong text bằng cách :color[text]
                        label = f"#{idx+1} | {icon} Key: {display_key} | Score: {score:.1f}"
                        
                        with st.expander(label):
                            # Hiển thị trạng thái màu mè bên trong
                            st.markdown(f"Trạng thái: <span style='color:{color}; font-weight:bold;'>{status}</span>", unsafe_allow_html=True)
                            
                            col1, col2 = st.columns(2)
                            col1.write(f"**Full Key:** `{full_key}`")
                            col2.write(f"**m:** {res.get('key_len', 'N/A')} | **IC:** {res.get('ic', 0):.4f}")
                            
                            st.divider()
                            st.write("**Bản giải mã thử:**")
                            st.code(res['text'], language="text")
                else:
                    st.info("Chưa có kết quả phân tích.")

            if st.button("Xóa Log & Dữ liệu", use_container_width=True):
                st.session_state.logs = []
                st.session_state.collected_results = []
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
               
    def on_result_received_st(self, data):
        pass
      

    def execute_logic_st(self, ciphertext):
        if not ciphertext: return
        
        # Reset dữ liệu cũ để tránh chồng chéo
        st.session_state.logs = []
        st.session_state.collected_results = []
        
        if 'core' not in st.session_state:
            st.session_state.core = VigenereCracker()

        def on_log_received(message):
            # Chỉ nhận tin nhắn văn bản thuần từ Core
            st.session_state.logs.append(message) 

        with st.spinner("🚀 Đang phân tích chuỗi lặp và thám mã..."):
            try:
                # 1. Gọi Core xử lý
                # Core sẽ tự động gọi on_log_received để ghi lại quá trình
                results = st.session_state.core.crack_vigenere(
                    ciphertext, 
                    self.handle_decrypt, 
                    log_callback=on_log_received
                )
                
                if not results:
                    on_log_received("\n[ERROR] ❌ Không tìm thấy cấu trúc lặp khả thi.")
                else:
                    # 2. Lưu kết quả vào state để Box hiển thị sử dụng
                    # Sắp xếp luôn tại đây
                    st.session_state.collected_results = sorted(
                        results, key=lambda x: x['score'], reverse=True
                    )
                    on_log_received(f"\n[SUCCESS] ✅ Tìm thấy {len(results)} ứng viên tiềm năng.")
                
            except Exception as e:
                on_log_received(f"\n[CRITICAL] ❌ Lỗi hệ thống: {str(e)}")

        # 3. Sau khi chạy xong, ép Streamlit cập nhật giao diện
        st.rerun()
        
    def handle_decrypt(self, method, ciphertext, key):
        if method == "Vigenère":
            key = key.upper()
            result = []
            key_index = 0 
            
            for char in ciphertext:
                if char.isalpha():
                    # Xác định viết hoa hay viết thường
                    start = ord('A') if char.isupper() else ord('a')
                    
                    # Vị trí ký tự Key (0-25)
                    k_char = key[key_index % len(key)]
                    k_val = ord(k_char) - ord('A')
                    
                    # Công thức giải mã: (C - K) mod 26
                    dec_char = chr((ord(char) - start - k_val) % 26 + start)
                    result.append(dec_char)
                    
                    # CHỈ TĂNG index khi gặp chữ cái
                    key_index += 1
                else:
                    # Giữ nguyên dấu cách, số, ký tự đặc biệt
                    result.append(char)
            return "".join(result)
    
    def display_final_output_st(self):
        # 1. Kiểm tra nếu chưa có kết quả thì thoát
        if not st.session_state.collected_results:
            return

        st.markdown("### 📋 Bảng xếp hạng ứng viên (Top Candidates)")
        
        # 2. Khởi tạo danh sách để chứa các dòng HTML
        output_lines = []
        
        # Header in đậm - Điều chỉnh padding để thẳng hàng với Key dạng String
        header = f"<b>{'HẠNG':<6} | {'KEY':<10} | {'ĐIỂM':<8} | {'NỘI DUNG GIẢI MÃ'}</b>"
        output_lines.append(header)
        output_lines.append("<hr style='margin: 5px 0; border: 0.5px solid #ddd;'>")

        # 3. Sắp xếp điểm cao nhất lên đầu (Dùng bản copy để không ảnh hưởng dữ liệu gốc nếu cần)
        sorted_results = sorted(st.session_state.collected_results, key=lambda x: x['score'], reverse=True)

        # Giới hạn hiển thị Top 20 để tránh lag UI
        for i, res in enumerate(sorted_results[:5]):
            rank = f"#{i + 1}"
            
            # Ngưỡng điểm của Vigenère thường cao hơn Caesar, nên điều chỉnh logic màu sắc
            if res['score'] >= 5000:
                color, status_icon = "#FF3131", "<b style='color: #FF3131;'> ✅</b>"
            elif res['score'] >= 1000:
                color, status_icon = "#D4A017", ""
            else:
                color, status_icon = "#555", ""

            # Hiển thị Key dạng chuỗi, cắt bớt nếu key quá dài (trường hợp m lớn)
            display_key = str(res['key'])
            if len(display_key) > 8:
                display_key = display_key[:6] + ".."

            # Cắt lấy preview văn bản
            text_preview = res['text'][:50].replace("\n", " ") + "..." if len(res['text']) > 50 else res['text']
            
            # Format dòng output (Sử dụng pre-wrap trong div nên cần căn lề cẩn thận)
            line = (
                f"<span style='color: {color};'>{rank:<6}</span> | "
                f"<b style='color: #2e7d32;'>{display_key:<10}</b> | "
                f"<b style='color: #1f538d;'>{res['score']:<8.1f}</b> | "
                f"<span>{text_preview}{status_icon}</span>"
            )
            
            output_lines.append(line)
            output_lines.append("<hr style='margin: 5px 0; border: 0.1px solid #eee;'>")

        # 4. Nối lại bằng thẻ xuống dòng
        final_content = "<br>".join(output_lines)

        # 5. Hiển thị vào box (Giữ nguyên style sáng của bạn để tương phản với Terminal Log)
        st.markdown(
            f"""
            <div style="
                background-color: #ffffff;
                color: #212529;
                padding: 15px;
                height: 400px;
                overflow-y: auto;
                overflow-x: hidden;
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
        # selected_key_val lúc này có thể là ID (số) hoặc trực tiếp là chuỗi Key (ví dụ: 'PYTHON')
        if not ciphertext or not selected_key_val:
            return None, "Vui lòng nhập Ciphertext và chọn/nhập Key!"

        try:
            # 1. Tìm chuỗi Key thực sự từ ID hoặc dùng trực tiếp nếu người dùng nhập chuỗi
            actual_key = ""
            
            # Nếu người dùng nhập số (ID từ bảng xếp hạng)
            if selected_key_val.isdigit():
                idx = int(selected_key_val) - 1 # Chuyển từ hạng #1, #2 về index 0, 1
                if 0 <= idx < len(st.session_state.collected_results):
                    # Sắp xếp lại để khớp với thứ tự hiển thị trên bảng xếp hạng
                    sorted_res = sorted(st.session_state.collected_results, key=lambda x: x['score'], reverse=True)
                    actual_key = sorted_res[idx]['key']
                else:
                    return None, f"Không tìm thấy Key ứng với hạng #{selected_key_val}!"
            else:
                # Nếu người dùng nhập trực tiếp chuỗi (ví dụ: 'HELLO')
                actual_key = selected_key_val.upper()

            # 2. Gọi hàm giải mã Vigenère từ master_app để xử lý văn bản
            # Chúng ta không nên viết lại logic giải mã tại đây để tránh sai sót
            decrypted_text = self.handle_decrypt("Vigenère", ciphertext, actual_key)
            
            # 3. Đóng gói nội dung file
            final_content = (
                f"--- KẾT QUẢ THÁM MÃ VIGENÈRE ---\n"
                f"KEY SỬ DỤNG: {actual_key}\n"
                f"THUẬT TOÁN: {self.algo_name}\n"
                f"---------------------------------\n\n"
                f"{decrypted_text}"
            )
            
            return final_content, None
            
        except Exception as e:
            return None, f"Lỗi khi trích xuất dữ liệu: {str(e)}"