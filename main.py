import time
import random
import numpy as np
import sys
from pathlib import Path
from datetime import datetime

from test_functions import simpleACRGNN, simpleACRGNN_bias,justRunATest, testGNN

ACRGNN_configurations = ['Cx+Ay+Rz+b', 'xC+yA+zR+b']
configurations = ACRGNN_configurations[0]  #choose either 'Cx+Ay+Rz+b' or 'xC+yA+zR+b'
SMT= ['ESBMC','Z3']
dimensions = 2
nb_layers =2
max_nb_vertices = 6
for selected_smt in SMT:
    #selected_smt= SMT[0]  #choose either ESBMC or Z3 
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
        with open(f"results/results{selected_smt}/general_{selected_smt}log.txt", "a") as f:
            f.write(f"# Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            if selected_smt == 'Z3':
                f.write(f"# test with, bits -{bitvect},activation function-{act}\n")
            else:
                f.write(f"# test with ,activation function-{act}\n")
            f.write(f"# model testGNN\n")
            print(f"Running testGNN with {selected_smt} and activation {act}")
            start = time.time()
            #simpleACRGNN_bias(str(smt_path),bitvect, act, selected_smt)
            testGNN(dimensions,nb_layers,max_nb_vertices,str(smt_path),bitvect, act, selected_smt,configurations)
            end = time.time()
            f.write(f"Finished in {end - start:.4f}s\n\n") 