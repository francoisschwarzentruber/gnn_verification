import torch
import re 

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
    number_of_input_features = 2
    in_filename= in_filename.replace('.smt',f'Nbound{nbound}_simpleACRGNN_bias_{in_activation}_bit_{in_bitvect}.smt')
    v = Z3VerificationTask(Nbound = nbound,filename=in_filename,bitvect=in_bitvect,activation=in_activation,configurations=in_configurations)
    for i in range(number_of_input_features):
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
    number_of_input_features = 3
    in_filename= in_filename.replace('.smt',f'Nbound{nbound}_justRunATest_{in_activation}_bit_{in_bitvect}.smt')
    T = Z3VerificationTask(Nbound = 3,filename=in_filename,bitvect=in_bitvect,activation=in_activation,configurations=in_configurations)
    for i in range(number_of_input_features):
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
                #print('Mvertex',np.shape(Mvertex))
                Magg = [[random.randint(1, 10) for _ in range(dimension)] for _ in range(dimension)]
                #print('Magg',np.shape(Magg))
                Maggglobal = [[random.randint(1, 10) for _ in range(dimension)] for _ in range(dimension)]
                #print('Maggglobal',np.shape(Maggglobal))
                biais = [[random.randint(1, 10)] for _ in range(dimension)]
                #print('biais',np.shape(biais))
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

def trained_models(in_filename,in_configurations):
    '''
    We look on the models trained before.
    '''
    path_to_model_folder='E:/GitHub_Francois/gnn_verification/ModelsforSMT/saved_models/results_synthetic'
    selection='acrgnn_relu/p1/MODEL-acrgnn-0-aggS-readS-combT-cl1-L1-H16.pth'
    selected_model = f"{path_to_model_folder}/{selection}"
    print(f"Loading model from {selected_model}")
    #extract parameters from the name of the model
    #we need to know the activation function, dimension of the hidden layers, number of layers
    act_value = selection.split("acrgnn_")[1].split("/")[0] #selected activation function
    L_value = int(selection.split("-L")[1].split("-")[0]) # number of the layers
    H_value = int(selection.split("-H")[1].split(".")[0]) #number of hidden units, dimesion of the matrices and number of the features
    print(act_value, L_value, H_value)

    #covert act_value to the corresonding value for the solver
    if act_value=='relu':
        activation_function='ReLU'
    elif act_value=='relu6':
        activation_function='ReLU6'
    elif act_value=='trrelu':
        activation_function='trReLU'
    else:
        raise ValueError("Activation function not recognized.")
    # modification of the filename
    in_filename= in_filename.replace('.smt',f'Nbound{H_value}_trained_ACRGNN_L{L_value}_H{H_value}_{act_value}.smt')
    in_bitvect=32

    # state is typically an OrderedDict of parameter tensors
    state = torch.load(selected_model, map_location="cpu")
    
    #print("Model state dictionary:")
    #for k, v in state.items():
    #    print(k, v.shape, v.dtype) 
    
    Nbound=3
    T = Z3VerificationTask(Nbound,H_value,filename=in_filename,bitvect=in_bitvect,activation=act_value,configurations=in_configurations)

    
    for i in range(H_value):
        x = T.add_input_feature()
        for v in range(Nbound):
            T.add_precondition(f"{x}[{v}] == 0 || {x}[{v}] == 1") # need to be fixed 
    # add layers
    for i in range(L_value):
        # --- extract weights ---
        W_C = state[f"convs.{i}.V.linear.weight"].detach().cpu().numpy() 
        b_C = state[f"convs.{i}.V.linear.bias"].detach().cpu().numpy()

        W_A = state[f"convs.{i}.A.linear.weight"].detach().cpu().numpy()
        b_A = state[f"convs.{i}.A.linear.bias"].detach().cpu().numpy()

        W_R = state[f"convs.{i}.R.linear.weight"].detach().cpu().numpy()
        b_R = state[f"convs.{i}.R.linear.bias"].detach().cpu().numpy()

        bias = b_C+b_A+b_R
        bias_vector_to_matrix = bias.reshape(1, -1)
        print(f"Layer {i+1}:")
        print("W_C shape:", W_C.shape)
        print("W_A shape:", W_A.shape)
        print("W_R shape:", W_R.shape)
        print("bias shape:",bias_vector_to_matrix.shape)
        
        T.add_layer(W_C, W_A, W_R, bias_vector_to_matrix)
    #here need to use BatchNorm. We need to add it into class Z3VerificationTask
    #here need to be the layer of the classification 0 1 without the activation function.     
    T.add_postcondition(f"{T.get_last_feature()}[0] >= 0")

    T.check()
    status, values = T.check()
    print("STATUS:", status)




        
   
ACRGNN_configurations = ['Cx+Ay+Rz+b', 'xC+yA+zR+b']
configurations = ACRGNN_configurations[1]  #choose either 'Cx+Ay+Rz+b' or 'xC+yA+zR+b'
'''
activations = ['ReLU','ReLU6','trReLU']
folder = Path(f"results/resultsZ3")
folder.mkdir(parents=True, exist_ok=True)
'''
'''
for act in activations:
    folder_act = Path(f"{folder}/results_{act}")
    folder_act.mkdir(parents=True, exist_ok=True)
    smt_path = folder_act / f"main_{act}.smt"
    testGNN(str(smt_path), 8, act,configurations)


#simpleACRGNN("main.smt",8,'ReLU',configurations)
smt_path = folder / f"main.smt"
simpleACRGNN_bias(str(smt_path),8,'ReLU',configurations)
#justRunATest("main.smt",8,'ReLU',configurations)
'''

trained_models("main.smt",configurations)