import subprocess
import time
import random
import math
import re 
import numpy as np
from pathlib import Path
from datetime import datetime

from gnn_verification.z3_flow.testZ3 import Z3VerificationTask



def simpleACRGNN(in_filename,in_bitvect,in_activation):
    nbound=2
    in_filename= in_filename.replace('.smt',f'Nbound{nbound}_simpleACRGNN_{in_activation}.smt')
    v = Z3VerificationTask(nbound,filename=in_filename,bitvect=in_bitvect,activation=in_activation)
    for i in range(nbound):
        v.add_input_feature()
    #add preconditions
    v.add_precondition("x1[0] == 1")
    v.add_precondition("x2[0] == 2")
    #add layer with the C, A, R ,b matrices
    v.add_layer([[1, 2]],
                [[0, 0]],
                [[0, 0]],
                [[0]])
    
    #add postconditions
    v.add_postcondition(f"{v.get_last_feature()}[0] == 5")
    status, values = v.check()
    print("STATUS:", status)

    if status == "sat":
        print("INTERMEDIATE VALUES:")
        for name, val in sorted(values.items()):
            print(f"  {name} = {val}")
    else:
        print("No model available (unsat/unknown).")


def simpleACRGNN_bias(in_filename,in_bitvect,in_activation):
    nbound=2
    in_filename= in_filename.replace('.smt',f'Nbound{nbound}_simpleACRGNN_bias_{in_activation}.smt')
    v = Z3VerificationTask(Nbound = nbound,filename=in_filename,bitvect=in_bitvect,activation=in_activation)
    for i in range(nbound):
        v.add_input_feature()
    #add preconditions
    v.add_precondition("x1[0] == 1")
    v.add_precondition("x2[0] == 2")
    #add layer with the C, A, R ,b matrices
    v.add_layer([[1, 2]],
                [[0, 0]],
                [[0, 0]],
                [[5]])
    #add postconditions
    v.add_postcondition(f"{v.get_last_feature()}[0] == 0")
    v.check()
    status, values = v.check()
    print("STATUS:", status)

    if status == "sat":
        print("INTERMEDIATE VALUES:")
        for name, val in sorted(values.items()):
            print(f"  {name} = {val}")
    else:
        print("No model available (unsat/unknown).")

def justRunATest(in_filename,in_bitvect,in_activation):
    """
    small example of how to use the tool
    """
    nbound=3
    in_filename= in_filename.replace('.smt',f'Nbound{nbound}_justRunATest_{in_activation}.smt')
    T = Z3VerificationTask(Nbound = 3,filename=in_filename,bitvect=in_bitvect,activation=in_activation)
    for i in range(3):
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
                [[1], [8]])
    T.add_postcondition(f"{T.get_last_feature()}[0] >= 0")
    T.check()
    status, values = T.check()
    print("STATUS:", status)

    if status == "sat":
        print("INTERMEDIATE VALUES:")
        for name, val in sorted(values.items()):
            print(f"  {name} = {val}")
    else:
        print("No model available (unsat/unknown).")

def testGNN(in_filename,in_bitvect,in_activation):
    dimension =2 
    nb_layers = 2
    max_nb_vertices = 6
    with open(f"log.txt", "a") as f:
        f.write(f"# Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# test with dimension {dimension}, nb of layers = {nb_layers}, bits -{in_bitvect},activation function-{in_activation}\n")
        base = in_filename.replace(".smt", "")  
        for N in range(1, max_nb_vertices+1):
            filename_N = f"{base}_Nbound{N}_testGNN.smt"
            start = time.time()
            T = Z3VerificationTask(Nbound = N,filename=filename_N,bitvect=in_bitvect,activation=in_activation)
            for i in range(dimension):
                x = T.add_input_feature()
                for v in range(N):
                    T.add_precondition(f"{x}[{v}] == 0 || {x}[{v}] == 1")
                               
            for i in range(nb_layers):
                Mvertex = [[random.randint(1, 10) for _ in range(dimension)] for _ in range(dimension)]
                print('Mvertex',np.shape(Mvertex))
                Magg = [[random.randint(1, 10) for _ in range(dimension)] for _ in range(dimension)]
                print('Magg',np.shape(Magg))
                Maggglobal = [[random.randint(1, 10) for _ in range(dimension)] for _ in range(dimension)]
                print('Maggglobal',np.shape(Maggglobal))
                biais = [[random.randint(1, 10)] for _ in range(dimension)]
                print('biais',np.shape(biais))
                T.add_layer(Mvertex, Magg, Maggglobal, biais)

            T.add_postcondition(f"{T.get_last_feature()}[0] >= 0")

            T.check()
            status, values = v.check()
            print("STATUS:", status)

            if status == "sat":
                print("INTERMEDIATE VALUES:")
                for name, val in sorted(values.items()):
                    print(f"  {name} = {val}")
            else:
                print("No model available (unsat/unknown).")
            end = time.time()
            f.write(f"Finished N={N} in {end - start:.4f}s\n\n") 
        f.write("\n")
        f.write("\n")






activations = ['ReLU','ReLU6','trReLU']

for act in activations:
    folder = Path(f"results/results_{act}")
    folder.mkdir(parents=True, exist_ok=True)
    smt_path = folder / f"output_{act}.smt"
    testGNN(str(smt_path), 8, act)

#simpleACRGNN("output.smt",8,'ReLU')
simpleACRGNN_bias("output.smt",8,'ReLU')
#justRunATest("output.smt",8,'ReLU')
