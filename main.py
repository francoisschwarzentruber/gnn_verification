import time
import random
import numpy as np
from pathlib import Path
from datetime import datetime

import sys
from pathlib import Path

from esbmc_flow.ESBMCVerificationTask import ESBMCVerificationTask
from z3_flow.z3VerificationTask import Z3VerificationTask

def confifurationsmt_solver(nbound,in_filename,in_bitvect,in_activation,smt_flag):
    if smt_flag == 'Z3':
        in_filename= in_filename.replace('.smt',f'Nbound{nbound}_simpleACRGNN_{in_activation}.smt')
        v = Z3VerificationTask(nbound,filename=in_filename,bitvect=in_bitvect,activation=in_activation)
    elif smt_flag == 'ESBMC':
        in_filename= in_filename.replace('.c',f'Nbound{nbound}_simpleACRGNN_{in_activation}.c')
        v = ESBMCVerificationTask(nbound,filename=in_filename,activation=in_activation)
    else:
        raise ValueError(f"Unsupported SMT solver: {smt_flag}")
    return v


def simpleACRGNN(in_filename,in_bitvect,in_activation,smt_flag):
    nbound=2
    if smt_flag == 'Z3':
        in_filename= in_filename.replace('.smt',f'Nbound{nbound}_simpleACRGNN_{in_activation}.smt')
        v = Z3VerificationTask(nbound,filename=in_filename,bitvect=in_bitvect,activation=in_activation)
    elif smt_flag == 'ESBMC':
        in_filename= in_filename.replace('.c',f'Nbound{nbound}_simpleACRGNN_{in_activation}.c')
        v = ESBMCVerificationTask(nbound,filename=in_filename,activation=in_activation)
    
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


def justRunATest(in_filename,in_bitvect,in_activation,smt_flag):
    """
    small example of how to use the tool
    """
    nbound=3
    in_filename= in_filename.replace('.smt',f'Nbound{nbound}_justRunATest_{in_activation}_bit_{in_bitvect}.smt')
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

















SMT= ['ESBMC','Z3']
selected_smt= SMT[1]  #choose either Z3 or ESBMC
activations = ['ReLU','ReLU6','trReLU']
bitvect = 8 #bitvector size for Z3

folder = Path(f"results/results{selected_smt}")
folder.mkdir(parents=True, exist_ok=True)

for act in activations:
    folder_act = Path(f"{folder}/results_{act}")
    folder_act.mkdir(parents=True, exist_ok=True)
    if selected_smt == 'ESBMC':
        smt_path = folder_act / f"main_{act}.c"
    elif selected_smt == 'Z3':
        smt_path = folder_act / f"main_{act}.smt"
    else:
        raise ValueError(f"Unsupported SMT solver: {selected_smt}")
    simpleACRGNN(str(smt_path),bitvect, act, selected_smt)