""" This program creates verification tasks for GNNs. It checks

Returns:
    _type_: _description_
"""

import subprocess
import time
import random
import math

from c_to_smt import c_to_smt

Number = int | float

C_filename = "main.c"
Z3_filename = "main.smt"


class VerificationTask:
    i = 0
    
    
    def __init__(self, Nbound = 3, type="charsaturation"):
        """ Initialize a new verification task

        Args:
            Nbound (int, optional): bound on the number of vertices in the example/counterexample we are search for. Defaults to 3.
            type (str): a string that is the name of a C type.
                        Can be either "float" or "charsaturation".
        """
        self.features = []
        self.Cprogram = [f"#define Nbound {Nbound}",
                         'unsigned int N = Nbound; //number of vertices', 
                         f'#include "type{type}.h"',
                          '#include "quantlogic.h"',
                          '',
                         "int main()",
                         "  {",
                         "  // testNumber();", 
                         "  for(int N1 = 1; N1 <= Nbound; N1++)", #loop over possible size of graphs # nico: N1 = 1 instead of 0
                         "  {", # { of the for loop
                         "    N = N1;", #assign the number of vertices N (global variable)
                         "    unknownGraph();"]



    def _addLineInMain(self, line: str) -> None:
        """ add a line in the main function in the C program

        Args:
            line (str): line to be added to the main function in the generated C program
        """
        self.Cprogram.append("    " + line)
        
        
    def _get_new_featurename(self) -> str:
        """ Create a new feature name (e.g. "x3", "x4", etc.)

        Returns:
            str: the name of the feature, e.g. "x3", "x4", etc.
        """
        self.i = self.i + 1
        featureName = f"x{self.i}"
        self.features.append(featureName)
        return featureName

    def add_input_feature(self) -> str:
        """ Add a new input feature. An input feature is undefined. We are search for a value of it in a counterexample.

        Returns:
            str: the name of the feature that was added
        """
        x = self._get_new_featurename()
        self._addLineInMain(f"feature({x});")
        self._addLineInMain(f"unknownFeature({x});")
        return x
    
    def _add_feature(self) -> str:
        """ Add an intermediate feature (set to 0 initially)

        Returns:
           str: name of the added feature
        """
        x = self._get_new_featurename()
        self._addLineInMain(f"feature({x});")
        return x
    
    
    def get_last_feature(self) -> str:
        return self.features[-1]
        
    def add_precondition(self, precondition: str) -> None:
        """ add a precondition

        Args:
            precondition (str): a string representing a precondition in C. 
            For example, "x1[0] <= 5 && x2[1] >= 6"
        """
        self._addLineInMain(f"__ESBMC_assume({precondition});")


    def add_postcondition(self, postcondition: str) -> None:
          self._addLineInMain(f"assert({postcondition});")



    def _writeCprogram(self) -> None:
        """ write the C program corresponding to the verification task

        Returns:
            _type_: _description_
        """
        self.Cprogram.append('  }') # end of the for loop
        self.Cprogram.append('  return 0;')
        self.Cprogram.append('}') # end of the C main function
        
        with open(C_filename, "w") as f:
             f.write('\n'.join(self.Cprogram))

        print(f"C program written in {C_filename}.")        

    def check(self) -> None:
        self._writeCprogram()
        subprocess.run(["esbmc",
                        "--no-bounds-check", 
                        "--no-pointer-check", 
                        "--no-div-by-zero-check", 
                        #"--z3",
                        "--cvc",
                        #"--no-unwinding-assertions", 
                        "main.c"],
                       stdout=subprocess.DEVNULL,
                       stderr = subprocess.DEVNULL)


    def add_layer(self, A: list[list[Number]],
                  Magg: list[list[Number]], 
                  MaggG: list[list[Number]],
                  b: list[Number]) -> None:
        previousFeatures = self.features[-len(A[0]):]
        
        aggPreviousFeatures = [self._add_feature() for j in range(len(A[0]))]
        aggGPreviousFeatures = [self._add_feature() for j in range(len(A[0]))]
        
        for j in range(len(A[0])):
            self._addLineInMain(f"agg({aggPreviousFeatures[j]}, {previousFeatures[j]});")
            self._addLineInMain(f"aggG({aggGPreviousFeatures[j]}, {previousFeatures[j]});")

        for i in range(len(A)):
            x = self._add_feature()
            for j in range(len(A[i])):
                self._addLineInMain(f"mul({x}, {A[i][j]}, {previousFeatures[j]});")
                
            for j in range(len(A[i])):
                self._addLineInMain(f"mul({x}, {Magg[i][j]}, {aggPreviousFeatures[j]});")  
                
            for j in range(len(A[i])):
                self._addLineInMain(f"mul({x}, {MaggG[i][j]}, {aggGPreviousFeatures[j]});")
                
            self._addLineInMain(f"addCte({x}, {b[i]});")
            self._addLineInMain(f"reLU({x}, {x});")


class VerificationTaskZ3:
    
    def __init__(self, Nbound=3, bits=8):
        """ Initialize a new verification task

        Args:
            Nbound (int, optional): bound on the number of vertices in the example/counterexample we are search for. Defaults to 3.
            bits (int): number of bits to represent numbers".
        """
        self.Nbound = Nbound
        self.bits = bits
        self.features = []
        self.next_feat_id = 0
        self.Z3program = ["""(define-fun saturating-add ((x1 (_ BitVec 8)) (x2 (_ BitVec 8))) (_ BitVec 8)
	    (ite (bvsge x2 #b00000000)
		 (ite (bvsle x1 (bvsub #b01111111 x2)) (bvadd x1 x2) #b01111111)
		 (ite (bvsge x1 (bvsub #b10000000 x2)) (bvadd x1 x2) #b10000000)))
""",
                          """(define-fun saturating-mul ((x1 (_ BitVec 8)) (x2 (_ BitVec 8))) (_ BitVec 8)
	    (let ((res (bvmul x1 x2)))
	      (ite (= x1 #b00000000)
		   #b00000000
		   (ite (= (bvsdiv res x1) x2)
			res
			(ite (bvsgt x1 #b00000000)
			     (ite (bvsgt x2 #b00000000)
				  #b01111111
				  #b10000000)
			     (ite (bvsgt x2 #b00000000)
				  #b10000000
				  #b01111111))))))
"""]  # todo: use {self.nbits} instead of 8
        self._declare_adjacency_matrix()

    def _addLineInMain(self, line: str) -> None:
        """ add a line in the main function in the C program

        Args:
            line (str): line to be added to the main function in the generated C program
        """
        self.Z3program.append(line)

    def _declare_adjacency_matrix(self):
        """ Declare the Bool constants that define the adjacency matrix.

            They take the form "e{i}z{j}", where i and j identify two nodes. ('z' is only a separator.)
        e{i}z{j} is True when there is an edge between node i and node j; it is False otherwise.
        """
        for i in range(self.Nbound):
            for j in range(self.Nbound):
                self._addLineInMain(f"(declare-const e{i}z{j} Bool)")
        
    def _get_new_featurename(self) -> str:
        """ Create a new feature name (e.g. "x3", "x4", etc.)

        Returns:
            str: the name of the feature, e.g. "x3", "x4", etc.
        """
        self.next_feat_id = self.next_feat_id + 1
        featureName = f"x{self.next_feat_id}"
        self.features.append(featureName)
        return featureName

    def add_input_feature(self) -> str:
        """ Add a new input feature.

        It takes the form "x{i}z{j}", where i is a feature id, and and j identifies a node. ('z' is only a separator.) x{i}z{j} holds the value of feature i at node j.
        Returns:
            str: the name of the feature that was added
        """
        x = self._get_new_featurename()
        for n in range(self.Nbound):
            self._addLineInMain(f"(declare-const {x}z{n} (_ BitVec {self.bits}))")
        return x
    
    def _add_feature(self) -> str:
        """ Add an intermediate feature (set to 0 initially)

        Returns:
           str: name of the added feature
        """
        x = self._get_new_featurename()
        for n in range(self.Nbound):
            self._addLineInMain(f"(declare-const {x}z{n} (_ BitVec {self.bits}))")
        return x
    
    
    def get_last_feature(self) -> str:
        return self.features[-1]
        
    def add_precondition(self, precondition: str) -> None:
        """ add a precondition

        Args:
            precondition (str): a string representing a precondition in C. 
            For example, "x1[0] <= 5 && x2[1] >= 6"
        """
        self._addLineInMain(f";; precondition {precondition}")
        self._addLineInMain(f"(assert {c_to_smt(precondition, self.bits)})")

    def add_postcondition(self, postcondition: str) -> None:
        """We are going to check that the postcondition is always verified using satisfiability.

        So we are asserting *the negation* of postcondition.

        The postcondition is valid when the program with the negation
        of the postcondition is UNSAT.

        """
        self._addLineInMain(f";; postcondition {postcondition}")
        self._addLineInMain(f"(assert (not {c_to_smt(postcondition, self.bits)}))")  # "(not ..." is on purpose!

    def add_precondition_Formula(self, f: Formula, node) -> None:
        self._addLineInMain(f";; precondition formula")
        self._addLineInMain(f"(assert {f.to_smt(node, range(self.Nbound))})")

    def add_postcondition_Formula(self, f: Formula) -> None:
        self._addLineInMain(f";; postcondition formula")
        self._addLineInMain(f"(assert (not {f.to_smt(node, range(self.Nbound))}))")  # "(not ..." is on purpose!

    def _writeZ3program(self) -> None:
        """ write the C program corresponding to the verification task

        Returns:
            _type_: _description_
        """
        with open(Z3_filename, "w") as f:
             f.write('\n'.join(self.Z3program))
        print(f"Z3 program written in {Z3_filename}.")

    def check(self) -> None:
        self._addLineInMain(f"(check-sat)")            
        self._writeZ3program()
        subprocess.run(["z3",
                        "main.smt"])#,
                       #stdout=subprocess.DEVNULL,
                       #stderr = subprocess.DEVNULL)

    def _hexa(self, val):
        """converts decimal integer to hexa representation, in the format of Z3,
        adapting to the number of bits.

        Warning: Rounding with math.ceil could be buggy, especially
        for uncommon (odd, not power-of-two, ...) bit numbers. Check
        with Z3 format.

        """
        if (val >= 0):
            return '#' + f"{val:#0{2+math.ceil(math.log(2**self.bits, 16))}x}"[1:]
        else:
            return '(bvneg #' + f"{-val:#0{2+math.ceil(math.log(2**self.bits, 16))}x}"[1:] +')'
        
    def _agg(self, agg_prev_feat, prev_feat, local) -> str:
        """handles aggreate features.

        Args:
            agg_prev_feat: ...
            prev_feat: ...
            local (bool): True if local aggregation, False otherwise
        """
        if (local):
            self._addLineInMain(f";; agg({agg_prev_feat}, {prev_feat})")
        else:
            self._addLineInMain(f";; aggG({agg_prev_feat}, {prev_feat})")
        for i in range(self.Nbound):
            self._addLineInMain(f"(assert (= {agg_prev_feat}z{i}")
            
            for j in range(self.Nbound):
                if (j < self.Nbound - 1): self._addLineInMain(f"  (saturating-add")                
                if (local):
                    self._addLineInMain(f"    (ite e{i}z{j} {prev_feat}z{j} {self._hexa(0)})")
                else:
                    self._addLineInMain(f"    {prev_feat}z{j}")
            self._addLineInMain(f"  " + ")"*(1+self.Nbound))  # close all parentheses

    def _forward(self, out_dim, A, Magg, MaggG, b,
                 previousFeatures, aggPreviousFeatures, aggGPreviousFeatures):
        """
        Warning: this does not apply the activation function.
        
        Compute *out_dim*th output dimension of layer
        A(previousFeatures) + Magg(aggPreviousFeatures) + MaggG(aggGPreviousFeatures) + b
        """
        x = self._add_feature()
        self._addLineInMain(f";; {x}; {out_dim + 1}th dimension")
        input_dimension = len(A[0])
        for i in range(self.Nbound):
            self._addLineInMain(f";; {x}z{i}")            
            self._addLineInMain(f"(assert (= {x}z{i}")
        
            for j in range(input_dimension):
                self._addLineInMain(f"  (saturating-add")
                self._addLineInMain(f"    (saturating-mul {previousFeatures[j]}z{i} {self._hexa(A[out_dim][j])})")
                
            for j in range(input_dimension):
                self._addLineInMain(f"  (saturating-add")
                self._addLineInMain(f"    (saturating-mul {aggPreviousFeatures[j]}z{i} {self._hexa(Magg[out_dim][j])})")
                
            for j in range(input_dimension):
                self._addLineInMain(f"  (saturating-add")                
                self._addLineInMain(f"    (saturating-mul {aggGPreviousFeatures[j]}z{i} {self._hexa(MaggG[out_dim][j])})")

            self._addLineInMain(f"    {self._hexa(b[out_dim])}")
            self._addLineInMain(f"  " + ")"*(2 + 3*input_dimension))  # close all parentheses

    def _relu(self, feature):
        self._addLineInMain(f";; feature for ReLU of {feature}")  # todo check ReLU
        r = self._add_feature()  # todo check ReLU
        for i in range(self.Nbound):
            self._addLineInMain(f";; ReLU of {feature}z{i}")
            self._addLineInMain(f"(assert (= {r}z{i} (ite (bvsge {feature}z{i} {self._hexa(0)}) {feature}z{i} {self._hexa(0)})))")  # todo check ReLU
        return r
    
    def add_layer(self, A: list[list[Number]],
                  Magg: list[list[Number]], 
                  MaggG: list[list[Number]],
                  b: list[Number]) -> None:
        input_dimension = len(A[0])
        output_dimension = len(A)
        previousFeatures = self.features[-input_dimension:]
        aggPreviousFeatures = [self._add_feature() for j in range(input_dimension)]
        aggGPreviousFeatures = [self._add_feature() for j in range(input_dimension)]
        
        for j in range(input_dimension):
            self._agg(aggPreviousFeatures[j], previousFeatures[j], local=True)
            self._agg(aggGPreviousFeatures[j], previousFeatures[j], local=False)            

        self._addLineInMain(f";; begin layer forward computations")
        for i in range(output_dimension):
            self._forward(i, A, Magg, MaggG, b, previousFeatures,
                          aggPreviousFeatures, aggGPreviousFeatures)
        beforeReLUfeatures = self.features[-output_dimension:]
        for i in range(output_dimension):
            self._relu(beforeReLUfeatures[i])
        self._addLineInMain(f";; end layer forward computations")



def VTfactory(c_or_z3, Nbound, bits):
    if (c_or_z3 == "C"):
        T = VerificationTask(Nbound)
    elif (c_or_z3 == "Z3"):
        T = VerificationTaskZ3(Nbound, bits)
    else:
        raise ValueError("Verification task can be only C or Z3.")
    return T


def justRunATest(c_or_z3):
    """
    small example of how to use the tool
    """
    T = VTfactory(c_or_z3, 3, 8)
    T.add_input_feature()
    T.add_input_feature()
    T.add_input_feature()

    T.add_precondition("x1[0] == 0")
    T.add_precondition("x1[1] == 0")
    T.add_precondition("x1[2] == 0")
    T.add_precondition("x2[0] == 0")
    T.add_precondition("x2[1] == 0")
    T.add_precondition("x2[2] == 0")
    T.add_precondition("x3[0] == 0 || x3[0] == 1")
    T.add_precondition("x3[1] == 0")
    T.add_precondition("x3[2] == 0")

    T.add_layer([[2, 3, 1], [1, 0, -7]],
                [[2, 3, 1], [1, 0, -7]],
                [[2, 3, 1], [1, 0, -7]],
                [1, 8])

    T.add_postcondition("x10[0] >= 0")

    T.check()


def testGNN(c_or_z3, dimension, nb_layers, max_nb_vertices, rand_post_cond=False):
    with open("log.txt", "a") as f:
        f.write(f"# test with dimension {dimension}, nb of layers = {nb_layers}\n");
        for N in range(1, max_nb_vertices+1):
            print(f"N={N}")
            start = time.time()
            T = VTfactory(c_or_z3, N, 8)
            for i in range(dimension):
                x = T.add_input_feature()
                for v in range(N):
                    T.add_precondition(f"{x}[{v}] == 0 || {x}[{v}] == 1")
                               
            for i in range(nb_layers):
                Mvertex = [[random.randint(1, 10) for _ in range(dimension)] for _ in range(dimension)]
                Magg = [[random.randint(1, 10) for _ in range(dimension)] for _ in range(dimension)]
                Maggglobal = [[random.randint(1, 10) for _ in range(dimension)] for _ in range(dimension)]
                biais = [random.randint(1, 10) for _ in range(dimension)]
                T.add_layer(Mvertex, Magg, Maggglobal, biais)

            T.add_postcondition(f"{T.get_last_feature()}[0] >= {random.randint(-(2**8), 2**8-1) if rand_post_cond else 0}")

            T.check()
            end = time.time()
            f.write("N = " + str(N) + ": " + str(end - start) + "s\n") 
        f.write("\n")
        f.write("\n")


def simple(c_or_z3):
    """
    simple example.
    """
    T = VTfactory(c_or_z3, Nbound=2, bits=8)
    T.add_input_feature()
    T.add_input_feature()

    T.add_precondition("x1[0] == 1")
    T.add_precondition("x2[0] == 2")

    T.add_layer([[1, 2]],
                [[0, 0]],
                [[0, 0]],
                [0])

    T.add_postcondition("x7[0] == 5")

    T.check()


def simplebias(c_or_z3):
    """
    simple example with a bias.
    """
    T = VTfactory(c_or_z3, Nbound=2, bits=8)
    T.add_input_feature()
    T.add_input_feature()

    T.add_precondition("x1[0] == 1")
    T.add_precondition("x2[0] == 2")

    T.add_layer([[1, 2]],
                [[0, 0]],
                [[0, 0]],
                [-5])

    T.add_postcondition("x7[0] == 0")

    T.check()


def z3_simplebias_with_simple_formulas():
    """
    Same as simplebias() but with Formula (only for Z3)
    """

    from logic import Expression, Formula
    
    T = VTfactory("Z3", Nbound=2, bits=8)
    T.add_input_feature()
    T.add_input_feature()

    x1 = Expression("variable", "x1")
    x2 = Expression("variable", "x2")
    one = Expression("constant", "#x01")
    two = Expression("constant", "#x02")
    geq11 = Formula("geq", x1, one)
    geq12 = Formula("geq", one, x1)
    geq21 = Formula("geq", x2, two)
    geq22 = Formula("geq", two, x2)
    f = Formula("not", Formula("or",
                               Formula("or",
                                       Formula("or",
                                               Formula("not", geq11),
                                               Formula("not", geq12)
                                               ),
                                       Formula("not", geq21)
                                       ),
                               Formula("not", geq22), 
                               ))
    
    T.add_precondition_Formula(f, 0)

    T.add_layer([[1, 2]],
                [[0, 0]],
                [[0, 0]],
                [-5])

    T.add_postcondition("x7[0] == 0")

    T.check()
    


if __name__ == "__main__":
    # justRunATest()
    # testGNN("Z3", 2, 2, 6, False)  # orginal test
    # testGNN("Z3", dimension=6, nb_layers=3, max_nb_vertices=20, rand_post_cond=True)
    # simple("Z3")
    # simplebias("Z3")
    z3_simplebias_with_simple_formulas()
