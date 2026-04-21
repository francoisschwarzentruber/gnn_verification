Activation function: ReLU
Scheme: xC+b_C
Input node features:
[[0. 1. 0.]
 [0. 1. 0.]]
x0_0=0.0=(fp #b0 #b00000000 #b00000000000000000000000)
x0_1=1.0=(fp #b0 #b01111111 #b00000000000000000000000)
x0_2=0.0=(fp #b0 #b00000000 #b00000000000000000000000)
x1_0=0.0=(fp #b0 #b00000000 #b00000000000000000000000)
x1_1=1.0=(fp #b0 #b01111111 #b00000000000000000000000)
x1_2=0.0=(fp #b0 #b00000000 #b00000000000000000000000)
Adjacency matrix:
[[0. 1.]
 [1. 0.]]
Input data type: Float32
Local Aggregation:
[[0. 1. 0.]
 [0. 1. 0.]]
Global Aggregation:
[0. 2. 0.]
Layer computations:
Computations for 1 layers
Layer: 0
xV:
[[ 0.16640157 -0.22236899  0.5174947 ]
 [ 0.16640157 -0.22236899  0.5174947 ]]
xV + b_V:
[[ 0.48635226 -0.39685178  0.7657869 ]
 [ 0.48635226 -0.39685178  0.7657869 ]]
yA:
[[-0.14759758  0.22824687 -0.37368515]
 [-0.14759758  0.22824687 -0.37368515]]
yA + b_A:
[[0.49900338 0.10942808 0.42013308]
 [0.49900338 0.10942808 0.42013308]]
zR:
[ 0.1217803  -0.72692776 -0.04312354]
zR + b_R:
[ 0.02318439 -1.130288   -0.22206801]
(xV + b_V) + (yA + b_A) + (zR + b_R):
[[ 1.00854   -1.4177117  0.963852 ]
 [ 1.00854   -1.4177117  0.963852 ]]
ReLU:
[[1.00854  0.       0.963852]
 [1.00854  0.       0.963852]]
Batch Normalization:
[[2.6736588  0.20484535 0.113276  ]
 [2.6736588  0.20484535 0.113276  ]]
Computations for the layer 0 are finished.
Linear Prediction
Linear prediction output before adding bias:
[[-2.8643522  2.8620489]
 [-2.8643522  2.8620489]]
Linear prediction output:
[[-2.5371943  2.4126396]
 [-2.5371943  2.4126396]]
Binary classification:
node 0 was classified as 1
node 1 was classified as 1
Computations are finished
