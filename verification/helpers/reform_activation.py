def reform_activation(state):
    print(f"Original activation function in the model: {state['activation']}")
    activation = state['activation']
    if activation=='relu':
        activation_function='ReLU'
    elif activation=='relu6':
        activation_function='ReLU6'
    elif activation=='trrelu':
        activation_function='trReLU'
    elif activation=='leakyrelu':
        activation_function='LeakyReLU'
    else:
        raise ValueError("Activation function not recognized.")
    return activation_function
