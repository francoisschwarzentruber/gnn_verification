import time
import random
import numpy as np
from pathlib import Path
from datetime import datetime

import sys
from pathlib import Path

import torch
from torch import unsqueeze

from ESBMCVerificationTask import ESBMCVerificationTask

def activation_function_mapping(act:str)->str: #put in separate file 
    '''
    Map the activation function name to the corresponding representation used in the Z3VerificationTask.
    '''
    mapping = {
        'relu': 'ReLU',
        'relu6': 'ReLU6',
        'trrelu': 'trReLU'
    }
    if act in mapping:
        return mapping[act]
    else:
        raise ValueError(f"Unsupported activation function: {act}")


def extract_parameters_from_name_of_model(selection): #put in separate file
    '''
    Extract parameters from the name of the model
    We need to know the activation function, dimension of the hidden layers, number of layers
    '''
    act_value = selection.split("acrgnn_")[1].split("/")[0] #selected activation function
    act_value=activation_function_mapping(act_value)
    L_value = int(selection.split("-L")[1].split("-")[0]) # number of the layers
    H_value = int(selection.split("-H")[1].split("-")[0]) if "quantized" in selection else int(selection.split("-H")[1].split(".")[0])# number of hidden units, dimesion of the matrices and number of the features
    bit_value = int(selection.split("-quantized")[0].split("-")[-1]) if "quantized" in selection else 32 # number of hidden units, dimesion of the matrices and number of the features
    return act_value, L_value, H_value, bit_value

def trained_model_fp32(in_filename, in_configurations):
    path_to_model_folder='E:/GitHub_Francois/gnn_verification/ModelsforSMT/saved_models/results_synthetic'
    additional_path='acrgnn_relu/p1'
    selection=f'{additional_path}/MODEL-acrgnn-0-aggS-readS-combT-cl1-L1-H16.pth'
    selected_model = f"{path_to_model_folder}/{selection}"
    print(f"Loading model from {selected_model}")

    in_activation, in_n_layers, in_dimension_of_hidden_layers,in_bitvect= extract_parameters_from_name_of_model(selection)
    
    # state is typically an OrderedDict of parameter tensors
    state = torch.load(selected_model, map_location="cpu")
    
    print("Model state dictionary:")
    print(type(state), len(state))
    print("keys:", list(state.keys()))

    #selection of the weights and biases of the first layer
    #need to be extracted in automatic way, not hardcoded, because we want to be able to test different models with different number of layers and different dimensions of hidden layers
    prefixes = [
    "convs.0.V.linear",
    "convs.0.A.linear",
    "convs.0.R.linear"
    ]
    max_nb_vertices = 16
    with open(f"results/resultsESBMC/ESBMClog.txt", "a") as f:
        f.write(f"# Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# test with dimension {in_dimension_of_hidden_layers}, nb of layers = {in_n_layers},activation function-{in_activation}\n")
        base = in_filename.replace(".c", "")  
        for N in range(1, max_nb_vertices+1):
            filename_N = f"{base}_Nbound{N}_testGNN.c"
            start = time.time()
            print(in_configurations)
            T = ESBMCVerificationTask(Nbound = N,type="float",filename=filename_N,activation=in_activation,confifuration_matrices=in_configurations)
            for i in range(in_dimension_of_hidden_layers):
                x = T.add_input_feature()
                for v in range(N):
                    print(f"Adding precondition for vertex {v} and feature {i}")
                    T.add_precondition(f"{x}[{v}] == 0 || {x}[{v}] == 1")
                               
            for i in range(in_n_layers):
                Mvertex = state[f'convs.{i}.V.linear.weight'].tolist()
                vertex_bias = state[f'convs.{i}.V.linear.bias'].unsqueeze(0).tolist()
                print('Mvertex',np.shape(Mvertex),np.shape(vertex_bias))
                
                Magg = state[f'convs.{i}.A.linear.weight'].tolist()
                agg_bias = state[f'convs.{i}.A.linear.bias'].unsqueeze(0).tolist()
                print('Magg',np.shape(Magg))
                Maggglobal = state[f'convs.{i}.R.linear.weight'].tolist()
                aggglobal_bias = state[f'convs.{i}.R.linear.bias'].unsqueeze(0).tolist()
                print('Maggglobal',np.shape(Maggglobal))
                biais = [[vertex_bias[0][j]+agg_bias[0][j]+aggglobal_bias[0][j] for j in range(len(vertex_bias[0]))]]
                print('biais',np.shape(biais))
                T.add_layer(Mvertex, Magg, Maggglobal, biais)
            print(f"Adding postcondition for N={N}")
            T.add_postcondition(f"{T.get_last_feature()}[0] >= 0")
            
            print("Adding check")
            T.check()
            end = time.time()
            
            f.write(f"Finished N={N} in {end - start:.4f}s\n\n") 
        f.write("\n")
        f.write("\n")







ACRGNN_configurations = ['Cx+Ay+Rz+b', 'xC+yA+zR+b']
configurations = ACRGNN_configurations[1]  #choose either 'Cx+Ay+Rz+b' or 'xC+yA+zR+b'
folder = Path(f"results/resultsESBMC")
folder.mkdir(parents=True, exist_ok=True)

smt_path = folder / f"main.c"
trained_model_fp32(str(smt_path),configurations)


