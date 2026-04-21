Activation function: ReLU
Scheme: xC+b_C
Input node features:
[[0. 0. 1.]
 [0. 1. 0.]]
x0_0=0.0=(fp #b0 #b00000000 #b00000000000000000000000)
x0_1=0.0=(fp #b0 #b00000000 #b00000000000000000000000)
x0_2=1.0=(fp #b0 #b01111111 #b00000000000000000000000)
x1_0=0.0=(fp #b0 #b00000000 #b00000000000000000000000)
x1_1=1.0=(fp #b0 #b01111111 #b00000000000000000000000)
x1_2=0.0=(fp #b0 #b00000000 #b00000000000000000000000)
Adjacency matrix:
[[1. 1.]
 [1. 0.]]
Input data type: Float32
Local Aggregation:
[[0. 1. 1.]
 [0. 0. 1.]]
Global Aggregation:
[0. 1. 1.]
Layer computations:
Computations for 1 layers
Layer: 0
xV:
[[ 0.07434869  0.15482074  0.33135426]
 [ 0.16640157 -0.22236899  0.5174947 ]]
xV + b_V:
[[ 0.3942994  -0.01966205  0.57964647]
 [ 0.48635226 -0.39685178  0.7657869 ]]
yA:
[[-0.2650145   0.5746702  -0.62156105]
 [-0.11741691  0.34642333 -0.24787587]]
yA + b_A:
[[0.38158646 0.4558514  0.17225718]
 [0.52918404 0.22760454 0.54594237]]
zR:
[ 0.12198891 -0.5096289  -0.07460423]
zR + b_R:
[ 0.02339301 -0.91298914 -0.25354868]
(xV + b_V) + (yA + b_A) + (zR + b_R):
[[ 0.79927886 -0.4767998   0.49835497]
 [ 1.0389293  -1.0822364   1.0581806 ]]
ReLU:
[[0.79927886 0.         0.49835497]
 [1.0389293  0.         1.0581806 ]]
Batch Normalization:
[[ 1.6614547   0.20484535 -1.1430105 ]
 [ 2.820653    0.20484535  0.36785078]]
Computations for the layer 0 are finished.
Linear Prediction
Linear prediction output before adding bias:
[[-2.9007876  3.0048144]
 [-2.7890828  2.7684474]]
Linear prediction output:
[[-2.5736296  2.5554051]
 [-2.4619248  2.3190382]]
Binary classification:
node 0 was classified as 1
node 1 was classified as 1
Computations are finished
