"""
Convert modal qL formulas into SMT assertions.

Assumptions:
- operations with qL expressions follow a quantized arithmetics
- counting neighbours with graded modal logic is done with more standard arithmetics

TODO:
- use correct Z3 addition and product, with appropriate arithmetics - possibily only binary
- convert numbers to appropriate types - possibly adapt to bitwidth
- in particular convert "constant" Expression
"""

SMT_ADD = "saturating-add"
SMT_MUL = "saturating-mul"
SMT_ZERO = "#x00"
SMT_ONE = "#x01"
SMT_GEQ = "bvsge"


class Expression:
    def __init__(self, kind, left, right=None):
        self.kind = kind
        self.left = left
        self.right = right

    def to_smt(self, node, all_nodes):
        match self.kind:
            case "variable":
                return f"{self.left}z{node}"
            case "constant":
                return str(self.left)
            case "activation":
                return f"({self.left} {self.right.to_smt(node, all_nodes)})"
            case "sum":
                return f"({SMT_ADD} {self.left.to_smt(node, all_nodes)} {self.right.to_smt(node, all_nodes)})"
            case "prod":
                return f"({SMT_MUL} {self.left.to_smt(node, all_nodes)} {self.right.to_smt(node, all_nodes)})"
            case "agg":
                aggregation = f"({SMT_ADD}"
                for n in all_nodes:
                    aggregation += f" (ite e{node}z{n} {self.left.to_smt(n, all_nodes)} {SMT_ZERO})"
                aggregation += ")"
                return aggregation
            case "gagg":
                aggregation = f"({SMT_ADD}"
                for n in all_nodes:
                    aggregation += f" {self.left.to_smt(n, all_nodes)}"
                aggregation += ")"
                return aggregation
            case _:
                raise ValueError("Incorrect kind of Expression.")


class Formula:
    def __init__(self, kind, left, right=None):
        self.kind = kind
        self.left = left
        self.right = right

    def to_smt(self, node, all_nodes):
        match self.kind:
            case "geq":
                return f"({SMT_GEQ} {self.left.to_smt(node, all_nodes)} {self.right.to_smt(node, all_nodes)})"
            case "not":
                return f"(not {self.left.to_smt(node, all_nodes)})"
            case "or":
                return f"(or {self.left.to_smt(node, all_nodes)} {self.right.to_smt(node, all_nodes)})"
            case "diamond":  # local modal logic diamond: Formula("diamond", someformula)
                """there is at least one neighbour such that..."""
                disjunction = f"(or"
                for n in all_nodes:
                    disjunction += f" (and e{node}z{n} {self.left.to_smt(n, all_nodes)})"
                disjunction += ")"
                return disjunction
            case "diamondk":  # local graded modal logic diamond: Formula("diamondk", k, someformula)
                """there are at least k neighbours such that..."""
                counting = f"({SMT_ADD}"
                for n in all_nodes:
                    counting += f" (ite (and e{node}z{n} {self.right.to_smt(n, all_nodes)}) 1 0)"
                counting += ")"
                return f"(>= " + counting + f" {self.left})"
            case "gdiamond":  # global modal logic diamond: Formula("gdiamond", someformula)
                """there is at least one node such that..."""
                disjunction = f"(or"
                for n in all_nodes:
                    disjunction += f" {self.left.to_smt(n, all_nodes)}"
                disjunction += ")"
                return disjunction
            case "gdiamondk":  # global graded modal logic diamond: Formula("gdiamondk", k, someformula)
                """there are at least k nodes such that..."""
                counting = f"({SMT_ADD}"
                for n in all_nodes:
                    counting += f" (ite {self.right.to_smt(n, all_nodes)} 1 0)"
                counting += ")"
                return f"(>= " + counting + f" {self.left})"
            case _:
                raise ValueError("Incorrect kind of Formula.")


def ex_expressions_formulas():
    all_nodes = {1, 2, 3, 4, 13}

    three = Expression("constant", 3)
    var_x = Expression("variable", "x13")
    three_times_var_x = Expression("prod", three, var_x)
    two = Expression("constant", 2)
    three_times_var_x_plus_2 = Expression("sum", three_times_var_x, two)
    activ = Expression("activation", "ReLU", three_times_var_x_plus_2)
    print(activ.to_smt(13, all_nodes))
    one = Expression("constant", 1)

    agg = Expression("agg", var_x)
    print(agg.to_smt(13, all_nodes))
    gagg = Expression("gagg", var_x)
    print(gagg.to_smt(13, all_nodes))

    gagg2 = Expression("gagg", three_times_var_x_plus_2)
    print(gagg2.to_smt(13, all_nodes))

    geq_one = Formula("geq", activ, one)
    diamond = Formula("diamond", geq_one)
    print(diamond.to_smt(13, all_nodes))
    diamond3 = Formula("diamondk", 3, geq_one)
    print(diamond3.to_smt(13, all_nodes))
    gdiamond = Formula("gdiamond", geq_one)
    print(gdiamond.to_smt(13, all_nodes))
    gdiamond8 = Formula("gdiamondk", 8, geq_one)
    print(gdiamond8.to_smt(13, all_nodes))


if __name__ == "__main__":
    ex_expressions_formulas()
