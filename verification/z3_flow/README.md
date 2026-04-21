# ACR-GNNVerification tool
Our goal is to translate an Aggregate Combine Graph Neural Network with the global Readout (ACR-GNN) to the code that we can pass trought Z3 solver

## Graph Neeural Network
In this code we are using the reference architecture of the paper of the Barcelò et. al.[1] with the implementation[2].

## Logic
For the Logic that we can use to verify chosen models is the modal $q\mathcal{L}$ Logic that was described in the article of [3],[4].

## Verification tool(s)
For these experiments we are using two verification tools: ESBMC[5] and Z3[6]. So in this case we have a comparison between the SMT solvers.

### Flow from the ESBMC
Here we have a flow of the programms that e are using to have:

Python program -[generate]-> C program -[parse]-> ESBMC solver -[obtain]-> Result: SAT or UNSAT.

### Flow for Z3 SMT solver
Formal verification of Aggregation-Convolution-Readout Graph Neural Networks using SMT (Z3)[6].

Here we have a flow of the programms that we are using to have:

Python programm -[generate]-> Z3 programm -[parse]-> Z3 solver -[obtain]-> Results SAT or non SAT.

>[!Note]
> This repository provides a Python tool (main.py) that automatically generates SMT-LIB encodings of small GNN-like layers and verifies postconditions using the Z3 SMT solver.
>The tool supports:
> - Arbitrary graph size (parameter Nbound)
> - Multiple layers
> - Multiple feature vectors
> - Several activation functions: ReLU, trReLU, and ReLU{p}
> - Configurable bit-vector width (default 8 bits)
> - Automatic SMT generation, logging, model extraction.


Right now we need to understands what structure of the code for the solver. For these case we took a simple ACR-GNN code. Lets split it for the peaces and code.

#### Phase0. Preprocessing.  

1. Create a class VerificationTask.
2. Variable `index_of_feature` set default to 0. We will use it after for indexation of variables.
<details>
  <summary>Sploiler</summary>
 With these index we can apply to postcondition to the feature of the last layer after applying the activation function. These index will be used to call the feature and be sure that all features have unique id.
</details>
 

#### Phase1. Creating functions.

**Create a function `__init__`.**

As input gets:
- `Nbound`- default value set to `2`.
- `filename` - default value set to `output.smt`.
- `bitvect` - default value set to `8`.
- `activation` -default value set to `ReLU`.
- `combination scheme` -default value set to `Cx+Ay+Rz`. Note: future work

Here we are working with the instancees.

- `Nbound` variable that takes into accound dimention of the unknown graph.
- `filename` variable stores the name of the output file that will be used for the Z3.
- `start_of_program` flag for writting the output file.
- `bitvector` value that will be used to convert numbers to the Z3 representation
- `features` stores all names of features
- `activation` store the name of the selected activation function
- `adj_matrix()` create anadjacency matrix of unknown graph 

**Create function `_addLineInMain`.**

Writes a given string to the specified output file. The resulting file is later consumed by the Z3 SMT solver.

**Create an Adjacency matrix; function `adj_matrix`.**

We create a square ($Nbound \times Nbound$) Adjacency matrix that represent the connection between the nodes, in term of the graph the 'connections' is the edges.
`e{i}_{j}`  edge between node i and node j;.
This variable is Bool type: True - edge exists, False otherwise.

In the `.smt` we can see the following code:

```smt
(declare-const eij Bool)
```

**Name feature; function `_get_new_featurename`.**
    
Here we are creating the unique name and storing the features that we are using.

This is useful to if we want to know in the end the final feature. (we do!)

**Decleare feature; function `add_input_feature` and `add_feature` .**

First of all , we need to understand how the name of the feature is forming. 
Each feature has:
    - the number i that depends on the variable `index_of_feature`, e.g. $x1, x2$.
    - dimendion j that depends on the `Nbound` variable, e.g. $x1[i]\text{ corresponds to } x1\_i$.
    - number of bits for the vector that depends on the variable `bitvect`.

```smt
(declare-const x{i}{j} (_ BitVec 8))
```

>[!Important] As can be clearly seen from the code, these functions produce the same output. The important difference is that we are comparing this code with the ESBMC-generated code, and therefore the function names must correspond.

**Preconditions `add_precondition`**

This method inserts a precondition into the encoding of the ACR-GNN verification problem.
A precondition is a logical constraint on existing feature variables (e.g., `x1[0] == 1, x2[3] == 0 || x2[3] == 1`).

>[!Important]
> The expression is processed by `convert_condition_to_smt`

**function `convert_condition_to_smt`**

Convert a high-level condition in Python into a single SMT-LIB assert.
Precedence: && is stronger than ||.

**function `parse_atomic`**

Convert a single atomic condition from the precondition string into an SMT-LIB bit-vector expression.

For each atomic expression, `parse_atomic`:

1. Parses the left-hand side variable (`x1[0]`, `x2[1]`, …).
2. Parses the comparison operator (`==`, `!=`, `<`, `<=`, `>`, `>=`).
3. Parses the right-hand side integer constant.
4. Produces the corresponding SMT-LIB bit-vector predicate, e.g.:

```smt
; from "x1[0] == 1"
(= x1_0 #x01)

; from "x1[0] <= 5"
(bvule x1_0 #x05)

; from "x2[1] >= 6"
(bvuge x2_1 #x06)
```

Also has a flag for the postconditions. We need to be sure that feature to which e apply postcondition is exists.

**function `parse_var`**

Convert a variable written in Python-style vector notation (as used in the precondition string) into the internal SMT variable name expected by Z3.

>[!IMPORTANT]
>- Input format: `name[index]`. Example: `x1[0]`, `x2[3]`, `x3[2]`
>- Output format: concatenation of base name and index, e.g.:
>   - `x1[0]` → `x1_0`
>   - `x2[3]` → `x2_3`
>   - `x3[2]` → `x3_2`

This matches how feature variables are declared and used in the SMT-LIB file.

**function `int_to_bv_hex`.**

Convert an integer value into an SMT-LIB hex bit-vector literal.

>[!IMPORTANT]
> Supports **any bit-width**, including non-multiples of 4 bits.
> Handles **negative values** using two’s complement encoding.
> Example for `bit_width = 8`:
>  - `1  → #x01`
>  - `5  → #x05`
>  - `-1 → #xff`

This function ensures that all numeric constants in the preconditions are correctly represented as bit-vectors for Z3.

**Layer of the ACR-GNN `add_layer`**
As input, this function takes 3 matrices and vector.
- $C$, $A$, $R$ - three matrices that corresponds to $C$ - combination, $A$ - aggregation and $R$ - the readout (global aggregation).
- $b$ - bias vector

> [!WARNING]  
> We use the scheme `C x + A y + R + b`. You must ensure that all
> matrices and vectors have compatible dimensions so that the matrix
> multiplications are well-defined. The same applies to the bias `b`.
>
> By design, each feature vector (e.g., `x1`, `x2`, …) has dimension  
> `Nbound × 1` (a column vector), corresponding to the variables  
> `x1[0] … x1[Nbound-1]` encoded as `x10 … x1(Nbound-1)`.
>
> Therefore, any matrix that multiplies a feature vector from the left
> must have shape `k × Nbound` (for some `k`). In particular, if you
> want a scalar result, you should use a `1 × Nbound` matrix.
> If these dimensions do not match, the generated SMT encoding will no
> longer correspond to a valid matrix–vector product.
To check the validy of the input we are using the finction `checking_input_matrices`

We have the scheme:
- store the input dimension that we get from the C matrix in variable `input_dimension`.
-store the output dimension in variable `input_dimension`.
- Look on the featurs that we are having right now.
- `previousFeatures = self.features[-input_dimension:]` take last Nbound number of features
- declare the local and global aggregation variables. Mark them into output file.
- block of the matrix multiplication
> [!Important] 
> Encodes, for each position $i = 0 \cdots Nbound-1$ and each output o:
> 
>  $$u_o(i) = sum_j C[o][j] * x_j(i)+ sum_j A[o][j] * y_j(i)+ sum_j R[o][j] * z_j(i)+ b[o][0]$$
> 
>  where:
> - previousFeatures[j]      = base name of x_j (e.g., "x1")
> - aggPreviousFeatures[j]   = base name of y_j
> - aggGPreviousFeatures[j]  = base name of z_j
> - outputFeatures[o]        = base name of u_o (e.g., "x5", "x6")

- apply activation function $\alpha(u_o(i))$ via calling function `apply_activation`

**function `apply_activation`.**  
Here we take an input feature, create the new feature specifically for the activation functiob via `declare_featuresAF` function and based on the selection of the supported activation functions apply them.

>[!Note]
> We support following activation functions: ReLU, ReLU{p} (e.g. ReLU6, ReLU2, etc.), trReLU.

**function `get_last_feature`.**  

As was mention in the name of the function return the last feature 


**Postconditions; function`add_postcondition`.**

The same flow as Preconditon block, but we also check if the feature is exists

**Check the model; function `check`**

Run Z3 on the generated SMT file, ask for intermediate values of all feature and activation variables after (check-sat).

Returns:
- status: 'sat', 'unsat', or 'unknown'
- values: dict { "x1_0": int, "x1_1": int, "a1_0": int, ... } if sat, empty dict otherwise.
    
So we create set of functions in the `main.py` to simulate the ACR-GNN. 
  


## Reference

[1] Pablo Barceló, Egor V. Kostylev, Mikaël Monet, Jorge Pérez, Juan L. Reutter, and Juan Pablo Silva.  
**The Logical Expressiveness of Graph Neural Networks**, 8th International Conference on Learning Representations (ICLR), 2020.  
Available at: [https://openreview.net/forum?id=r1lZ7AEKvB](https://openreview.net/forum?id=r1lZ7AEKvB)

[2] Pablo Barceló, Egor V. Kostylev, Mikaël Monet, Jorge Pérez, Juan L. Reutter, and Juan Pablo Silva.  
**GNN-logic**, GitHub repository, 2021.  
Available at: [https://github.com/juanpablos/GNN-logic](https://github.com/juanpablos/GNN-logic)

[3]

[4]

[5] Menezes, R., Aldughaim, M., Farias, B., Li, X., Manino, E., Shmarov, F., Song, K., Brauße, F., Gadelha, M. R., Tihanyi, N., Korovin, K., & Cordeiro, L. C. **ESBMC 7.4: Harnessing the Power of Intervals**, TACAS, LNCS 14572, pp. 376–380. Springer,2024.  
Available at: [https://doi.org/10.1007/978-3-031-57256-2_24](https://doi.org/10.1007/978-3-031-57256-2_24)
    

[6] De Moura, Leonardo, and Nikolaj Bjørner. **Z3: An efficient SMT solver.**,TACAS. Springer, 2008.
Available at: [https://link.springer.com/chapter/10.1007/978-3-540-78800-3_24](https://link.springer.com/chapter/10.1007/978-3-540-78800-3_24)

## License

This project is licensed under the [MIT License](LICENSE).
