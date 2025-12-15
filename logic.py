"""
Convert modal qL formulas into SMT assertions.

"""

class Expression:
    def __init__(self, kind, left, right=False):
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
                return f"(smt-add {self.left.to_smt(node, all_nodes)} {self.right.to_smt(node, all_nodes)})"
            case "prod":
                return f"(smt-mul {self.left.to_smt(node, all_nodes)} {self.right.to_smt(node, all_nodes)})"
            case _:
                raise ValueError("Incorrect kind of expression.")


class Formula:
    def __init__(self, kind, left, right=False):
        self.kind = kind
        self.left = left
        self.right = right
    
    def to_smt(self, node, all_nodes):
        match self.kind:
            case "geq":
                return f"(>= {self.left.to_smt(node, all_nodes)} {self.right.to_smt(node, all_nodes)})"
            case "not":
                return f"(not {self.left.to_smt(node, all_nodes)})"
            case "or":
                return f"(or {self.left.to_smt(node, all_nodes)} {self.right.to_smt(node, all_nodes)})"
            case "diamond":  # local modal logic diamond: Formula("diamond", someformula)
                """there is at least one successor such that..."""
                disjunction = f"(or "               
                for neigh in all_nodes:
                    disjunction += f"(and e{node}z{neigh} {self.left.to_smt(neigh, all_nodes)}) "
                disjunction += ")"
                return disjunction
            case "diamondk":  # local graded modal logic diamond: Formula("diamondk", k, someformula)
                """there are at least k successors such that..."""
                counting = f"(smt-add "
                for neigh in all_nodes:
                    counting += f"(ite (and e{node}z{neigh} {self.right.to_smt(neigh, all_nodes)}) 1 0) "
                counting += ")"
                return "(smt-geq " + counting + f" {self.left})"
            case "gdiamond":  # global modal logic diamond: Formula("gdiamond", someformula)
                """there is at least one node such that..."""
                disjunction = f"(or "               
                for neigh in all_nodes:
                    disjunction += f"{self.left.to_smt(neigh, all_nodes)} "
                disjunction += ")"
                return disjunction
            case "gdiamondk":  # global graded modal logic diamond: Formula("gdiamondk", k, someformula)
                """there are at least k nodes such that..."""
                counting = f"(smt-add "
                for neigh in all_nodes:
                    counting += f"(ite {self.right.to_smt(neigh, all_nodes)} 1 0) "
                counting += ")"
                return "(smt-geq " + counting + f" {self.left})"
                

                
def ex_expression():
    three = Expression("constant", 3)
    var_x = Expression("variable", "x13")
    three_times_var_x = Expression("prod", three, var_x)
    two = Expression("constant", 2)
    three_times_var_x_plus_2 = Expression("sum", three_times_var_x, two)
    activ = Expression("activation", "ReLU", three_times_var_x_plus_2)
    print(activ.to_smt(13, {1, 2, 3, 4, 13}))
    one = Expression("constant", 1)
    geq_one = Formula("geq", activ, one)
    diamond = Formula("diamond", geq_one)
    print(diamond.to_smt(13, {1, 2, 3, 4, 13}))
    diamond3 = Formula("diamondk", 3, geq_one)
    print(diamond3.to_smt(13, {1, 2, 3, 4, 13}))
    gdiamond = Formula("gdiamond", geq_one)
    print(gdiamond.to_smt(13, {1, 2, 3, 4, 13}))
    gdiamond8 = Formula("gdiamondk", 8, geq_one)
    print(gdiamond8.to_smt(13, {1, 2, 3, 4, 13}))
    
ex_expression()
