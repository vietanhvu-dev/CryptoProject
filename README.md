# Cryptosystem Demo Tool - Project

Dự án mô phỏng và triển khai các hệ mật mã cổ điển và khóa công khai (Public-key Cryptography). Tập trung vào việc trực quan hóa các thuật toán phức tạp và phân tích các bài toán  nền tảng trong an toàn máy tính.

## Cấu trúc dự án (Project Structure)

Dự án được thiết kế theo mô hình Modular để dễ dàng mở rộng các hệ mật mới:

```text
D:.
|   .gitignore
|   main.py                 # Entry point của ứng dụng
|   README.md               # Tài liệu dự án
|   requirements.txt        # Danh sách thư viện (customtkinter, etc.)
|   
+---app                     # Tầng Giao diện (Presentation Layer)
|       attack_view.py      # Logic thám mã & giao diện tấn công
|       crypto_view.py      # Giao diện mã hóa/giải mã thông thường
|       gui.py              # Điều phối giao diện chính (Main Navigation)
|       home_view.py        # Dashboard giới thiệu dự án
|       __init__.py
|       
+---core                    # Tầng Xử lý lõi (Business Logic Layer)
|   |   base.py             # Class cơ sở cho các thuật toán
|   |   __init__.py
|   |   
|   +---classical           # Các hệ mật cổ điển (Caesar, Vigenère, ...)
|   |       __init__.py
|   |       
|   \---public_key          # Các hệ mật khóa công khai (RSA, ...)
|           __init__.py
|           
\---utils                   # Các công cụ hỗ trợ (Helper)
        math_helper.py      # Các hàm toán học (Tính IC, GCD, Modulo...)
        __init__.py
```

## Sử dụng
```
pip install -r requirements.txt
python main.py
```
