#Additional support functions for Z3 verification tasks
import re 
import numpy as np


def int_to_bv_hex(value: int, bit_width: int = 8) -> str:
    """
    Convert Python int to an SMT-LIB bit-vector literal of exactly `bit_width` bits.
    - Uses two's complement modulo 2^bit_width.
    - Uses #x... when bit_width is a multiple of 4 (nicer),
      otherwise uses #b... to get exact width.
    """
    if bit_width <= 0:
        raise ValueError("bit_width must be positive")

    # modulo 2^bit_width (wrap-around, like bit-vector arithmetic)
    mask = (1 << bit_width) - 1
    v_mod = value & mask

    if bit_width % 4 == 0:
        # hex: each digit = 4 bits
        hex_digits = bit_width // 4
        return f"#x{v_mod:0{hex_digits}x}"
    else:
        # binary: exactly bit_width bits
        return "#b" + format(v_mod, f"0{bit_width}b")    
    '''
    if value < 0:
        value = (1 << bit_width) + value

    hex_digits = (bit_width + 3) // 4  

    return f"#x{value:0{hex_digits}x}"
    '''

def bv_to_signed_int(bv: str, bit_width: int= 8) -> int:
    """
    Convert an SMT-LIB bit-vector literal (#x.. or #b..) into a signed Python int,
    assuming two's complement semantics with the given bit_width.

    This is the inverse of `int_to_bv_hex` in the sense that:
        v  ->  lit = int_to_bv_hex(v, bit_width)
        lit -> bv_to_signed_int(lit, bit_width)
    yields v modulo 2^bit_width, interpreted as signed.
    """
    if bit_width <= 0:
        raise ValueError("bit_width must be positive")

    if bv.startswith("#x"):
        # hex literal
        raw = bv[2:]
        value = int(raw, 16)
        # optional sanity check: width from hex length
        # inferred_width = 4 * len(raw)
        # assert inferred_width >= bit_width or inferred_width == bit_width
    elif bv.startswith("#b"):
        # binary literal
        raw = bv[2:]
        value = int(raw, 2)
        # inferred_width = len(raw)
        # assert inferred_width >= bit_width or inferred_width == bit_width
    else:
        raise ValueError(f"Unsupported bit-vector literal format: {bv}")

    # Now interpret `value` as signed two's-complement with `bit_width` bits
    sign_bit = 1 << (bit_width - 1)
    full_range = 1 << bit_width

    if value & sign_bit:
        # negative number
        return value - full_range
    else:
        # non-negative
        return value

def parse_var(var: str) -> str:
    var = var.strip()
    m = re.match(r"([A-Za-z_]\w*)\[(\d+)\]", var)
    if not m:
        raise ValueError(f"Invalid variable format: {var}")
    base, index = m.group(1), m.group(2)
    # encode as base_index to avoid ambiguity (x1[28] vs x12[8])
    return f"{base}_{index}"

def parse_atomic(expr: str,features,flag, bit_width: int = 8) -> str:
    expr = expr.strip()
    # check longer operators first
    for op in ["==", "!=", "<=", ">=", "<", ">"]:
        if op in expr:
            left, right = expr.split(op, 1)
            left = left.strip()
            right = right.strip()

            smt_var = parse_var(left)

            m = re.match(r"([A-Za-z_]\w*)_(\d+)$", smt_var)
            if not m:
                raise ValueError(f"Cannot parse SMT var: {smt_var}")
            base = m.group(1)


            if flag == "postcondition" and base not in features:
                raise ValueError("Cannot add a postcondition to a non-existing variable.")
            
            val_int = int(right)
            bv_val = int_to_bv_hex(val_int, bit_width)

            if op == "==":
                return f"(= {smt_var} {bv_val})"
            elif op == "!=":
                return f"(distinct {smt_var} {bv_val})"
            elif op == "<=":
                return f"(bvsle {smt_var} {bv_val})"
            elif op == ">=":
                return f"(bvsge {smt_var} {bv_val})"
            elif op == "<":
                return f"(bvslt {smt_var} {bv_val})"
            elif op == ">":
                return f"(bvsgt {smt_var} {bv_val})"


    raise ValueError(f"Unsupported atomic expression: {expr!r}")

def convert_condition_to_smt(expr: str,features,flag, bit_width: int = 8) -> str:
    """
    Convert a high-level condition in Python
    into a single SMT-LIB assert.
    Precedence: && is stronger than ||  (like in C).
    """
    # 1) Split by OR
    or_parts = [p.strip() for p in expr.split("||") if p.strip()]

    smt_or_clauses = []
    for part in or_parts:
        # 2) For each OR part, split by AND
        and_parts = [x.strip() for x in part.split("&&") if x.strip()]
        smt_and_clauses = [parse_atomic(p,features,flag, bit_width) for p in and_parts]

        if len(smt_and_clauses) == 1:
            smt_or_clauses.append(smt_and_clauses[0])
        else:
            smt_or_clauses.append(f"(and {' '.join(smt_and_clauses)})")

    # 3) Build the final assert
    if len(smt_or_clauses) == 1:
        if flag == 'postcondition':
            return f"(assert (not {smt_or_clauses[0]}))"
        return f"(assert {smt_or_clauses[0]})"
    else:
        if flag == 'postcondition':
            return f"(assert (not (or {' '.join(smt_or_clauses)})))"
        return f"(assert (or {' '.join(smt_or_clauses)}))"

def parse_get_value_output(output: str, bit_width: int) -> dict[str, int]:
    """
    Parse lines like:
      ((x1_0 #x01))
      ((a1_2 #b11111110))
    and return { "x1_0": 1, "a1_2": -2, ... }.
    """
    values: dict[str, int] = {}
    # Matches a line: ((var literal))
    pattern = re.compile(r"\(+\s*(\S+)\s+(#x[0-9A-Fa-f]+|#b[01]+)\s*\)+")

    
    for line in output.splitlines():
        m = pattern.match(line.strip())
        if not m:
            continue
        var, bv = m.group(1), m.group(2)
        values[var] = bv_to_signed_int(bv, bit_width)
        

    return values

