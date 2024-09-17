import ctypes

# Tente carregar a biblioteca do sistema
try:
    libc = ctypes.CDLL("msvcrt.dll")  # Use msvcrt.dll para Windows
except Exception as e:
    print(f"Erro ao carregar libc: {e}")
