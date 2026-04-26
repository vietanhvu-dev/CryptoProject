import streamlit as st

class HomeView:
    def __init__(self, master=None, **kwargs):
        # Lưu trữ master nếu cần dùng sau này
        self.master = master

    def render(self):
        """
        Thay thế cho việc pack() vào container.
        Hàm này sẽ vẽ giao diện trực tiếp lên trình duyệt.
        """
        # Giả lập fg_color="#F1F3F5" và corner_radius bằng một div container
        st.markdown("""
            <style>
            .home-container {
                background-color: #F1F3F5;
                padding: 40px;
                border-radius: 20px;
                text-align: center;
            }
            .alice-bob-svg {
                margin-bottom: 20px;
            }
            </style>
        """, unsafe_allow_html=True)

        with st.container():
            # Sử dụng HTML/SVG để vẽ lại sơ đồ Alice & Bob thay cho Canvas
            # Điều này giúp giao diện sắc nét hơn trên mọi màn hình
            st.markdown(f"""
                <div class="home-container">
                    <svg width="500" height="250" viewBox="0 0 500 250" class="alice-bob-svg">
                        <circle cx="85" cy="115" r="35" fill="#1f538d" />
                        <text x="85" y="175" font-family="Segoe UI" font-size="14" font-weight="bold" fill="#1f538d" text-anchor="middle">Alice</text>
                        
                        <circle cx="415" cy="115" r="35" fill="#1f538d" />
                        <text x="415" y="175" font-family="Segoe UI" font-size="14" font-weight="bold" fill="#1f538d" text-anchor="middle">Bob</text>
                        
                        <defs>
                            <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="0" refY="3.5" orient="auto">
                                <polygon points="0 0, 10 3.5, 0 7" fill="#adb5bd" />
                            </marker>
                        </defs>
                        <line x1="130" y1="115" x2="360" y2="115" stroke="#adb5bd" stroke-width="3" marker-end="url(#arrowhead)" />
                        
                        <rect x="230" y="125" width="40" height="30" fill="#fcc419" />
                        <circle cx="250" cy="125" r="10" fill="none" stroke="#fcc419" stroke-width="3" />
                    </svg>
                </div>
            """, unsafe_allow_html=True)
# --- THÔNG TIN GIỚI THIỆU MỚI ---
            st.markdown("<h1 style='color: #1f538d; margin-top: 20px; margin-bottom: 0px;'>VŨ VIỆT ANH</h1>", unsafe_allow_html=True)
            st.markdown("<p style='color: #495057; font-size: 16px; font-weight: 500;'>Data Engineer | Cryptography Researcher</p>", unsafe_allow_html=True)
            
            st.divider()

            # Sử dụng cột để trình bày các đại ý cho gọn
            col_info1, col_info2 = st.columns(2)
            
            with col_info1:
                st.markdown("🎯 **Education Focus**")
                st.caption("Designed for academic research and learning classical ciphers.")
                
                st.markdown("⚖️ **License**")
                st.caption("Open-sourced under the **Apache License 2.0**.")

            with col_info2:
                st.markdown("🔐 **Privacy First**")
                st.caption("Zero data collection. Processing happens entirely in RAM.")
                
                st.markdown("⚠️ **Notice**")
                st.caption("Third-party cloud; avoid uploading sensitive personal data.")

            # Nút dẫn nhanh tới SECURITY.md (thay cho st.info cũ)
            st.markdown("---")
            st.markdown(
                """
                <div style="background-color: #f8f9fa; padding: 10px; border-left: 5px solid #1f538d; border-radius: 5px;">
                    <small style="color: #495057;">
                        For full terms, please visit our 
                        <a href="https://github.com/vietanhvu-dev/CryptoProject/blob/master/SECURITY.md" target="_blank" style="color: #1f538d; font-weight: bold; text-decoration: none;">
                            Security & Privacy Policy
                        </a>
                    </small>
                </div>
                """, 
                unsafe_allow_html=True
            )