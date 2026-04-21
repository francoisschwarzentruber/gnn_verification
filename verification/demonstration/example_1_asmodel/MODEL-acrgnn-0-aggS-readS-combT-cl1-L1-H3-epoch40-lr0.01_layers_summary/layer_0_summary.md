# 1-Layer of the ACR-GNN with Activation: relu.
## Parameters for layer 1.
### Matrices and Biases. Description and checking.
- Number of Matrices with Biases: 6.
- Found expected number of parameters for layer 1.
- Found weight for `V` in layer 1, shape: torch.Size([3, 3]), dtype: torch.float32
- Found bias for `V` in layer 1, shape: torch.Size([3]), dtype: torch.float32
- Found weight for `A` in layer 1, shape: torch.Size([3, 3]), dtype: torch.float32
- Found bias for `A` in layer 1, shape: torch.Size([3]), dtype: torch.float32
- Found weight for `R` in layer 1, shape: torch.Size([3, 3]), dtype: torch.float32
- Found bias for `R` in layer 1, shape: torch.Size([3]), dtype: torch.float32
> [!NOTE]
> Weights for layer 1 have consistent shape: torch.Size([3, 3])
> [!NOTE]
> Biases for layer 1 have consistent shape: torch.Size([3])

> [!NOTE]
> Output dimensions of weights and biases match for layer 1.
### Batch Normalization Description and checking:
- Batch Normalization parameters: 5
> [!NOTE]
> Output is 5, but we care during the inference about weight, bias, running_mean, running_var
- Found Batch Normalization parameter `weight` for layer 1.
- Found Batch Normalization parameter `bias` for layer 1.
- Found Batch Normalization parameter `running_mean` for layer 1.
- Found Batch Normalization parameter `running_var` for layer 1.
> [!NOTE]
> Batch normalization parameters for layer 1 have consistent shape: torch.Size([3])
