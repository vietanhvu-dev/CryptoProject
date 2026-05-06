# D:\Project_Git\CryptoProject\utils\math_helpers.py
import math
import random

def is_prime(n):
    if n < 2:
        return False
    if n < 10000:
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    return miller_rabin(n)

def miller_rabin(n, k=5):  # k = số lần test (càng lớn càng chính xác)
    if n < 2:
        return False   
    # số chẵn > 2 không phải nguyên tố
    if n % 2 == 0:
        return n == 2
    # viết n-1 = d * 2^r
    r, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        r += 1   
    # test k lần
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False 
    return True

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    if a == 0: return b, 0, 1
    gcd_val, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd_val, x, y

def mod_inverse(e, phi):
    gcd_val, x, y = extended_gcd(e, phi)
    if gcd_val != 1: return None
    return x % phi