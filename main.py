""" This program creates verification tasks for GNNs. It checks

Returns:
    _type_: _description_
"""

import subprocess
import time
import random

Number = int | float


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
                          "  testNumber();", 
                         "  for(int N1 = 0; N1 <= Nbound; N1++)", #loop over possible size of graphs
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
        
        with open("main.c", "w") as f:
             f.write('\n'.join(self.Cprogram))

    def check(self) -> None:
        self._writeCprogram()
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
                
            self._addLineInMain(f"addCte({x}, {-b[i]});")
            self._addLineInMain(f"reLU({x}, {x});")
        




def justRunATest():
    """
    small example of how to use the tool
    """
    T = VerificationTask(Nbound = 3)
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


def testSmallGNN():
    with open("log.txt", "a") as f:
        for N in range(1, 7):
            start = time.time()
            T = VerificationTask(Nbound = N)
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
            end = time.time()
            f.write("N = " + str(N) + ": " + str(end - start) + "s\n") 
        f.write("\n")




def testBigGNN():
    with open("log.txt", "a") as f:
        for N in range(3, 6):
            start = time.time()
            T = VerificationTask(Nbound = N)
            for i in range(10):
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

            M = [[random.randint(1, 10) for _ in range(10)] for _ in range(10)]
            v = [random.randint(1, 10) for _ in range(10)]
            
            for i in range(5):
                T.add_layer(M, M, M, v)

            T.add_postcondition("x10[0] >= 0")

            T.check()
            end = time.time()
            f.write("N = " + str(N) + ": " + str(end - start) + "s\n") 
        f.write("\n")



#testBigGNN()
testSmallGNN()