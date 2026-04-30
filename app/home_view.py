import streamlit as st

class HomeView:
    def __init__(self, master=None, **kwargs):
        # Lưu trữ master nếu cần dùng sau này
        self.master = master

    def render(self):
        """
        Giao diện Home tập trung vào tính thẩm mỹ và thông tin tổng quan.
        Sử dụng Expander để tổ chức các Module thông tin.
        """
        # --- STYLE & CSS ---
        st.markdown("""
            <style>
            .home-container {
                background-color: #F1F3F5;
                padding: 30px;
                border-radius: 15px;
                text-align: center;
                margin-bottom: 20px;
            }
            .module-card {
                padding: 10px;
                border-radius: 10px;
                border: 1px solid #e6e9ef;
                margin-bottom: 10px;
            }
            </style>
        """, unsafe_allow_html=True)


    
        # --- HEADER SECTION (SVG & BRANDING) ---
        with st.container():
            st.markdown(f"""
                <div class="home-container">
                    <h1 style='color: #1f538d; margin-top: 10px;'>CRYPTO SYSTEM DEMO PLATFORM</h1>
                    <p style='color: #495057; font-size: 1.1rem;'>Vũ Việt Anh | Trần Sỹ Toàn</p>
                </div>
            """, unsafe_allow_html=True)


        st.subheader("Cryptography Modules")

        # --- MODULE 1: CAESAR CIPHER ---
        with st.expander("🔑 **1. Caesar Cipher (Mật mã Caesar)**"):
            st.info("**Category:** Symmetric Encryption / Substitution Cipher")
            st.markdown("""
            **Cách hoạt động:**
            Mỗi ký tự trong văn bản gốc (Plaintext) sẽ được thay thế bằng một ký tự khác nằm cách nó một khoảng $k$ vị trí trong bảng chữ cái.
            * **Encryption:** $E(x) = (x + k) \mod 26$
            * **Decryption:** $D(x) = (x - k) \mod 26$
            """)
            st.markdown('<div class="how-it-works"><b>Ví dụ:</b> Với k=3, "A" trở thành "D", "B" trở thành "E".</div>', unsafe_allow_html=True)

        # --- MODULE 2: VIGENERE CIPHER ---
        with st.expander("🔑 **2. Vigenère Cipher (Mật mã Vigenère)**"):
            st.info("**Category:** Polyalphabetic Substitution")
            st.markdown("""
            **Cách hoạt động:**
            Sử dụng một từ khóa (Key) để thay đổi khoảng cách dịch chuyển cho từng ký tự, thay vì dùng một số cố định như Caesar.
            1. Lặp lại từ khóa sao cho chiều dài bằng với văn bản gốc.
            2. Cộng giá trị của từng cặp ký tự tương ứng từ văn bản gốc và từ khóa.
            * **Formula:** $C_i = (P_i + K_i) \mod 26$
            """)
            st.markdown('<div class="how-it-works"><b>Ưu điểm:</b> Chống lại việc thám mã dựa trên tần suất chữ cái đơn giản.</div>', unsafe_allow_html=True)

        # --- MODULE 3: RSA ALGORITHM ---
        with st.expander("🔑 **3. RSA Algorithm (Hệ mật mã khóa công khai)**"):
            st.info("**Category:** Asymmetric Encryption")
            st.markdown("""
            **Cách hoạt động:**
            Dựa trên độ khó của việc phân tích một số nguyên cực lớn thành các thừa số nguyên tố.
            1. **Key Generation:** Chọn 2 số nguyên tố lớn $p, q$, tính $n = p \times q$.
            2. **Public Key (e, n):** Dùng để mã hóa, có thể chia sẻ rộng rãi.
            3. **Private Key (d, n):** Dùng để giải mã, được giữ bí mật tuyệt đối.
            * **Encryption:** $C = M^e \mod n$
            * **Decryption:** $M = C^d \mod n$
            """)

        # --- MODULE 4: CAESAR CRYPTANALYSIS ---
        with st.expander("🔍 **4. Caesar Cryptanalysis (Thám mã Caesar)**"):
            st.info("**Method:** Brute Force & Frequency Analysis")
            st.markdown("""
            **Cách hoạt động:**
            Vì Caesar chỉ có 26 khả năng dịch chuyển (Key $k$ từ 1-26), chúng ta có thể phá giải bằng:
            * **Brute Force:** Thử lần lượt tất cả 26 khóa cho đến khi tìm thấy văn bản có nghĩa.
            * **Frequency Analysis: (Not Implemented)** Phân tích tần suất các chữ cái xuất hiện (ví dụ trong tiếng Anh, chữ 'E' thường xuất hiện nhiều nhất) để dự đoán khóa $k$.
            """)

        # --- MODULE 5: VIGENERE CRYPTANALYSIS ---
        with st.expander("🔍 **5. Vigenère Cryptanalysis (Thám mã Vigenère)**"):
            st.info("**Method:** Kasiski Examination / Friedman Test")
            st.markdown("""
            **Cách hoạt động:**
            Phức tạp hơn Caesar vì mỗi chữ cái có thể được mã hóa bởi các khóa khác nhau.
            1. **Tìm độ dài khóa (m):** Tìm các chuỗi ký tự lặp lại trong bản mã để dự đoán chiều dài của từ khóa.
            2. **Tách nhóm:** Chia bản mã thành $m$ nhóm. Mỗi nhóm bây giờ thực chất là một hệ mật mã Caesar đơn giản.
            3. **Phá giải:** Dùng Frequency Analysis trên từng nhóm để tìm ra từng chữ cái của từ khóa.
            """)

        # --- MAIN INFO EXPANDER ---
        with st.expander("ℹ️ **About this Project & Security**", expanded=True):
            col_info1, col_info2 = st.columns(2)
            with col_info1:
                st.markdown("🎯 **Education Focus**")
                st.caption("Designed for academic research and learning classical ciphers.")
                st.markdown("⚖️ **License**")
                st.caption("Open-sourced under the **Apache License 2.0**.")
            with col_info2:
                st.markdown("⚠️ **Privacy First**")
                st.caption("Zero data collection. Processing happens entirely in RAM.")
                st.markdown("🤖 **Notice**")
                st.caption("Third-party cloud; avoid uploading sensitive personal data.")
            
            st.markdown(
                """
                <div style="background-color: #f8f9fa; padding: 10px; border-left: 5px solid #1f538d; border-radius: 5px; margin-top: 10px;">
                    <small>For full terms, visit <a href="https://github.com/" target="_blank">Security Policy</a></small>
                </div>
                """, unsafe_allow_html=True)


        st.divider()
        st.caption("© 2026 Vũ Việt Anh & Contributors - Built with Streamlit")