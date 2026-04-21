# Z3 flow
This file aim to illustrate the path of the trained model throug the verification process: from unpacking the learned parameters to the Z3 instances.

For this case we used the trained models with the PyTorch Geometric Library.

## Step 1: Create the Adjacency Matrix 
We define the Adjacency Matrix of the input graph.

The Adjacency Matrix has the dimension $n \times n$ where $n$ is the number of the nodes. Values of the matrix is `1` is there is the edge between nodes, `0` otherwise. In other words, values are  Boolean (dtype=Bool).

> [!Note]
> Here we describe the notation that we are using for the Adjacency Matrix: `ei_j`, where `e` stands for the edge, so mathematicaly we can represent this as a $E(u,v)$ edge between node $u$ and $v$, so the first index refer to the node $u$ and the second one to the node $v$.

For our example we define the Adjacency Matrix in the hardcode mode.

This is mean that we have to code this:

```python
adj_matrix=np.array([[0,1],[1,0]], dtype=np.float32) 

[0,1]
[1,0]
```

To define the edges we are using the following: `(declare-const e0_0 Bool)`.

To assing the values that we want, we need to add: `(assert (= e0_0 false))`.

This line means that there is no edge between node 0 and node 0.

We skip this, when we are codding the general case.

## Step 2: Create the Feature Matrix 
Each node has the feature. This feture represents as a vector with the dimension `in_feature_dimension` (maximum number of feature for this graph).

For example, in the graph with 10 nodes and 5 features, the feature vector will have dimension $\mathbb{R}^{1 \times 5}$. 
Possible values of feature per node: 0 or 1 or 2 or 3 or 4.

This feature is one-hot encoded as a vector where value `1` we put in the position that corespond the number of the feature. 

For example, if the node 0 has the feature 2(out of 3 possibilities) this is represented as: [0,0,1].

To include this into the SMT we coded each feature uses the: (declare-const x1_0 Float32).

We used the dtype Float32 as in the model. To code Float32 we used SMTLIB2 standard IEEE Floating Point Numbers [Flot32 Z3](https://microsoft.github.io/z3guide/docs/theories/IEEE%20Floats/).

> [!Note]
> Here we describe the notation for this step. Each feature vector has the two indeses that are separated by `_`. As we described before, we use the notation of the arrays, where the feature vector that corresponds to the node stores the one-hot encoding defined. For example for the first feature we have the feature vector `x1`. 
> We need to declare values separately, so the x1[0] correspond to x1_0. Also, with this choice of separation we avoid the collision between x1[28] and x12[8].

[Task to think] How we could use Arrays in Z3? Could we? https://microsoft.github.io/z3guide/docs/theories/Arrays

In the example we have two nodes and maximum number of the feature is three, so the Feature Matrix has dimension $\mathbb{R}^{2 \times 3}$.

> [!Important]
> In the code we aredealing with feature vector for each node: `x[0]=[0,0,1]`, where feature #2 was one-hot encoded for the node 0. 
>
> In SMT, we have feature vector where information about this feature stores for all nodes. Preciesly,
> ```smt
> ;; declare feature x1 <-- feature 1
> (declare-const x1_0 (_ BitVec 32)) <-- value of the feature 1 for node 0
> (declare-const x1_1 (_ BitVec 32)) <-- value of the feature 1 for node 1
> ```
> To calculate $x[0]C$ we need `x0_0`,`x1_0`,`x2_0` -- this is correspond to `x[0]=[0,0,1]` and we need to take column of $C$ with index `0`. 

Now we need to assign the values to the features. These values we call preconditions.
By desing the value could be 0 or 1.:
- In General case value could be or 0 or 1: `(assert (or (= x0_0 ((_ to_fp 8 24) RNE 0.0)) (= x0_0 ((_ to_fp 8 24) RNE 1.0))))`
this is equivalent to `precondition x0[0] == 0 || x0[0] == 1`.
- For the example we assing the values hardcoded, only one option exists. 

```smt
;; precondition x0[0] == 0 
(assert (= x0_0 0))
```

## Step 3: Computations

Here we are working with the architecture of the ACR-GNN and consiquences of the decisons.

In the architecture convolution layers were defined with the `nn.Linear(input, output, bias=True)`, so each weight matrix has the own bias vector. We are working with the `state_dict` of the model, so we unpacked the matrices, biases and we need to parse them to the SMT.

Model parameters of the combination: $(xV+b_V)+(yA+b_A)+(zR+b_R)$
where:
- x is the initias Feature Matrix. 
- y is the local aggregation (aggregation from the neighbours)
- z is global aggregartion (aggregation across the graph)


>[!Note] We added brackets here because Floating point operations are defined modulo rounding modes. Many algebraic properties of bit-vectors, integers and reals don't carry over to floating points. For example, addition is not associative.

But before doing the matrix multiplication we need to form the local (y) and gloabal (z)
aggregation vectors.
 
### Local Aggregation

First of all we need to declare the features for the local aggregation. 

So if there is the edge between nodes then add the neighbour's feature.
```
(assert
  (= f3_0
     (fp.add RNE
        (ite e0_0 f1_0 ((_ to_fp 8 24) RNE 0.0))
        (ite e0_1 f1_1 ((_ to_fp 8 24) RNE 0.0))
     )
  )
)
```
### Global Aggregation

Here we need to compute the aggregation across all graph.

### Matrix multiplication
After forming the vectors of the local and global aggregation vectors