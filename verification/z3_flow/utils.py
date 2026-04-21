#Additional support functions for Z3 verification tasks
import re 
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

def parse_var(var: str) -> str:
    var = var.strip()
    m = re.match(r"([A-Za-z_]\w*)\[(\d+)\]", var)
    if not m:
        raise ValueError(f"Invalid variable format: {var}")
    base, index = m.group(1), m.group(2)
    # encode as base_index to avoid ambiguity (x1[28] vs x12[8])
    return f"{base}_{index}"

def parse_atomic(expr: str, features, flag,
                 default_dtype: str = "Float32",
                 int_features=None) -> str:
    expr = expr.strip()
    if int_features is None:
        int_features = []

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

            # choose actual dtype
            if base in int_features:
                dtype = "Int"
            else:
                dtype = default_dtype

            # encode right-hand side constant
            if dtype == "Float32":
                smt_val = numpy_float32_to_smt_fp(np.float32(right))
            elif dtype == "Real":
                smt_val = format(np.float32(right), ".9g")
            elif dtype == "Int":
                smt_val = str(int(float(right)))
            else:
                raise ValueError(f"Unsupported dtype: {dtype}")

            # equality / disequality
            if op == "==":
                return f"(= {smt_var} {smt_val})"
            elif op == "!=":
                return f"(distinct {smt_var} {smt_val})"

            # order comparisons
            if dtype == "Float32":
                if op == "<=":
                    return f"(fp.leq {smt_var} {smt_val})"
                elif op == ">=":
                    return f"(fp.geq {smt_var} {smt_val})"
                elif op == "<":
                    return f"(fp.lt {smt_var} {smt_val})"
                elif op == ">":
                    return f"(fp.gt {smt_var} {smt_val})"

            elif dtype in ["Real", "Int"]:
                return f"({op} {smt_var} {smt_val})"

    raise ValueError(f"Unsupported atomic expression: {expr!r}")

def convert_condition_to_smt(expr: str, features, flag,
                             default_dtype: str = "Float32",
                             int_features=None) -> str:
    if int_features is None:
        int_features = []

    or_parts = [p.strip() for p in expr.split("||") if p.strip()]

    smt_or_clauses = []
    for part in or_parts:
        and_parts = [x.strip() for x in part.split("&&") if x.strip()]
        smt_and_clauses = [
            parse_atomic(p, features, flag, default_dtype, int_features)
            for p in and_parts
        ]

        if len(smt_and_clauses) == 1:
            smt_or_clauses.append(smt_and_clauses[0])
        else:
            smt_or_clauses.append(f"(and {' '.join(smt_and_clauses)})")

    if len(smt_or_clauses) == 1:
        if flag == "postcondition":
            return f"(assert (not {smt_or_clauses[0]}))"
        return f"(assert {smt_or_clauses[0]})"
    else:
        if flag == "postcondition":
            return f"(assert (not (or {' '.join(smt_or_clauses)})))"
        return f"(assert (or {' '.join(smt_or_clauses)}))"
    

def build_add_chain(vars_list):
    """
    Build SMT addition:
    (+ x0_0 x0_1 x0_2)
    """
    if not vars_list:
        raise ValueError("vars_list cannot be empty")
    if len(vars_list) == 1:
        return vars_list[0]
    return f"(+ {' '.join(vars_list)})"


def build_fp_add_chain(vars_list, rounding="RNE"):
    """
    Build nested floating-point addition:
    (fp.add RNE x0_0 (fp.add RNE x0_1 x0_2))
    """
    if not vars_list:
        raise ValueError("vars_list cannot be empty")
    if len(vars_list) == 1:
        return vars_list[0]

    expr = vars_list[-1]
    for v in reversed(vars_list[:-1]):
        expr = f"(fp.add {rounding} {v} {expr})"
    return expr