import torch
import re 
import os
import time
import random
import numpy as np
from pathlib import Path
from datetime import datetime

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from scipy.stats import norm, skew, kurtosis


def activation_function_mapping(act:str)->str:
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

def extract_parameters_from_name_of_model(selection):
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

def check_int_to_float(tensor):
    # reconstruct real matrix manually
    W_int = tensor.int_repr()
    scale = tensor.q_scale()
    zero_point = tensor.q_zero_point()
    W_manual = (W_int.float() - zero_point) * scale
    return torch.allclose(W_manual, tensor.dequantize())  # should be True

def unpack_qlinear_from_state(state, prefix: str):
    print(f"Unpacking quantized linear layer with prefix: {prefix}")
    out_scale = state[f"{prefix}.scale"]
    out_zp    = state[f"{prefix}.zero_point"]
    packed    = state[f"{prefix}._packed_params._packed_params"]
    dtype     = state[f"{prefix}._packed_params.dtype"]

    # Unpack packed params -> (quantized_weight, bias)
    weight_matrix, bias = packed
    print(f"Unpacked weight shape: {weight_matrix}, bias shape: {bias}")
    info = {
        "prefix": prefix,
        "dtype": str(dtype) if dtype is not None else None,
        "out_scale": out_scale,
        "out_zero_point": out_zp,
        'quantized_weights': weight_matrix,
        'quantized_weights_dtype': weight_matrix.dtype,
        'quantized_weights_shape': weight_matrix.shape,
        'quantized_weight_exactly_in_int8': weight_matrix.int_repr(),
        'bias': bias,
        'bias_dtype': bias.dtype if bias is not None else None,
        'bias_shape': bias.shape if bias is not None else None
    }
    print('check_int_to_float(weight_matrix):', check_int_to_float(weight_matrix))
    return weight_matrix.int_repr().tolist(),bias.tolist()

def apply_bn_inference(x, bn_state, prefix="batch_norms.0", eps=1e-5): # need to be added to layer into class Z3 and ESBMC
    """
    x: Tensor shaped [N, C] or [*, C] depending on your model (C is feature dim).
    bn_state: state_dict-like mapping
    """
    gamma = bn_state[f"{prefix}.weight"]        # gamma (learned scale)
    beta = bn_state[f"{prefix}.bias"]          # beta (learned shift)
    mu = bn_state[f"{prefix}.running_mean"] # mu (EMA mean)
    sigma = bn_state[f"{prefix}.running_var"]  # var (EMA variance) sigma**2

    # training=False forces use of running stats
    y = gamma * (x - mu) / torch.sqrt(sigma + eps) + beta
    return y


def analysis_of_weights(
    t,
    title,
    bins=100,
    lim=None,
    show_stats=True,
    save_dir=None,
    filename=None,
    dpi=300,
    show=False
):
    """
    Plot histogram of tensor values with fitted normal distribution
    and optionally save it to disk.

    Parameters
    ----------
    t : torch.Tensor
        FP32 tensor
    title : str
        Plot title
    bins : int
        Number of bins
    lim : tuple or None
        (xmin, xmax) axis limits
    show_stats : bool
        Show skewness and kurtosis
    save_dir : str or None
        Directory where the plot is saved
    filename : str or None
        Output filename (without extension)
    dpi : int
        Resolution for saved figure
    show : bool
        Whether to display the plot interactively
    """

    x = t.detach().cpu().flatten().numpy()

    mu = x.mean()
    sigma = x.std()
    s = skew(x)
    k = kurtosis(x)
    sparsity = (t == 0).float().mean()
    print(f"{title}: mean={mu:.2e}, std={sigma:.2e}, skew={s:.2f}, kurtosis={k:.2f}, sparsity={sparsity:.2f}    ")
    print(f"{title}: {mu:.2e} & {sigma:.2e} & {s:.2f} & {k:.2f} & {sparsity:.2f}    ")

    plt.figure()
    plt.hist(x, bins=bins, density=True, alpha=0.6, label="Empirical")

    xmin, xmax = plt.xlim()
    xx = np.linspace(xmin, xmax, 1000)
    pdf = norm.pdf(xx, mu, sigma)

    plt.plot(
        xx, pdf,
        linewidth=2,
        label=f"N(μ={mu:.2e}, σ={sigma:.2e})"
    )

    if lim is not None:
        plt.xlim(lim)

    if show_stats:
        plt.title(f"{title}\nskew={s:.2f}, kurt={k:.2f}")
    else:
        plt.title(title)

    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    if save_dir is not None:
        os.makedirs(save_dir, exist_ok=True)

        if filename is None:
            safe_title = title.replace(" ", "_").replace(".", "")
            filename = safe_title

        path = os.path.join(save_dir, f"{filename}.png")
        plt.savefig(path, dpi=dpi, bbox_inches="tight")

    if show:
        plt.show()

    plt.close()

def trained_models_float32():
    '''
    For this case we are usung the models that were trained in float32, not quantized
    '''
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


    #lets analyse the weights
    # input - (V , A , R) - BatchNorm - linear_prediction - output
    #steps to do:
    # 1) get the input x (we can use random input for that, just to see how the quantization works)
    # 2) pass it through V, A, R to get h: h= ReLU(xV + yA + zR + b)
    # this need to be added to the ESBMC flow and Z3 flow
    # 3) pass h through BatchNorm 
    # 4) pass it through linear_prediction to get output: output=linear_prediction(BatchNorm(h))
    #these prefixes only for the one layer model. We know by the design that we have three matrices: V,A,R for the convolution and one final linear layer for the prediction
    prefixes = [
    "convs.0.V.linear",
    "convs.0.A.linear",
    "convs.0.R.linear"#linear_prediction is the final quantized affine layer that produces the model’s output, and its scale / zero_point define how integer results are converted back to real values before BatchNorm.
    ]
    save_dir = f"results/figures/weight/fp32_distributions/H{in_dimension_of_hidden_layers}/L{in_n_layers}/{in_activation}"
    for i in range(len(prefixes)):
        analysis_of_weights(
            state[prefixes[i]+".weight"],
            f"FP32 Layer {prefixes[i].split('.')[1]} {prefixes[i].split('.')[2]} weights",
            save_dir=save_dir,
            filename=f"FP32 Layer {prefixes[i].split('.')[1]} {prefixes[i].split('.')[2]} weights".replace(" ","_")
        )
        analysis_of_weights(
            state[prefixes[i]+".bias"],
            f"FP32 Layer {prefixes[i].split('.')[1]} {prefixes[i].split('.')[2]} bias",
            save_dir=save_dir,
            filename=f"FP32 Layer {prefixes[i].split('.')[1]} {prefixes[i].split('.')[2]} bias".replace(" ","_")
        )
    analysis_of_weights(
        state['linear_prediction.weight'],
        f"FP32 Linear Prediction weights",
        save_dir=save_dir,
        filename=f"FP32 Linear Prediction weights"
    )
    analysis_of_weights(
        state['linear_prediction.bias'],
        f"FP32 Linear Prediction bias",
        save_dir=save_dir,
        filename=f"FP32 Linear Prediction bias"
    )
    print(state['linear_prediction.bias'].tolist())
    
def trained_models_quantized():
    '''
    For this case we are usung the models that were quantized via PyTorch, dynamic PTQ from float32 to qint8
    '''
    path_to_model_folder='E:/GitHub_Francois/gnn_verification/ModelsforSMT/saved_models/results_synthetic'
    additional_path='acrgnn_relu/p1'
    selection=f'{additional_path}/MODEL-acrgnn-0-aggS-readS-combT-cl1-L1-H16-8-quantized.pth'
    selected_model = f"{path_to_model_folder}/{selection}"
    print(f"Loading model from {selected_model}")

    in_activation, in_n_layers, in_dimension_of_hidden_layers,in_bitvect= extract_parameters_from_name_of_model(selection)
    
    # state is typically an OrderedDict of parameter tensors
    state = torch.load(selected_model, map_location="cpu")
    
    print("Model state dictionary:")
    print(type(state), len(state))
    print("keys:", list(state.keys()))

    #these prefixes only for the one layer model. We know by the design that we have three matrices: V,A,R for the convolution and one final linear layer for the prediction
    prefixes = [
    "convs.0.V.linear",
    "convs.0.A.linear",
    "convs.0.R.linear",
    "linear_prediction",#linear_prediction is the final quantized affine layer that produces the model’s output, and its scale / zero_point define how integer results are converted back to real values before BatchNorm.
    ]
    print(unpack_qlinear_from_state(state, prefixes))
    #lets analyse the weights
    # input - (V , A , R) - BatchNorm - linear_prediction - output
    #steps to do:
    # 1) get the input x (we can use random input for that, just to see how the quantization works)
    # 2) pass it through V, A, R to get h: h= ReLU(xV + yA + zR + b)
    # 3) pass h through BatchNorm
    # 4) pass it through linear_prediction to get output: output=linear_prediction(BatchNorm(h))
    analysis_of_weights(state, prefixes[0])

    
    
    
trained_models_float32()