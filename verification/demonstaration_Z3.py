import torch
import re 
import os
import time
import random
import numpy as np
from pathlib import Path
from datetime import datetime

import sys
#######################
from helpers.analys_help import data_per_layer
from helpers.batch_normalization_linear import apply_bn_inference
from helpers.reform_activation import reform_activation

from z3_flow.z3VerificationFloat32 import Z3VerificationFloat32
from z3_flow.utils import numpy_float32_to_smt_fp
#######################

def parse_model_toZ3(state_of_model,file_smt, scheme='xC+b_C',Nnodes=2, Nfeatures=3,node_matrix=None, adj_matrix=None, in_dtype="Float32"):
    #transform the activation function frm state_dict to the format that Z3 knows
    in_activation_value=reform_activation(state_of_model)
    #[todo] think how to add here the alpha for the LeakyReLU
    if scheme!='xC+b_C':
        raise ValueError("Scheme not recognized.")
    
    #we need to extract the parameters of the trained model and prepare them for the SMT encoding.
    #we will use the same notation as in the paper, where:
    # x as the input features, 
    # C as the weight matrix, 
    # b_C as the bias of the weight matrix.
    flag_precondition_0_or_1= False
    flag_postcondition_0_or_1= False

    T = Z3VerificationFloat32(Nnodes,Nfeatures,in_filename_smt=file_smt,in_activation=in_activation_value, in_configurations=scheme,in_dtype=in_dtype) 
    
    if adj_matrix is not None:
        T._add_adj_matrix(adj_matrix) #we can add the adjacency matrix as a comment in the SMT file, as it is part of the model's computation but does not need to be encoded as variables in the SMT problem.
    
    for n in range (0,Nnodes):
        x = T.add_input_node()
        for f in range(0,Nfeatures):
            if node_matrix is None:
                T.add_precondition(f"{x}[{f}] == 0 || {x}[{f}] == 1")
                flag_precondition_0_or_1=True
            else:
                T.add_precondition(f"{x}[{f}] == {node_matrix[n][f]}") #we can add the node features as preconditions in the SMT file, as they are part of the model's computation but do not need to be encoded as variables in the SMT problem.
        if flag_precondition_0_or_1 == True:
            T._addLineInMain(f";; Node {n} features are binary (0 or 1)")
            T.add_one_hot_row_precondition(x, Nfeatures)   
    # add layers
    NumberOfLayers = len([k for k in state_of_model if k.startswith("convs.") and k.endswith(".linear.weight")])    
    for layer in range(0, NumberOfLayers+1):
        V = state_of_model['state_dict'][f'convs.{layer}.V.linear.weight'].numpy(force=True).T
        A = state_of_model['state_dict'][f'convs.{layer}.A.linear.weight'].numpy(force=True).T
        R = state_of_model['state_dict'][f'convs.{layer}.R.linear.weight'].numpy(force=True).T

        b_V = state_of_model['state_dict'][f'convs.{layer}.V.linear.bias'].numpy(force=True)
        b_A = state_of_model['state_dict'][f'convs.{layer}.A.linear.bias'].numpy(force=True)
        b_R = state_of_model['state_dict'][f'convs.{layer}.R.linear.bias'].numpy(force=True)

        #Batch Normalization
        # Feature after applying the Activation function
        # If the model includes batch normalization layers, you can extract their parameters as follows:
        bn_a, bn_c = apply_bn_inference(state['state_dict'], f'batch_norms.0') #need to add to the verification task the batch normalization parameters, as they are part of the model's computation.
        bn_a = bn_a.numpy(force=True)  
        bn_c = bn_c.numpy(force=True)  
        T.add_layer(V,A,R,b_V,b_A,b_R,bn_a,bn_c)
    
    # add linear prediction layer
    W = state_of_model['state_dict']['linear_prediction.weight'].numpy(force=True).T
    bias = state_of_model['state_dict']['linear_prediction.bias'].numpy(force=True)

    T.add_linear_prediction_layer(W, bias)
    
    last_features = T.get_lasts(2)
    print('last_features', last_features)
    if flag_postcondition_0_or_1 == True:
        #Find me a counterexample where node 0 is not class 0 and node 1 is not class 1.
        T.add_postcondition(f"{last_features[0]}[0] == 0")
        T.add_postcondition(f"{last_features[1]}[0] == 1")
    
    T.check(get_model=True,model_filename="model.smt2")
    
def parse_model_inference_without_architecture(state_of_model,file, scheme='xC+b_C',node_matrix=np.array([[0,0,1],[1,0,0]], dtype=np.float32), adj_matrix=np.array([[0,1],[1,0]], dtype=np.float32), in_dtype="Float32" ):
    #transform the activation function frm state_dict to the format that Z3 knows
    in_activation_value=reform_activation(state_of_model)
    #[todo] think how to add here the alpha for the LeakyReLU
    
    index_of_node=0 #[todo] think how I could add x0,x1 to the computations
    
    if scheme!='xC+b_C':
        raise ValueError("Scheme not recognized.")
    if node_matrix is None:
        raise ValueError("No Graph provided.")
    if adj_matrix is None:
        raise ValueError("No adjacency matrix provided.")
    Nnodes=node_matrix.shape[0]
    Nfeatures=node_matrix.shape[1]

    with open(file, "w", encoding="utf-8") as f:
        f.write(f"Activation function: {in_activation_value}\n")
        f.write(f"Scheme: {scheme}\n")
        f.write(f"Input node features:\n{node_matrix}\n")
        for i in range(node_matrix.shape[0]):
            for j in range(node_matrix.shape[1]):
                f.write(f"x{i}_{j}={node_matrix[i][j]}={numpy_float32_to_smt_fp(node_matrix[i][j])}\n")
        f.write(f"Adjacency matrix:\n{adj_matrix}\n")
        f.write(f"Input data type: {in_dtype}\n")

        agg_local=np.dot(adj_matrix, node_matrix)
        f.write(f"Local Aggregation:\n{agg_local}\n")
        
        agg_global = np.sum(node_matrix, axis=0)
        f.write(f"Global Aggregation:\n{agg_global}\n")
        
        f.write(f"Layer computations:\n")
        # add layers
        NumberOfLayers = len([k for k in state_of_model if k.startswith("convs.") and k.endswith(".linear.weight")])    
        f.write(f"Computations for {NumberOfLayers+1} layers\n")
        
        
        for layer in range(0, NumberOfLayers+1):
            f.write(f"Layer: {layer}\n")
            V = state_of_model['state_dict'][f'convs.{layer}.V.linear.weight'].numpy(force=True).T
            A = state_of_model['state_dict'][f'convs.{layer}.A.linear.weight'].numpy(force=True).T
            R = state_of_model['state_dict'][f'convs.{layer}.R.linear.weight'].numpy(force=True).T

            b_V = state_of_model['state_dict'][f'convs.{layer}.V.linear.bias'].numpy(force=True)
            b_A = state_of_model['state_dict'][f'convs.{layer}.A.linear.bias'].numpy(force=True)
            b_R = state_of_model['state_dict'][f'convs.{layer}.R.linear.bias'].numpy(force=True)

            xV = np.dot(node_matrix, V)
            f.write(f"xV:\n{xV}\n")
            xVb= xV + b_V
            f.write(f"xV + b_V:\n{xVb}\n")

            yA = np.dot(agg_local, A)
            f.write(f"yA:\n{yA}\n")
            yAb = yA + b_A
            f.write(f"yA + b_A:\n{yAb}\n")

            zR = np.dot(agg_global, R)
            f.write(f"zR:\n{zR}\n")
            zRb = zR + b_R
            f.write(f"zR + b_R:\n{zRb}\n")

            update=xVb+yAb+zRb
            f.write(f"(xV + b_V) + (yA + b_A) + (zR + b_R):\n{update}\n")
            if in_activation_value == 'ReLU':
                act=np.maximum(0, update)
                f.write(f"{in_activation_value}:\n{act}\n")
            else:
                raise ValueError("Activation function not ReLU, need additional inmplementations.")
            #Batch Normalization
            # Feature after applying the Activation function
            # If the model includes batch normalization layers, you can extract their parameters as follows:
            bn_a, bn_c = apply_bn_inference(state_of_model['state_dict'], f'batch_norms.{layer}') #need to add to the verification task the batch normalization parameters, as they are part of the model's computation.
            bn_a = bn_a.numpy(force=True)  
            bn_c = bn_c.numpy(force=True)

            feature_after_bn = act * bn_a + bn_c
            f.write(f"Batch Normalization:\n{feature_after_bn}\n")
            f.write(f'Computations for the layer {layer} are finished.\n')
            if (NumberOfLayers+1 > 1) and (layer < NumberOfLayers+1):
                f.write(f'Form new matrices for the next layer: {layer+1}')
                node_matrix=feature_after_bn

                agg_local=np.dot(adj_matrix, node_matrix)
                f.write(f"Local Aggregation:\n{agg_local}\n")
                
                agg_global = np.sum(node_matrix, axis=0)
                f.write(f"Global Aggregation:\n{agg_global}\n")

        f.write('Linear Prediction\n')
        W = state_of_model['state_dict']['linear_prediction.weight'].numpy(force=True).T
        bias = state_of_model['state_dict']['linear_prediction.bias'].numpy(force=True)

        lp=np.dot(feature_after_bn, W)
        f.write(f"Linear prediction output before adding bias:\n{lp}\n")
        lpb=lp + bias
        f.write(f"Linear prediction output:\n{lpb}\n")
        classes=np.argmax(lpb, axis=1)
        f.write(f"Binary classification:\n")
        for i in range(len(classes)):
            f.write(f'node {i} was classified as {classes[i]}\n')
        f.write(f"Computations are finished\n")


    



    






#######################   
# Path to folder
file_path = "E:/GitHub_Francois/verification/"
folder_models = "Models"
#Path to the model
path_to_model_folder=f'{file_path}{folder_models}/saved_models/results_synthetic'
#######################
#detailed spesification of the path
#detailes that we can get from the input models'
#######################
activation = "relu"
key = "p0"
epoch = 40
layer = 1
hidden_dimension = 3
learning_rate = 0.01
#######################
additional_path = f'acrgnn_{activation}/{key}/{epoch}'
selection=f'MODEL-acrgnn-0-aggS-readS-combT-cl1-L{layer}-H{hidden_dimension}-epoch{epoch}-lr{learning_rate}'
#######################
selected_model = f"{path_to_model_folder}/{additional_path}/{selection}.pth"
print(f"Loading model from {selected_model}")
#######################
# state is typically an OrderedDict of parameter tensors
state = torch.load(selected_model, map_location="cpu",weights_only=True)
#######################
#Example1 p0_2
#block of the graph initiation, where we extract the parameters of the trained model and prepare them for the SMT encoding.
x_ex1=np.array([[0,0,1],[1,0,0]], dtype=np.float32) #default float64
adj_matrix_ex1=np.array([[0,1],[1,0]], dtype=np.float32) #default float64
#######################
#Example2
x_ex2=np.array([[0,1,0],[0,1,0]], dtype=np.float32) #default float64
adj_matrix_ex2=np.array([[0,1],[1,0]], dtype=np.float32) #default float64
#######################
#Example3
x_ex3=np.array([[0,0,1],[0,1,0]], dtype=np.float32) #default float64
adj_matrix_ex3=np.array([[1,1],[1,0]], dtype=np.float32) #default float64
#######################
#Example4 p0_3
x_ex4=np.array([[1,0,0],[0,1,0],[0,0,1]], dtype=np.float32) #default float64
adj_matrix_ex4=np.array([[0,1,1],[1,0,1],[1,1,0]], dtype=np.float32) #default float64
#######################
#Example5 p0_4
x_ex5=np.array([[0,1,0],[0,1,0],[0,1,0],[0,0,1]], dtype=np.float32) #default float64
adj_matrix_ex5=np.array([[0,1,1,0],[1,0,1,1],[1,1,0,0],[0,1,0,0]], dtype=np.float32) #default float64
#######################
#Example6 Complete
#block of the graph initiation, where we extract the parameters of the trained model and prepare them for the SMT encoding.
x_ex6=np.array([[0,0,1],[1,0,0]], dtype=np.float32) #default float64
adj_matrix_ex6=None
#######################

# Selection of the example to run
x_selected=None
adj_matrix_selected=adj_matrix_ex2
#postfix = "example6_postconditions"
N_nodes = 2
N_features = 3

#######################
#x_selected=None
#adj_matrix_selected=None
postfix = "example6"
#N_nodes = 2
#N_features = 3
os.makedirs(f'{postfix}', exist_ok=True)
possible_dtypes=['Float32']
#######################
for selected_dtype in possible_dtypes:
    parse_model_toZ3(state_of_model=state, file_smt=os.path.join(postfix, f"test_case_{selected_dtype}.smt2"), scheme='xC+b_C',Nnodes=N_nodes, Nfeatures=N_features,node_matrix=x_selected, adj_matrix=adj_matrix_selected, in_dtype=selected_dtype)
#parse_model_inference_without_architecture(state_of_model=state, file=os.path.join(postfix, "test_case.md"), scheme='xC+b_C',node_matrix=x_selected, adj_matrix=adj_matrix_selected, in_dtype="Float32")
'''
for i in range(2,16):
    N_nodes = i
    N_features = 3
    parse_model_toZ3(state_of_model=state, file_smt=f"test_case_{postfix}.smt2", scheme='xC+b_C',Nnodes=N_nodes, Nfeatures=N_features,node_matrix=None, adj_matrix=None, in_dtype="Float32")
'''
