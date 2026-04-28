import math
import random

def gcd(a, b):
    """
    Tìm ước chung lớn nhất (Greatest Common Divisor).
    Sử dụng thuật toán Euclid cơ bản.
    """
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    """
    Thuật toán Euclid mở rộng.
    Trả về (gcd, x, y) sao cho: a*x + b*y = gcd(a, b)
    Dùng để tìm nghịch đảo modulo trong RSA.
    """
    if a == 0:
        return b, 0, 1
    gcd_val, x1, y1 = extended_gcd(b % a, a)
    
    x = y1 - (b // a) * x1
    y = x1
    
    return gcd_val, x, y

def mod_inverse(e, phi):
    """
    Tìm số d (Private Key) sao cho: (d * e) % phi == 1
    Sử dụng kết quả từ thuật toán Euclid mở rộng.
    """
    gcd_val, x, y = extended_gcd(e, phi)
    if gcd_val != 1:
        raise ValueError("Nghịch đảo modulo không tồn tại (e và phi không nguyên tố cùng nhau)!")
    else:
        # Đảm bảo kết quả là số dương
        return x % phi

def is_prime(n):
    """
    Kiểm tra số nguyên tố theo phương pháp chia thử
    """
    # 1. Các trường hợp cơ sở
    if n <= 1:
        return False
    if n <= 3:
        return True # Số 2 và 3 là số nguyên tố
    
    # 2. Loại bỏ các số chẵn và bội số của 3 nhanh chóng
    if n % 2 == 0 or n % 3 == 0:
        return False
    
    # 3. Kiểm tra các số từ 5 trở đi
    # Sử dụng quy luật: mọi số nguyên tố (trừ 2, 3) đều có dạng 6k ± 1
    # Chỉ cần kiểm tra đến căn bậc hai của n để tối ưu hiệu suất
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
        
    return True

def modular_exponentiation(base, exp, mod):
    """
    Tính lũy thừa bậc lớn: (base^exp) % mod
    Mặc dù Python có sẵn hàm pow(base, exp, mod) cực nhanh
    """
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result
