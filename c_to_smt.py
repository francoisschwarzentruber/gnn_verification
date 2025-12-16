"""
Vibe-coded with GPT-5.
"""

import re
import math

def _hexa(val, num_bits):
    if (val >= 0):
        return '#' + f"{val:#0{2+math.ceil(math.log(2**num_bits, 16))}x}"[1:]
    else: # not sure this will work smoothly...
        return '(bvsge #' + f"{-val:#0{2+math.ceil(math.log(2**num_bits, 16))}x}"[1:] + ')'
    

def c_to_smt(expr, num_bits):
    # convert array indexing: x[3] → xz3
    expr = re.sub(r'([A-Za-z_]\w*)\[(\d+)\]', r'\1z\2', expr)

    # tokenize
    token_pattern = r"""
        <=|>=|==|!=|&&|\|\||       # multi-char operators
        [()<>!] |                  # single-char operators/parens
        [A-Za-z_]\w* |             # identifiers
        \d+                        # numbers
    """
    tokens = re.findall(token_pattern, expr, flags=re.VERBOSE)

    # operator precedence table
    prec = {
        'or': 1,
        'and': 2,
        'not': 3,
        '=': 4, '/=': 4, '<': 4, '>': 4, '<=': 4, 'bvsge': 4
    }

    # translate C operators to smt/lisp/Z3 operators
    op_map = {'&&': 'and', '||': 'or', '!': 'not',
              '==': '=', '!=': '/=',
              '>=': 'bvsge'} ## nico: map bitvector ops, todo: do the others

    # convert operator tokens
    tokens = [op_map.get(t, t) for t in tokens]

    out = []
    ops = []

    def apply_op():
        op = ops.pop()
        if op == 'not':
            a = out.pop()
            out.append(f"(not {a})")
        else:
            b = out.pop()
            a = out.pop()
            out.append(f"({op} {a} {b})")

    def is_op(t):
        return t in prec

    for t in tokens:
        if re.fullmatch(r'\d+', t):  # number
            # out.append(hex(int(t)))
            # out.append(f"{int(t):#0{2+math.ceil(math.log(2**num_bits, 16))}x}")
            out.append(_hexa(int(t), num_bits))
        elif t == '(':
            ops.append(t)
        elif t == ')':
            while ops[-1] != '(':
                apply_op()
            ops.pop()
        elif is_op(t):
            while ops and ops[-1] != '(' and prec[ops[-1]] >= prec[t]:
                apply_op()
            ops.append(t)
        elif re.fullmatch(r'[A-Za-z_]\w*', t):  # variable
            out.append(t)            
        else:
            raise ValueError("unexpected token: " + t)

    while ops:
        apply_op()

    return out[0]
