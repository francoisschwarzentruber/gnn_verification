import time
import random
import numpy as np
import sys
from pathlib import Path
from datetime import datetime

from esbmc_flow.ESBMCVerificationTask import ESBMCVerificationTask
from z3_flow.z3VerificationTask import Z3VerificationTask

def confifurationsmt_solver(nbound,in_filename,in_bitvect,in_activation,smt_flag):
    if smt_flag == 'Z3':
        in_filename= in_filename.replace('.smt',f'Nbound{nbound}_ACRGNN_{in_activation}.smt')
        v = Z3VerificationTask(Nbound =nbound,filename=in_filename,bitvect=in_bitvect,activation=in_activation)
    elif smt_flag == 'ESBMC':
        in_filename= in_filename.replace('.c',f'Nbound{nbound}_ACRGNN_{in_activation}.c')
        v = ESBMCVerificationTask(Nbound =nbound,filename=in_filename,activation=in_activation)
    else:
        raise ValueError(f"Unsupported SMT solver: {smt_flag}")
    return v


def simpleACRGNN(in_filename,in_bitvect,in_activation,smt_flag):
    nbound=2
    
    v=confifurationsmt_solver(nbound,in_filename,in_bitvect,in_activation,smt_flag)

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
        with open(f"results/results{smt_flag}/{smt_flag}_sat_log.txt", "a") as sat:
            sat.write(f"simpleACRGNN with {in_activation} the result: {status}\n\n") 
            for name, val in sorted(values.items()):
                sat.write(f"  {name} = {val}\n")
            sat.write(f" \n\n")
    else:
        print("No model available (unsat/unknown).")

def simpleACRGNN_bias(in_filename,in_bitvect,in_activation,smt_flag):
    nbound=2
    v=confifurationsmt_solver(nbound,in_filename,in_bitvect,in_activation,smt_flag)

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
        with open(f"results/results{smt_flag}/{smt_flag}_sat_log.txt", "a") as sat:
            sat.write(f"simpleACRGNN_bias with {in_activation} the result: {status}\n\n") 
            for name, val in sorted(values.items()):
                sat.write(f"  {name} = {val}\n")
            sat.write(f" \n\n")
    else:
        print("No model available (unsat/unknown).")


def justRunATest(in_filename,in_bitvect,in_activation,smt_flag):
    """
    small example of how to use the tool
    """
    nbound=3
    
    T=confifurationsmt_solver(nbound,in_filename,in_bitvect,in_activation,smt_flag)

    
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
        with open(f"results/results{smt_flag}/{smt_flag}_sat_log.txt", "a") as sat:
            sat.write(f"justRunATest with {in_activation} the result: {status}\n\n") 
            for name, val in sorted(values.items()):
                sat.write(f"  {name} = {val}\n")
            sat.write(f" \n\n")
    else:
        print("No model available (unsat/unknown).")

def testGNN(in_dimensions,in_nb_layers,in_max_nb_vertices,in_filename,in_bitvect,in_activation,smt_flag):
    dimension =in_dimensions
    nb_layers = in_nb_layers
    max_nb_vertices = in_max_nb_vertices
    with open(f"results/results{smt_flag}/{smt_flag}log.txt", "a") as f:
        f.write(f"# Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        if smt_flag == 'Z3':
            f.write(f"# test with dimension {dimension}, nb of layers = {nb_layers}, bits -{in_bitvect},activation function-{in_activation}\n")
        else:
            f.write(f"# test with dimension {dimension}, nb of layers = {nb_layers},activation function-{in_activation}\n")
        for N in range(1, max_nb_vertices+1):
            start = time.time()
            T=confifurationsmt_solver(N,in_filename,in_bitvect,in_activation,smt_flag)
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
                with open(f"results/results{smt_flag}/{smt_flag}_sat_log.txt", "a") as sat:
                    sat.write(f"# {smt_flag} test with dimension {dimension}, nb of layers = {nb_layers},activation function-{in_activation}\n")
                    f.write(f"Finished N={N} with {in_activation} the result: {status}\n\n") 
                    for name, val in sorted(values.items()):
                        sat.write(f"  {name} = {val}\n")
                    sat.write(f" \n\n")
            else:
                print("No model available (unsat/unknown).")
            end = time.time()
            f.write(f"Finished N={N} in {end - start:.4f}s\n")
            f.write(f"Finished N={N} with the result: {status}\n\n") 
        f.write("\n")
        f.write("\n")