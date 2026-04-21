def data_per_layer(state, layer_idx, filename=None):
    if filename is None:
        filename = f"layer_{layer_idx}_summary.md"

    with open(filename, "w", encoding="utf-8") as f:
        activation = state["activation"]
        
        f.write(f"# {layer_idx + 1}-Layer of the ACR-GNN with Activation: {activation}.\n")

        state_dict = state["state_dict"]
        

        if not any(k.startswith(f"convs.{layer_idx}.") for k in state_dict):
            raise ValueError(f"No parameters found for layer {layer_idx + 1}.")
        
        f.write(f"## Parameters for layer {layer_idx + 1}.\n")
        f.write('### Matrices and Biases. Description and checking.\n')
        
        #----Matrices with bias Description and checking----#
        num_mb_parameters = sum(
            1 for k in state_dict
            if k.startswith(f"convs.{layer_idx}.") and ("weight" in k or "bias" in k)
        )
        f.write(f"- Number of Matrices with Biases: {num_mb_parameters}.\n")
        
        if num_mb_parameters != 6:  
            raise ValueError(f"Warning: Expected 6 parameters for layer {layer_idx} (V, A, R weights and biases), but found {num_mb_parameters}.\n")
        else:
            f.write(f"- Found expected number of parameters for layer {layer_idx + 1}.\n")

        shapes_matrices = []
        shapes_biases  = []
        for matrix in ["V", "A", "R"]:
            weight_key = f"convs.{layer_idx}.{matrix}.linear.weight"
            
            bias_key = f"convs.{layer_idx}.{matrix}.linear.bias"
            
            if weight_key not in state_dict:
                raise ValueError(f"Warning: Missing weight for {matrix} in layer {layer_idx}.")
            else:
                shapes_matrices.append(state_dict[weight_key].shape)
                f.write(f"- Found weight for `{matrix}` in layer {layer_idx + 1}, shape: {state_dict[weight_key].shape}, dtype: {state_dict[weight_key].dtype}\n")
            if bias_key not in state_dict:
                raise ValueError(f"Warning: Missing bias for {matrix} in layer {layer_idx}.")
            else:
                shapes_biases.append(state_dict[bias_key].shape)
                f.write(f"- Found bias for `{matrix}` in layer {layer_idx + 1}, shape: {state_dict[bias_key].shape}, dtype: {state_dict[bias_key].dtype}\n")

        if len(set(shapes_matrices)) > 1:
            raise ValueError(f"Warning: Inconsistent shapes for weights in layer {layer_idx}: {shapes_matrices}")
        else:
            f.write('> [!NOTE]\n')
            f.write(f"> Weights for layer {layer_idx+1} have consistent shape: {shapes_matrices[0]}\n")
        if len(set(shapes_biases)) > 1:
            raise ValueError(f"Warning: Inconsistent shapes for biases in layer {layer_idx}: {shapes_biases}")
        else:
            f.write('> [!NOTE]\n')
            f.write(f"> Biases for layer {layer_idx+1} have consistent shape: {shapes_biases[0]}\n\n")
        
        if shapes_matrices and shapes_biases and shapes_matrices[0][0] != shapes_biases[0][0]:
            raise ValueError(f"Warning: Output dimension of weights {shapes_matrices[0][0]} does not match output dimension of biases {shapes_biases[0][0]} in layer {layer_idx+1}.")    
        else:
            f.write('> [!NOTE]\n')
            f.write(f"> Output dimensions of weights and biases match for layer {layer_idx + 1}.\n")

        #----Batch Normalization Description and checking----#
        f.write('### Batch Normalization Description and checking:\n')
        #calculate number of the Batch Normalization parameters.
        num_bn_parameters = sum(
            1 for k in state_dict if k.startswith(f"batch_norms.{layer_idx}.")
        )
        f.write(f"- Batch Normalization parameters: {num_bn_parameters}\n")
        #Output is 5, but we care during the inference about weight, bias, running_mean, running_var
        if num_bn_parameters == 5:
            f.write('> [!NOTE]\n')
            f.write(f"> Output is 5, but we care during the inference about weight, bias, running_mean, running_var\n")
        # required parameters for batch normalization: weight, bias, running_mean, running_var
        shapes_bn = []
        for parameter in ["weight", "bias", "running_mean", "running_var"]:
            if f"batch_norms.{layer_idx}.{parameter}" not in state_dict:
                f.write(f"Warning: Missing batch normalization parameter '{parameter}' for layer {layer_idx+1}.\n")
            else:
                f.write(f"- Found Batch Normalization parameter `{parameter}` for layer {layer_idx+1}.\n")
                shapes_bn.append(state_dict[f"batch_norms.{layer_idx}.{parameter}"].shape)

        if len(set(shapes_bn)) > 1:
            raise ValueError(f"Warning: Inconsistent shapes for batch normalization parameters in layer {layer_idx}: {shapes_bn}")
        else:
            f.write('> [!NOTE]\n')
            f.write(f"> Batch normalization parameters for layer {layer_idx + 1} have consistent shape: {shapes_bn[0]}\n")

 