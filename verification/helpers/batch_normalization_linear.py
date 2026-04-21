import torch

def apply_bn_inference(bn_state, prefix, eps=1e-5): 
    """
    x: Tensor shaped [N, C] or [*, C] depending on your model (C is feature dim).
    bn_state: state_dict-like mapping
    """
    gamma = bn_state[f"{prefix}.weight"]        # gamma (learned scale)
    beta = bn_state[f"{prefix}.bias"]          # beta (learned shift)
    mu = bn_state[f"{prefix}.running_mean"] # mu (EMA mean)
    sigma = bn_state[f"{prefix}.running_var"]  # var (EMA variance) sigma**2
    #print(f"BatchNorm parameters for {prefix}:")
    #print(f"gamma (weight): {gamma}, shape: {gamma.shape}, dtype: {gamma.dtype}")
    #print(f"beta (bias): {beta}, shape: {beta.shape}, dtype: {beta.dtype}")
    #print(f"mu (running_mean): {mu}, shape: {mu.shape}, dtype: {mu.dtype}")
    #print(f"sigma (running_var): {sigma}, shape: {sigma.shape}, dtype: {sigma.dtype}")
    # training=False forces use of running stats
    a= gamma / torch.sqrt(sigma + eps)
    c = beta - mu * a
    return a,c
