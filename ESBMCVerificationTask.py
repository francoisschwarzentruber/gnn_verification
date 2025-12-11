""" This program creates verification tasks for GNNs. It checks

Python program -[generate]-> C program -[parse]-> ESBMC solver -[obtain]-> Result: SAT or UNSAT.

Returns:
    _type_: _description_
"""

import subprocess
import time
import random
from gnn_verification import validity

Number = int | float


class ESBMCVerificationTask:
    index_of_feature = 0
    
    
    def __init__(self, Nbound = 3, type="charsaturation",filename="main.c",activation='ReLU'):
        """ Initialize a new verification task

        Args:
            Nbound (int, optional): bound on the number of vertices in the example/counterexample we are search for. Defaults to 3.
            type (str): a string that is the name of a C type.
                        Can be either "float" or "charsaturation".
        """
        self.Nbound = Nbound
        self.filename = filename
        self.start_of_program = "w"
        self.features = []
        self.activation =activation
        self.type = type
        self._headerCprogram()
        '''
        self.Cprogram = [f"#define Nbound {Nbound}",
                         'unsigned int N = Nbound; //number of vertices', 
                         f'#include "type{type}.h"',
                          '#include "quantlogic.h"',
                          '',
                         "int main()",
                         "  {",
                          "  testNumber();", 
                         "  for(int N1 = 0; N1 <= Nbound; N1++)", #loop over possible size of graphs
                         "  {", # { of the for loop
                         "    N = N1;", #assign the number of vertices N (global variable)
                         "    unknownGraph();"]
        '''
    def _headerCprogram(self) -> None:
        """ add the header of the C program
        """
        with open(self.filename, self.start_of_program) as c_file:
            c_file.write(f"#define Nbound {self.Nbound}\n")
            c_file.write('unsigned int N = Nbound; //number of vertices\n')
            c_file.write(f'#include "type{self.type}.h"\n')
            c_file.write('#include "quantlogic.h"\n\n')
            c_file.write("int main()\n")
            c_file.write("  {\n")
            c_file.write("  testNumber();\n")
            c_file.write("  for(int N1 = 0; N1 <= Nbound; N1++)\n") #loop over possible size of graphs
            c_file.write("  {\n") # { of the for loop  
            c_file.write("    N = N1;\n") #assign the number of vertices N (global variable)
            c_file.write("    unknownGraph();\n")
        self.start_of_program ="a"

    def _addLineInMain(self, line: str) -> None:
        """ add a line in the main function in the C program

        Args:
            line (str): line to be added to the main function in the generated C program
        """
        with open(self.filename, self.start_of_program) as c_file:
            c_file.write("    " + f"{line}\n")
        
    
    def _get_new_featurename(self) -> str:
        """ Create a new feature name (e.g. "x3", "x4", etc.)

        Returns:
            str: the name of the feature, e.g. "x3", "x4", etc.
        """
        self.index_of_feature = self.index_of_feature + 1
        featureName = f"x{self.index_of_feature}"
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
        
    def add_precondition(self, precondition: str) -> None:
        """ add a precondition

        Args:
            precondition (str): a string representing a precondition in C. 
            For example, "x1[0] <= 5 && x2[1] >= 6"
        """
        self._addLineInMain(f"__ESBMC_assume({precondition});")

    def add_layer(self, A: list[list[Number]],
                  Magg: list[list[Number]], 
                  MaggG: list[list[Number]],
                  b: list[Number]) -> None:
        input_dimension = len(A[0])
        output_dimension = len(A)
        # validity
        if validity.checking_input_matrices(input_dimension, A, Magg, MaggG, b) != 'fine':
            raise ValueError("Something wrong. Check your input.")

        previousFeatures = self.features[-input_dimension:]
        
        aggPreviousFeatures = [self._add_feature() for j in range(input_dimension)]
        aggGPreviousFeatures = [self._add_feature() for j in range(input_dimension)]
        
        for j in range(input_dimension):
            self._addLineInMain(f"agg({aggPreviousFeatures[j]}, {previousFeatures[j]});")
            self._addLineInMain(f"aggG({aggGPreviousFeatures[j]}, {previousFeatures[j]});")

        for i in range(output_dimension):
            x = self._add_feature()
            for j in range(input_dimension):
                self._addLineInMain(f"mul({x}, {A[i][j]}, {previousFeatures[j]});")
                
            for j in range(input_dimension):
                self._addLineInMain(f"mul({x}, {Magg[i][j]}, {aggPreviousFeatures[j]});")  
                
            for j in range(input_dimension):
                self._addLineInMain(f"mul({x}, {MaggG[i][j]}, {aggGPreviousFeatures[j]});")
                
            self._addLineInMain(f"addCte({x}, {-b[i]});")
            self._addLineInMain(f"reLU({x}, {x});")
    
    def get_last_feature(self) -> str:
        return self.features[-1]
    
    def add_postcondition(self, postcondition: str) -> None:
          self._addLineInMain(f"assert({postcondition});")

    def _endCprogram(self) -> None:
        """ write the C program corresponding to the verification task

        Returns:
            _type_: _description_
        """

        """
        self.Cprogram.append('  }') # end of the for loop
        self.Cprogram.append('  return 0;')
        self.Cprogram.append('}') # end of the C main function
        """

        with open(self.filename, self.start_of_program) as c_file:
            c_file.write('  }\n')
            c_file.write('  return 0;\n')
            c_file.write('}\n')

    def check(self) -> None:
        self._endCprogram()
        subprocess.run(["./esbmc",
                        "--no-bounds-check", 
                        "--no-pointer-check", 
                        "--no-div-by-zero-check", 
                        #"--z3",
                        "--cvc",
                        #"--no-unwinding-assertions", 
                        "main.c"],
                       stdout=subprocess.DEVNULL,
                       stderr = subprocess.DEVNULL)
    




def justRunATest():
    """
    small example of how to use the tool
    """
    T = ESBMCVerificationTask(Nbound = 3)
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





def testGNN():
    dimension = 2
    nb_layers = 2
    max_nb_vertices = 6
    with open("log.txt", "a") as f:
        f.write(f"# test with dimension {dimension}, nb of layers = {nb_layers}\n");
        for N in range(1, max_nb_vertices+1):
            start = time.time()
            T = ESBMCVerificationTask(Nbound = N)
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

            T.add_postcondition(f"{T.get_last_feature()}[0] >= 0")

            T.check()
            end = time.time()
            f.write("N = " + str(N) + ": " + str(end - start) + "s\n") 
        f.write("\n")
        f.write("\n")


testGNN()

