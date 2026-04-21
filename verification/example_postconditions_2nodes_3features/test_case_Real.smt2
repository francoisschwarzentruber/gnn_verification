;; SMT encoding for ACR-GNN verification with Real precision
;; Activation function: ReLU
(set-option :produce-models true)
(set-option :produce-unsat-cores true)
(define-fun fp0 () Real 0.0)
(define-fun fp1 () Real 1.0)
;; adjacency matrix of unknown graph
(declare-const e0_0 Bool)
(declare-const e0_1 Bool)
(declare-const e1_0 Bool)
(declare-const e1_1 Bool)

;; declare nodes with dimension of the number of features.
;; declare node x0
(declare-const x0_0 Real)
(declare-const x0_1 Real)
(declare-const x0_2 Real)

;; precondition x0[0] == 0 || x0[0] == 1
(assert (or (= x0_0 0) (= x0_0 1)))

;; precondition x0[1] == 0 || x0[1] == 1
(assert (or (= x0_1 0) (= x0_1 1)))

;; precondition x0[2] == 0 || x0[2] == 1
(assert (or (= x0_2 0) (= x0_2 1)))

;; Node 0 features are binary (0 or 1)
;; one-hot precondition for x0 with 3 features
(assert (= (+ x0_0 x0_1 x0_2) 1.0))

;; declare node x1
(declare-const x1_0 Real)
(declare-const x1_1 Real)
(declare-const x1_2 Real)

;; precondition x1[0] == 0 || x1[0] == 1
(assert (or (= x1_0 0) (= x1_0 1)))

;; precondition x1[1] == 0 || x1[1] == 1
(assert (or (= x1_1 0) (= x1_1 1)))

;; precondition x1[2] == 0 || x1[2] == 1
(assert (or (= x1_2 0) (= x1_2 1)))

;; Node 1 features are binary (0 or 1)
;; one-hot precondition for x1 with 3 features
(assert (= (+ x1_0 x1_1 x1_2) 1.0))

;; decline features for the local aggregation.
;; declare node x2
(declare-const x2_0 Real)
(declare-const x2_1 Real)
(declare-const x2_2 Real)

;; declare node x3
(declare-const x3_0 Real)
(declare-const x3_1 Real)
(declare-const x3_2 Real)

;; decline features for the global aggregation.
;; declare node x4
(declare-const x4_0 Real)
(declare-const x4_1 Real)
(declare-const x4_2 Real)

;; declare node x5
(declare-const x5_0 Real)
(declare-const x5_1 Real)
(declare-const x5_2 Real)

;; Local aggregation (across neighbours)

;; agg_local(x2,x0)
(assert
  (= x2_0
     (+ (ite e0_0 x0_0 0.0) (ite e0_1 x1_0 0.0))
  )
)

(assert
  (= x2_1
     (+ (ite e0_0 x0_1 0.0) (ite e0_1 x1_1 0.0))
  )
)

(assert
  (= x2_2
     (+ (ite e0_0 x0_2 0.0) (ite e0_1 x1_2 0.0))
  )
)

;; agg_local(x3,x1)
(assert
  (= x3_0
     (+ (ite e1_0 x0_0 0.0) (ite e1_1 x1_0 0.0))
  )
)

(assert
  (= x3_1
     (+ (ite e1_0 x0_1 0.0) (ite e1_1 x1_1 0.0))
  )
)

(assert
  (= x3_2
     (+ (ite e1_0 x0_2 0.0) (ite e1_1 x1_2 0.0))
  )
)

;; end local aggregation

;; Global aggregation
;; Compute global agg(x4)
(assert (= x4_0
          (+ x0_0 x1_0)))
(assert (= x4_1
          (+ x0_1 x1_1)))
(assert (= x4_2
          (+ x0_2 x1_2)))
;; end global agg(x4)

;; Compute global agg(x5)
(assert (= x5_0
          (+ x0_0 x1_0)))
(assert (= x5_1
          (+ x0_1 x1_1)))
(assert (= x5_2
          (+ x0_2 x1_2)))
;; end global agg(x5)

;; matrix multiplication
;;np.dot(FM,V) xV
;; declare node x6
(declare-const x6_0 Real)
(declare-const x6_1 Real)
(declare-const x6_2 Real)

;; declare node x7
(declare-const x7_0 Real)
(declare-const x7_1 Real)
(declare-const x7_2 Real)

(assert
  (= x6_0
     (+ (+ (* x0_0 -0.0229690429) (* x0_1 0.166401565)) (* x0_2 0.0743486881))
  )
)
(assert
  (= x6_1
     (+ (+ (* x0_0 -0.424894571) (* x0_1 -0.222368985)) (* x0_2 0.15482074))
  )
)
(assert
  (= x6_2
     (+ (+ (* x0_0 -0.519000232) (* x0_1 0.517494678)) (* x0_2 0.33135426))
  )
)

(assert
  (= x7_0
     (+ (+ (* x1_0 -0.0229690429) (* x1_1 0.166401565)) (* x1_2 0.0743486881))
  )
)
(assert
  (= x7_1
     (+ (+ (* x1_0 -0.424894571) (* x1_1 -0.222368985)) (* x1_2 0.15482074))
  )
)
(assert
  (= x7_2
     (+ (+ (* x1_0 -0.519000232) (* x1_1 0.517494678)) (* x1_2 0.33135426))
  )
)

;;np.dot(V,FM) + b_V
;; declare node x8
(declare-const x8_0 Real)
(declare-const x8_1 Real)
(declare-const x8_2 Real)

;; declare node x9
(declare-const x9_0 Real)
(declare-const x9_1 Real)
(declare-const x9_2 Real)

(assert
   (= x8_0
      (+ x6_0 0.3199507)
   )
)
(assert
   (= x8_1
      (+ x6_1 -0.174482793)
   )
)
(assert
   (= x8_2
      (+ x6_2 0.248292178)
   )
)

(assert
   (= x9_0
      (+ x7_0 0.3199507)
   )
)
(assert
   (= x9_1
      (+ x7_1 -0.174482793)
   )
)
(assert
   (= x9_2
      (+ x7_2 0.248292178)
   )
)

;;np.dot(agg_local,A) yA
;; declare node x10
(declare-const x10_0 Real)
(declare-const x10_1 Real)
(declare-const x10_2 Real)

;; declare node x11
(declare-const x11_0 Real)
(declare-const x11_1 Real)
(declare-const x11_2 Real)

(assert
  (= x10_0
     (+ (+ (* x2_0 -0.967314124) (* x2_1 -0.147597581)) (* x2_2 -0.117416911))
  )
)
(assert
  (= x10_1
     (+ (+ (* x2_0 0.0213871002) (* x2_1 0.228246868)) (* x2_2 0.346423328))
  )
)
(assert
  (= x10_2
     (+ (+ (* x2_0 0.39980644) (* x2_1 -0.373685151)) (* x2_2 -0.247875869))
  )
)

(assert
  (= x11_0
     (+ (+ (* x3_0 -0.967314124) (* x3_1 -0.147597581)) (* x3_2 -0.117416911))
  )
)
(assert
  (= x11_1
     (+ (+ (* x3_0 0.0213871002) (* x3_1 0.228246868)) (* x3_2 0.346423328))
  )
)
(assert
  (= x11_2
     (+ (+ (* x3_0 0.39980644) (* x3_1 -0.373685151)) (* x3_2 -0.247875869))
  )
)

;;np.dot(agg_local,A) + b_A
;; declare node x12
(declare-const x12_0 Real)
(declare-const x12_1 Real)
(declare-const x12_2 Real)

;; declare node x13
(declare-const x13_0 Real)
(declare-const x13_1 Real)
(declare-const x13_2 Real)

(assert
   (= x12_0
      (+ x10_0 0.646600962)
   )
)
(assert
   (= x12_1
      (+ x10_1 -0.11881879)
   )
)
(assert
   (= x12_2
      (+ x10_2 0.793818235)
   )
)

(assert
   (= x13_0
      (+ x11_0 0.646600962)
   )
)
(assert
   (= x13_1
      (+ x11_1 -0.11881879)
   )
)
(assert
   (= x13_2
      (+ x11_2 0.793818235)
   )
)

;;np.dot(agg_global,R) zR
;; declare node x14
(declare-const x14_0 Real)
(declare-const x14_1 Real)
(declare-const x14_2 Real)

;; declare node x15
(declare-const x15_0 Real)
(declare-const x15_1 Real)
(declare-const x15_2 Real)

(assert
  (= x14_0
     (+ (+ (* x4_0 0.0741181746) (* x4_1 0.0608901493)) (* x4_2 0.0610987656))
  )
)
(assert
  (= x14_1
     (+ (+ (* x4_0 -0.535590708) (* x4_1 -0.363463879)) (* x4_2 -0.146165013))
  )
)
(assert
  (= x14_2
     (+ (+ (* x4_0 0.136728138) (* x4_1 -0.0215617679)) (* x4_2 -0.053042464))
  )
)

(assert
  (= x15_0
     (+ (+ (* x5_0 0.0741181746) (* x5_1 0.0608901493)) (* x5_2 0.0610987656))
  )
)
(assert
  (= x15_1
     (+ (+ (* x5_0 -0.535590708) (* x5_1 -0.363463879)) (* x5_2 -0.146165013))
  )
)
(assert
  (= x15_2
     (+ (+ (* x5_0 0.136728138) (* x5_1 -0.0215617679)) (* x5_2 -0.053042464))
  )
)

;;np.dot(agg_global,R) + b_R
;; declare node x16
(declare-const x16_0 Real)
(declare-const x16_1 Real)
(declare-const x16_2 Real)

;; declare node x17
(declare-const x17_0 Real)
(declare-const x17_1 Real)
(declare-const x17_2 Real)

(assert
   (= x16_0
      (+ x14_0 -0.0985959098)
   )
)
(assert
   (= x16_1
      (+ x14_1 -0.403360248)
   )
)
(assert
   (= x16_2
      (+ x14_2 -0.178944468)
   )
)

(assert
   (= x17_0
      (+ x15_0 -0.0985959098)
   )
)
(assert
   (= x17_1
      (+ x15_1 -0.403360248)
   )
)
(assert
   (= x17_2
      (+ x15_2 -0.178944468)
   )
)

;;(np.dot(V,FM) + b_V)+(np.dot(A,agg_local) + b_A)+(np.dot(R,agg_global) + b_R)
;; declare node x18
(declare-const x18_0 Real)
(declare-const x18_1 Real)
(declare-const x18_2 Real)

;; declare node x19
(declare-const x19_0 Real)
(declare-const x19_1 Real)
(declare-const x19_2 Real)

(assert
   (= x18_0
      (+ (+ x8_0 x12_0) x16_0)
   )
)
(assert
   (= x18_1
      (+ (+ x8_1 x12_1) x16_1)
   )
)
(assert
   (= x18_2
      (+ (+ x8_2 x12_2) x16_2)
   )
)

(assert
   (= x19_0
      (+ (+ x9_0 x13_0) x17_0)
   )
)
(assert
   (= x19_1
      (+ (+ x9_1 x13_1) x17_1)
   )
)
(assert
   (= x19_2
      (+ (+ x9_2 x13_2) x17_2)
   )
)

;; applying activation function
;; activation function: ReLU
(define-fun ReLU ((x Real)) Real
  (ite (> x fp0) x fp0)
)
;; declare node x20
(declare-const x20_0 Real)
(declare-const x20_1 Real)
(declare-const x20_2 Real)

;; declare node x21
(declare-const x21_0 Real)
(declare-const x21_1 Real)
(declare-const x21_2 Real)

(assert
   (= x20_0
      (ReLU x18_0)
   )
)
(assert
   (= x20_1
      (ReLU x18_1)
   )
)
(assert
   (= x20_2
      (ReLU x18_2)
   )
)

(assert
   (= x21_0
      (ReLU x19_0)
   )
)
(assert
   (= x21_1
      (ReLU x19_1)
   )
)
(assert
   (= x21_2
      (ReLU x19_2)
   )
)

;; applying Batch Normalization. Linear form: bn_a * act + bn_c
;; bn_a and bn_c are computed from the parameters of the batch normalization layer as follows:
;; bn_a = gamma / sqrt(running_var + eps)
;; bn_c = beta - (gamma * running_mean) / sqrt(running_var + eps)
;; act[i][j]*a[j] + c[j]
;; declare node x22
(declare-const x22_0 Real)
(declare-const x22_1 Real)
(declare-const x22_2 Real)

;; declare node x23
(declare-const x23_0 Real)
(declare-const x23_1 Real)
(declare-const x23_2 Real)

(assert
   (= x22_0
      (+ (* x20_0 4.83703804) -2.2046876)
   )
)
(assert
   (= x22_1
      (+ (* x20_1 316.227783) 0.204845354)
   )
)
(assert
   (= x22_2
      (+ (* x20_2 2.698807) -2.48797441)
   )
)

(assert
   (= x23_0
      (+ (* x21_0 4.83703804) -2.2046876)
   )
)
(assert
   (= x23_1
      (+ (* x21_1 316.227783) 0.204845354)
   )
)
(assert
   (= x23_2
      (+ (* x21_2 2.698807) -2.48797441)
   )
)

;; end layer

;; Linear Prediction np.dot(BN, W_LP) + b_LP
;; declare node x24
(declare-const x24_0 Real)
(declare-const x24_1 Real)

;; declare node x25
(declare-const x25_0 Real)
(declare-const x25_1 Real)

;; np.dot(BN, W_LP)
(assert
  (= x24_0
     (+ (+ (* x22_0 -1.1680429) (* x22_1 0.725942314)) (* x22_2 0.970107555))
  )
)
(assert
  (= x24_1
     (+ (+ (* x22_0 1.11273301) (* x22_1 0.00688288594)) (* x22_2 -1.01018238))
  )
)

(assert
  (= x25_0
     (+ (+ (* x23_0 -1.1680429) (* x23_1 0.725942314)) (* x23_2 0.970107555))
  )
)
(assert
  (= x25_1
     (+ (+ (* x23_0 1.11273301) (* x23_1 0.00688288594)) (* x23_2 -1.01018238))
  )
)

;;np.dot(BN, W_LP) + b_LP
;; declare node x26
(declare-const x26_0 Real)
(declare-const x26_1 Real)

;; declare node x27
(declare-const x27_0 Real)
(declare-const x27_1 Real)

(assert
   (= x26_0
      (+ x24_0 0.327157974)
   )
)
(assert
   (= x26_1
      (+ x24_1 -0.449409246)
   )
)

(assert
   (= x27_0
      (+ x25_0 0.327157974)
   )
)
(assert
   (= x27_1
      (+ x25_1 -0.449409246)
   )
)

;; end linear prediction layer

;;Binary classification
(define-fun argmax ((x Real) (y Real)) Int
  (ite (> x y) 0 1)
)
;; declare node x28
(declare-const x28_0 Int)

;; declare node x29
(declare-const x29_0 Int)

(assert
   (= x28_0
      (argmax x26_0 x26_1)
   )
)
(assert
   (= x29_0
      (argmax x27_0 x27_1)
   )
)
;; postcondition x28[0] == 0
(assert (not (= x28_0 0)))

;; postcondition x29[0] == 1
(assert (not (= x29_0 1)))

(check-sat)
;;(get-model)
(get-model)
;;(Feature Matrix for nodes)
(get-value (x0_0))
(get-value (x0_1))
(get-value (x0_2))
(get-value (x1_0))
(get-value (x1_1))
(get-value (x1_2))
;;(Adjacency  Matrix for nodes)
(get-value (e0_0))
(get-value (e0_1))
(get-value (e1_0))
(get-value (e1_1))
;; Binary classification result (0 or 1) for each node
(get-value (x28_0 x29_0))
