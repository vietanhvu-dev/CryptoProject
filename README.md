# Cryptosystem Demo Tool - Project

Dự án mô phỏng và triển khai các hệ mật mã cổ điển và khóa công khai (Public-key Cryptography). Tập trung vào việc trực quan hóa các thuật toán phức tạp và phân tích các bài toán  nền tảng trong an toàn máy tính.

## Cấu trúc dự án (Project Structure)

Dự án được thiết kế theo mô hình Modular để dễ dàng mở rộng các hệ mật mới:

```text
├── app/                # Giao diện người dùng (CustomTkinter UI)
├── core/               # Lõi thuật toán (Logic xử lý chính)
│   ├── classical/      # Các hệ mật cổ điển (Caesar, Vigenère,...)
│   └── public_key/     # Hệ mật khóa công khai (RSA, ECC, NTRU,...)
├── utils/              # Thư viện toán học bổ trợ (Modular Arithmetic)
├── main.py             # Entry point của ứng dụng
└── requirements.txt    # Danh sách thư viện phụ thuộc
```

## Sử dụng
```
pip install -r requirements.txt
python main.py
```
