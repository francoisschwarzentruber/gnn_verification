import torch
import re 
import os
import time
import random
import numpy as np
from pathlib import Path
from datetime import datetime

import sys

from helpers.analys_help import data_per_layer
from helpers.batch_normalization_linear import apply_bn_inference
from helpers.reform_activation import reform_activation
from helpers.numpy_float32_to_smt_fp import numpy_float32_to_smt_fp

#######################   
# Path to folder
file_path = "./"
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
state = torch.load(selected_model, map_location="cpu")
filename_state = f"{file_path}/{folder_models}/model_{selection}_state_summary.md"

with open(filename_state, "w", encoding="utf-8") as f:
    f.write(f"# Model State Summary for {selection}\n")
    f.write(f"## Activation Function: {state['activation']}\n")
    f.write(f"## Number of parameters: {len(state['state_dict'])}\n")
    f.write("## Keys in state_dict:\n")
    for key in state['state_dict'].keys():
        f.write(f"- {key}\n")

print("Model loaded successfully.")
print("Model activation function:", state['activation'])
#######################
layer_ids = sorted({
    int(k.split(".")[1])
    for k in state["state_dict"]
    if k.startswith("convs.")
    })


with open(filename_state, "a", encoding="utf-8") as f:
    f.write(f"## Layer indices found in state_dict: {layer_ids}\n")

print("Layer indices:", layer_ids)
print("Number of layers:", len(layer_ids))
#######################
# Print parameter counts for the layer
folder = f"{selection}_layers_summary"
path_dir=f'{file_path}/{folder_models}/{folder}'
os.makedirs(f'{path_dir}', exist_ok=True)
for layer in range(len(layer_ids)):
    data_per_layer(state, layer_ids[layer], filename=f"{path_dir}/layer_{layer_ids[layer]}_summary.md")
#######################
#block of the graph initiation, where we extract the parameters of the trained model and prepare them for the SMT encoding.
x=np.array([[0,0,1],[1,0,0]], dtype=np.float32) #default float64
with open(filename_state, "a", encoding="utf-8") as f:
    f.write(f"## Input feature matrix x:\n")
    f.write(f"```\n{x}\n```\n")
    f.write(f"Shape: {x.shape}, Data type: {x.dtype}\n")
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            f.write(f"x[{i},{j}]={x[i,j]} = {numpy_float32_to_smt_fp(x[i,j])}\n")

adj_matrix=np.array([[0,1],[1,0]], dtype=np.float32) #default float64
#######################

#agg_local=np.array([[1,0,0],[0,0,1]], dtype=np.float32) 
agg_local=np.dot(adj_matrix, x) 
# we can also use the adjacency matrix to form the local aggregation,
#  as it is a common way to aggregate the features of the neighboring nodes in GNNs.
#  The local aggregation can be computed as the product of the adjacency matrix and
#  the feature matrix x, which will give us a new matrix where each row corresponds to
#  the aggregated features of the neighboring nodes for each node in the graph.
print("agg_local", agg_local, "shape:", agg_local.shape, agg_local.dtype)
#form the globall aggregation, we need to sum the features of all the nodes in the graph, so we can use a matrix of ones to achieve this.
agg_global = np.sum(x, axis=0)
print("agg_global", agg_global, "shape:", agg_global.shape, agg_global.dtype)
#agg_global=np.array([[1,0,1],[1,0,1]], dtype=np.float32)     

print(state['state_dict'].keys())

#Block of the matrices

# V,A ,R should be transposed to be used in the SMT encoding, as they are stored in the format (output_dim, input_dim)
#in PyTorch, but we need them in the format (input_dim, output_dim) for the SMT encoding. 
#https://docs.pytorch.org/docs/stable/generated/torch.Tensor.numpy.html
V = state['state_dict']['convs.0.V.linear.weight'].numpy(force=True).T
print("V", V, "shape:", V.shape,V.dtype) #check the data type of the weights, as it can affect the SMT encoding. If the weights are in float32, we may need to convert them to a compatible format for SMT solvers, which often require rational numbers or fixed-point representations. If the weights are in a different format (e.g., int8), we may need to adjust our encoding accordingly.
A = state['state_dict']['convs.0.A.linear.weight'].numpy(force=True).T
print("A", A, "shape:", A.shape,A.dtype)
R = state['state_dict']['convs.0.R.linear.weight'].numpy(force=True).T
print("R", R, "shape:", R.shape,R.dtype)
# The biases b_V, b_A, and b_R can be used directly without transposition, 
# as they are stored as 1D tensors of shape (output_dim,) in PyTorch, which is compatible with the SMT encoding.
# these biases shpuld be sumed up. After needed to be stored as matrix. (output_dim,1) in the SMT encoding.
print("Extracting biases...")
print("state['state_dict']['convs.0.V.linear.bias']:", state['state_dict']['convs.0.V.linear.bias'].size())
b_V = state['state_dict']['convs.0.V.linear.bias'].numpy(force=True)
print("b_V", b_V, "shape:", b_V.shape,b_V.dtype)
b_A = state['state_dict']['convs.0.A.linear.bias'].numpy(force=True)
print("b_A", b_A, "shape:", b_A.shape,b_A.dtype)
b_R = state['state_dict']['convs.0.R.linear.bias'].numpy(force=True)
print("b_R", b_R, "shape:", b_R.shape,b_R.dtype)

#for this data we need that each x must have (N,5) features
#so 
if (V.shape[0] != A.shape[0]) and (V.shape[0] != R.shape[0]) and (A.shape[0] != R.shape[0]):
    raise ValueError("Error: The input dimensions of V, A, and R do not match.")   
if (V.shape[1] != A.shape[1]) and (V.shape[1] != R.shape[1]) and (A.shape[1] != R.shape[1]):
    raise ValueError("Error: The output dimensions of V, A, and R do not match.")
if (V.shape[1] != b_V.shape[0]):
    raise ValueError("Error: The output dimensions of V and input dimension of b_V do not match.")
if (A.shape[1] != b_A.shape[0]):
    raise ValueError("Error: The output dimensions of A and input dimension of b_A do not match.")
if (R.shape[1] != b_R.shape[0]):
    raise ValueError("Error: The output dimensions of R and input dimension of b_R do not match.")

in_dimension= V.shape[0]



#enter in conv.layer

xV = np.dot(x, V)
xVb= xV + b_V
print("xV.T+b_V:")
print("xV", xV, "shape:", xV.shape, xV.dtype)
print("xVb", xVb, "shape:", xVb.shape, xVb.dtype)

yA = np.dot(agg_local, A)
yAb = yA + b_A
print("yA.T+b_A:")
print("yA", yA, "shape:", yA.shape, yA.dtype)
print("yAb", yAb, "shape:", yAb.shape, yAb.dtype)

zR = np.dot(agg_global, R)
zRb = zR + b_R
print("zR.T+b_R:")
print("zR", zR, "shape:", zR.shape, zR.dtype)
print("zRb", zRb, "shape:", zRb.shape, zRb.dtype)

update=xVb+yAb+zRb
print("xVb+yAb+zRb:")
print("xVb+yAb+zRb", update, "shape:", update.shape, update.dtype)

print('apply activation function: ReLU')
act=np.maximum(0, update)
print("act", act, "shape:", act.shape, act.dtype)


#Batch Normalization
# Feature after applying the Activation function
# If the model includes batch normalization layers, you can extract their parameters as follows:
bn_a, bn_c = apply_bn_inference(state['state_dict'], f'batch_norms.0') #need to add to the verification task the batch normalization parameters, as they are part of the model's computation.
bn_a = bn_a.numpy(force=True)  
print('bn_a',bn_a,"shape:", bn_a.shape,bn_a.dtype)
bn_c = bn_c.numpy(force=True)  
print('bn_c',bn_c,"shape:", bn_c.shape,bn_c.dtype)

# here we have a*x + c, where a and c are the parameters of the batch normalization layer.
# x is a feature after Activation Function 
print('apply batch normalization')
feature_after_bn = act * bn_a + bn_c
print("feature_after_bn", feature_after_bn, "shape:", feature_after_bn.shape, feature_after_bn.dtype)


#Linear Prediction parameters: output = feature_afterBN*W+bias
#https://docs.pytorch.org/docs/stable/generated/torch.nn.Linear.html
W = state['state_dict']['linear_prediction.weight'].numpy(force=True).T
print('W',W, "shape:", W.shape,W.dtype)
bias = state['state_dict']['linear_prediction.bias'].numpy(force=True)
print('bias',bias, "shape:", bias.shape,bias.dtype)

lp=np.dot(feature_after_bn, W)
lpb=lp + bias
print("Linear prediction output before adding bias:", lp, "shape:", lp.shape, lp.dtype)
print("Linear prediction output:", lpb, "shape:", lpb.shape, lpb.dtype)
#last_features = T.get_last_features(output_dimension)
print("last_features:", np.argmax(lpb, axis=1), "shape:", lpb.shape, lpb.dtype)
