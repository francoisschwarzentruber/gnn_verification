# General description of the flow.
In this project, we are focusing on the Aggregate-combine Graph Neural Network with the global Readout (ACR-GNN).

[art: we can work on AC-GNN also, just we need to have a flag in the code.][task: ask ]

ACR-GNN can be applied at different levels of granularity:
- Node-level tasks, where the objective is to assign a label to each node (e.g., node classification),
- Edge-level tasks, where relationships between pairs of nodes are predicted (e.g., link prediction),
- Graph-level tasks, where an entire graph is assigned a label (e.g., graph classification).
In our case, we focus on **binary node classification**, meaning that the model operates at the node level and learns to assign labels to individual nodes within each graph.

## Data
In this article, we are using several datasets. In particular:
- Synthetic data Erdos–Renyi model
- PPI (need to be converted to the Binary node classification) https://pytorch-geometric.readthedocs.io/en/2.5.0/generated/torch_geometric.datasets.PPI.html
- Citeseer Graph Dataset (* need to look closer) https://www.dgl.ai/dgl_docs/generated/dgl.data.CiteseerGraphDataset.html
- QM9 (* need to look closer) https://pytorch-geometric.readthedocs.io/en/2.5.0/generated/torch_geometric.datasets.QM9.html

> [!Important]
> We are interested in datasets containing multiple graphs.

## Model
For the verification flow, we are using the Aggregate-Combine Graph Neural (with global Readout).

[todo: clarify this step]

For the code input, we need the `.pth` model and the activation function.

> [!NOTE] In our implementation (what we modified from the article of Barcelo et. al.) of the model, we save the model and the activation function that was applied. Otherwise, the activation function should be specified. Important information is that the SMT-solver could work only with the Piecewise linear activation functions (e.x, ReLU, ReLU6, trReLU, and LeakyReLU)

> [!WARNING]
> It is crutual to pass the selected activation function with wich model was trained. 

> [!IMPORTANT]
> There are two ways to work with the model:
> 1. Access to architecture.
> Here we neeed ot use the model in evoluation mode.
> 2. Access to the `.pth` file of the model.
> We do not have access to the architecture and are working with the state_dict[1].

For the first steps, we focus on the implementation using the state_dict.


## SMT Solver 

In this article, we use the Z3 SMT solver for the verification of the model.
In Z3 we have two ways to integrate it into the verification flow:
1. Use the `.py` to generate the .smt file. Illustration of the method. In this case, we can pass the `.smt` file generated to CVC5[3]. 
2. Use the Pythom library directly.

As a __baseline__ we will us the flow from 


# Bibliography
[1] https://docs.pytorch.org/tutorials/recipes/recipes/what_is_state_dict.html

[2] Z3
- [Article](https://dl.acm.org/doi/10.5555/1792734.1792766)
- [GitHub](https://github.com/z3prover/z3)

[3] CVC5
- [Article](https://dl.acm.org/doi/10.1007/978-3-030-99524-9_24)
- [GitHub](https://github.com/cvc5/cvc5)