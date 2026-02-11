'''
Docstring for quantization

Here our goal is to quantize floating point numbers to integers
using a given scale and bitwidth.
This type of the Quantization that can apply is the Post-Training Quantization (PTQ).
Scheme of the quantization - uniform quantization.
We took a pre-trained model(s) in the floating point (FP32) format.
Enabling integer (INT8) inference without the need for retraining or fine-tuning the model.
For this we require two fundamental operations: quantization and dequantization.
The quantization process maps floating point values to integers using a scale factor and zero point.
The dequantization process maps integers back to floating point values using the same scale factor and zero point.
'''


import numpy as np
import math

def scale_symmetric(tensor,bitwidth):
    r_min=np.min(tensor)
    r_max=np.max(tensor)
    return (2*np.maximum(np.abs(r_min),np.abs(r_max)))/(2**(bitwidth)-1)

def scale_asymmetric(tensor,bitwidth):
    r_min=np.min(tensor)
    r_max=np.max(tensor)
    return (r_max-r_min)/(2**(bitwidth)-1)

def zero_point_asymmetric(tensor,bitwidth):
    r_min=np.min(tensor)
    r_max=np.max(tensor)
    scale=scale_asymmetric(tensor,bitwidth)
    return round(round(round(r_min/scale)+round(r_max/scale+1))/2)


def quantize_to_int(x: np.ndarray, bitwidth: int, scheme: str) -> np.ndarray:
    '''
    Quantize the input floating point array to integers using the given scale and zero point.

    Parameters:
    x (np.ndarray): Input floating point array.
    bitwidth (int): Bitwidth for quantization (e.g., 8 for int8).
    scale (float): Scale factor for quantization.
    zero_point (int): Zero point for quantization.

    Returns:
    np.ndarray: Quantized integer array.
    '''
    # calculate the uniform quantization range

    if scheme == 'symmetric':
        # symmetric quantization
        scale = scale_symmetric(x,bitwidth)
        zero_point = 0
    elif scheme == 'asymmetric':
        # asymmetric quantization
        scale = scale_asymmetric(x,bitwidth)
        zero_point = zero_point_asymmetric(x,bitwidth)
    else:
        raise ValueError("Unsupported quantization scheme. Use 'symmetric' or 'asymmetric'.")

    return np.round(x / scale) + zero_point

'''
Test cases
'''
if __name__ == "__main__":
    # Example usage
    x = np.array([-1.0, -0.5, 0.0, 0.5, 1.0], dtype=np.float32)
    bitwidth = 8
    print("Original:", x)
    quantized_symmetric = quantize_to_int(x, bitwidth, scheme='symmetric')
    print("Quantized (symmetric):", quantized_symmetric)

    quantized_asymmetric = quantize_to_int(x, bitwidth, scheme='asymmetric')
    print("Quantized (asymmetric):", quantized_asymmetric)