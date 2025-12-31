import time
import random
import numpy as np
from pathlib import Path
from datetime import datetime

import sys
from pathlib import Path

from z3VerificationTask import Z3VerificationTask


def simpleACRGNN(in_filename,in_bitvect,in_activation,in_configurations):
    nbound=2
    number_of_input_features = 2
    in_filename= in_filename.replace('.smt',f'Nbound{nbound}_simpleACRGNN_{in_activation}.smt')
    v = Z3VerificationTask(nbound,number_of_input_features,filename=in_filename,bitvect=in_bitvect,activation=in_activation,configurations=in_configurations)
    for i in range(number_of_input_features):
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

def simpleACRGNN_bias(in_filename,in_bitvect,in_activation,in_configurations):
    nbound=2
    in_filename= in_filename.replace('.smt',f'Nbound{nbound}_simpleACRGNN_bias_{in_activation}_bit_{in_bitvect}.smt')
    v = Z3VerificationTask(Nbound = nbound,filename=in_filename,bitvect=in_bitvect,activation=in_activation,configurations=in_configurations)
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
    elif status == "unknown":
        print("The solver returned 'unknown', unable to determine satisfiability.")
    else:
        print("unsat.")

def justRunATest(in_filename,in_bitvect,in_activation,in_configurations):
    """
    small example of how to use the tool
    """
    nbound=3
    in_filename= in_filename.replace('.smt',f'Nbound{nbound}_justRunATest_{in_activation}_bit_{in_bitvect}.smt')
    T = Z3VerificationTask(Nbound = 3,filename=in_filename,bitvect=in_bitvect,activation=in_activation,configurations=in_configurations)
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

def testGNN(in_filename,in_bitvect,in_activation,in_configurations):
    dimension =2 
    nb_layers = 2
    max_nb_vertices = 6
    with open(f"results/resultsZ3/Z3log.txt", "a") as f:
        f.write(f"# Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# test with dimension {dimension}, nb of layers = {nb_layers}, bits -{in_bitvect},activation function-{in_activation}\n")
        base = in_filename.replace(".smt", "")  
        for N in range(1, max_nb_vertices+1):
            filename_N = f"{base}_Nbound{N}_testGNN_{in_activation}_bit_{in_bitvect}.smt"
            start = time.time()
            T = Z3VerificationTask(Nbound = N,filename=filename_N,bitvect=in_bitvect,activation=in_activation,configurations=in_configurations)
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
            status, values = T.check()
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


ACRGNN_configurations = ['Cx+Ay+Rz+b', 'xC+yA+zR+b']
configurations = ACRGNN_configurations[0]  #choose either 'Cx+Ay+Rz+b' or 'xC+yA+zR+b'

activations = ['ReLU','ReLU6','trReLU']
folder = Path(f"results/resultsZ3")
folder.mkdir(parents=True, exist_ok=True)
'''
for act in activations:
    folder_act = Path(f"{folder}/results_{act}")
    folder_act.mkdir(parents=True, exist_ok=True)
    smt_path = folder_act / f"main_{act}.smt"
    testGNN(str(smt_path), 8, act,configurations)

'''
#simpleACRGNN("main.smt",8,'ReLU',configurations)
smt_path = folder / f"main.smt"
simpleACRGNN_bias(str(smt_path),8,'ReLU',configurations)
#justRunATest("main.smt",8,'ReLU',configurations)
