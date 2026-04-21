Activation function: ReLU
Scheme: xC+b_C
Input node features:
[[0. 0. 1.]
 [1. 0. 0.]]
x0_0=0.0=(fp #b0 #b00000000 #b00000000000000000000000)
x0_1=0.0=(fp #b0 #b00000000 #b00000000000000000000000)
x0_2=1.0=(fp #b0 #b01111111 #b00000000000000000000000)
x1_0=1.0=(fp #b0 #b01111111 #b00000000000000000000000)
x1_1=0.0=(fp #b0 #b00000000 #b00000000000000000000000)
x1_2=0.0=(fp #b0 #b00000000 #b00000000000000000000000)
Adjacency matrix:
[[0. 1.]
 [1. 0.]]
Input data type: Float32
Local Aggregation:
[[1. 0. 0.]
 [0. 0. 1.]]
Global Aggregation:
[1. 0. 1.]
Layer computations:
Computations for 1 layers
Layer: 0
xV:
[[ 0.07434869  0.15482074  0.33135426]
 [-0.02296904 -0.42489457 -0.51900023]]
xV + b_V:
[[ 0.3942994  -0.01966205  0.57964647]
 [ 0.29698166 -0.5993774  -0.27070805]]
yA:
[[-0.9673141   0.0213871   0.39980644]
 [-0.11741691  0.34642333 -0.24787587]]
yA + b_A:
[[-0.32071316 -0.09743169  1.1936247 ]
 [ 0.52918404  0.22760454  0.54594237]]
zR:
[ 0.13521694 -0.6817557   0.08368567]
zR + b_R:
[ 0.03662103 -1.0851159  -0.09525879]
(xV + b_V) + (yA + b_A) + (zR + b_R):
[[ 0.11020725 -1.2022097   1.6780124 ]
 [ 0.8627867  -1.4568888   0.17997551]]
ReLU:
[[0.11020725 0.         1.6780124 ]
 [0.8627867  0.         0.17997551]]
Batch Normalization:
[[-1.671611    0.20484535  2.0406573 ]
 [ 1.9686446   0.20484535 -2.0022552 ]]
Computations for the layer 0 are finished.
Linear Prediction
Linear prediction output before adding bias:
[[ 4.0808764 -3.9200828]
 [-4.0931582  4.2146287]]
Linear prediction output:
[[ 4.4080343 -4.369492 ]
 [-3.7660003  3.7652194]]
Binary classification:
node 0 was classified as 0
node 1 was classified as 1
Computations are finished
