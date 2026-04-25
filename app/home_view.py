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

            # Thông tin cá nhân (Sử dụng CSS để đồng bộ màu sắc)
            st.markdown("<h1 style='color: #1f538d; margin-top: 20px;'>VŨ VIỆT ANH</h1>", unsafe_allow_html=True)
            st.markdown("<p style='color: #495057; font-size: 16px; font-weight: 500;'>Data Engineer | FPT Software</p>", unsafe_allow_html=True)
            
            st.divider()
            st.info("Ứng dụng hỗ trợ mã hóa, giải mã và thám mã các hệ mật mã cổ điển và hiện đại.")