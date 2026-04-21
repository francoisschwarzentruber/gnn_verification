# Data
**Task**: Binary Node classification across multiple graphs.

## Create graphs

To create the dataset we usen the __Erdos-Reniy__ model with several specifications:
- Number of nodes from 2 to 6.
- Number of edges is equal to the numebr of nodes.
- Number of features per node is 1. Possible values are: 0,1,2

## Color nodes
For the coloring we used thee following expression:

`A node is SAT if it has 1 or 2 neighbors with a feature green`.

Here SAT or UNSAt is the target for the Binary Node classification and these are endoded as 1 or 1 respectfully.

## Data in .txt file

We could parse the data directly from the the same files as we used for the training.
Only, we need to describe the format in which the information is stored.
The easest way to describe the data, describe it on the example.

<a id="fig1"></a>
<p align="center">
  <img src="../description/p0_graph_2_nodes.png" alt="example1" width="300">
</p>
<p align="center"><b>Figure 1.</b> Simple Graph for the analysis. Example 1.</p>

In the `.txt` file we could find the description of this graph:
```txt
2 1
1 2 0 1 1
1 0 1 1 0
```
This is corresponds to the description
```
```txt
number_of_nodes graph_label
number_of_features feature_value node_label number_of_neighbours list_of_neightbours
number_of_features feature_value node_label number_of_neighbours list_of_neightbours
```
So for this graph:
- number_of_nodes =2
- graph_label =1 
> [!Note]
> For our model we do not care about the graph label. We focus on the node classification.
- number_of_features
- feature_value. For node_0 is 2, for node_1 is 0.
- node_label. For node_0 is 0 (UNSAT), for node_1 is 1(SAT). 
> [!Note]
> We don't use this during inference. Only for the training.
- number_of_neighbours. Specisications of the number, with this data we form the dimension of the Adjastency matrix. For node_0 is 1, for node_1 is 1. So the dimension of the AM is $2 \times 2$.
- list_of_neightbours. Here is the list of the neighbours. For node_0 is 1, for node_1 is 0.

## Test cases for the verification Tasks.
### Example 1

For the example 1 we consider the graph [Figure 1](#fig1).