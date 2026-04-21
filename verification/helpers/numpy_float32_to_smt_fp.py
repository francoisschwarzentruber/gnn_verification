import numpy as np
import struct

def numpy_float32_to_smt_fp(x: np.float32) -> str:
    x = np.float32(x)
    bits = struct.unpack('>I', struct.pack('>f', float(x)))[0]
    b = f"{bits:032b}"
    sign = b[0]
    exp = b[1:9]
    frac = b[9:]
    return f"(fp #b{sign} #b{exp} #b{frac})"

zero = np.float32(0.0)
one = np.float32(1.0)
print(numpy_float32_to_smt_fp(zero))
print(numpy_float32_to_smt_fp(one))