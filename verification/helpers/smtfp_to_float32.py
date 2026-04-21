import struct

def z3_fp_to_float32(sign, exponent_hex, fraction_bin):
    sign_bit = sign
    exp_bits = format(int(exponent_hex, 16), '08b')
    frac_bits = fraction_bin

    full_bits = sign_bit + exp_bits + frac_bits
    int_val = int(full_bits, 2)

    return struct.unpack('>f', struct.pack('>I', int_val))[0]

# Example
v = z3_fp_to_float32(
    sign='1',
    exponent_hex='7e',
    fraction_bin='01011101000011110001011'
)

w = z3_fp_to_float32(
    sign='1',
    exponent_hex='7b',
    fraction_bin='10001111000101001000100'
)

print('f22_1v:', v)  # 1.0
print('f19_0w:', w)  # 1.0