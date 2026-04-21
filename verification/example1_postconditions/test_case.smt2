;; SMT encoding for ACR-GNN verification with Float32 precision
;; Activation function: ReLU
(set-option :produce-models true)
(set-option :produce-unsat-cores true)
(define-fun fp0 () Float32 (fp #b0 #b00000000 #b00000000000000000000000))
(define-fun fp1 () Float32 (fp #b0 #b01111111 #b00000000000000000000000))
;; adjacency matrix of unknown graph
(declare-const e0_0 Bool)
(declare-const e0_1 Bool)
(declare-const e1_0 Bool)
(declare-const e1_1 Bool)

;; hard code the example one.
(assert (= e0_0 false))
(assert (= e0_1 true))
(assert (= e1_0 true))
(assert (= e1_1 false))

;; declare nodes with dimension of the number of features.
;; declare node x0
(declare-const x0_0 Float32)
(declare-const x0_1 Float32)
(declare-const x0_2 Float32)

;; precondition x0[0] == 0.0
(assert (= x0_0 (fp #b0 #b00000000 #b00000000000000000000000)))

;; precondition x0[1] == 0.0
(assert (= x0_1 (fp #b0 #b00000000 #b00000000000000000000000)))

;; precondition x0[2] == 1.0
(assert (= x0_2 (fp #b0 #b01111111 #b00000000000000000000000)))

;; declare node x1
(declare-const x1_0 Float32)
(declare-const x1_1 Float32)
(declare-const x1_2 Float32)

;; precondition x1[0] == 1.0
(assert (= x1_0 (fp #b0 #b01111111 #b00000000000000000000000)))

;; precondition x1[1] == 0.0
(assert (= x1_1 (fp #b0 #b00000000 #b00000000000000000000000)))

;; precondition x1[2] == 0.0
(assert (= x1_2 (fp #b0 #b00000000 #b00000000000000000000000)))

;; decline features for the local aggregation.
;; declare node x2
(declare-const x2_0 Float32)
(declare-const x2_1 Float32)
(declare-const x2_2 Float32)

;; declare node x3
(declare-const x3_0 Float32)
(declare-const x3_1 Float32)
(declare-const x3_2 Float32)

;; decline features for the global aggregation.
;; declare node x4
(declare-const x4_0 Float32)
(declare-const x4_1 Float32)
(declare-const x4_2 Float32)

;; declare node x5
(declare-const x5_0 Float32)
(declare-const x5_1 Float32)
(declare-const x5_2 Float32)

;; Local aggregation (across neighbours)

;; agg_local(x2,x0)
(assert
  (= x2_0
     (fp.add RNE (ite e0_0 x0_0 (fp #b0 #b00000000 #b00000000000000000000000)) (ite e0_1 x1_0 (fp #b0 #b00000000 #b00000000000000000000000)))
  )
)

(assert
  (= x2_1
     (fp.add RNE (ite e0_0 x0_1 (fp #b0 #b00000000 #b00000000000000000000000)) (ite e0_1 x1_1 (fp #b0 #b00000000 #b00000000000000000000000)))
  )
)

(assert
  (= x2_2
     (fp.add RNE (ite e0_0 x0_2 (fp #b0 #b00000000 #b00000000000000000000000)) (ite e0_1 x1_2 (fp #b0 #b00000000 #b00000000000000000000000)))
  )
)

;; agg_local(x3,x1)
(assert
  (= x3_0
     (fp.add RNE (ite e1_0 x0_0 (fp #b0 #b00000000 #b00000000000000000000000)) (ite e1_1 x1_0 (fp #b0 #b00000000 #b00000000000000000000000)))
  )
)

(assert
  (= x3_1
     (fp.add RNE (ite e1_0 x0_1 (fp #b0 #b00000000 #b00000000000000000000000)) (ite e1_1 x1_1 (fp #b0 #b00000000 #b00000000000000000000000)))
  )
)

(assert
  (= x3_2
     (fp.add RNE (ite e1_0 x0_2 (fp #b0 #b00000000 #b00000000000000000000000)) (ite e1_1 x1_2 (fp #b0 #b00000000 #b00000000000000000000000)))
  )
)

;; end local aggregation

;; Global aggregation
;; Compute global agg(x4)
(assert (= x4_0
          (fp.add RNE x0_0 x1_0)))
(assert (= x4_1
          (fp.add RNE x0_1 x1_1)))
(assert (= x4_2
          (fp.add RNE x0_2 x1_2)))
;; end global agg(x4)

;; Compute global agg(x5)
(assert (= x5_0
          (fp.add RNE x0_0 x1_0)))
(assert (= x5_1
          (fp.add RNE x0_1 x1_1)))
(assert (= x5_2
          (fp.add RNE x0_2 x1_2)))
;; end global agg(x5)

;; matrix multiplication
;;np.dot(FM,V) xV
;; declare node x6
(declare-const x6_0 Float32)
(declare-const x6_1 Float32)
(declare-const x6_2 Float32)

;; declare node x7
(declare-const x7_0 Float32)
(declare-const x7_1 Float32)
(declare-const x7_2 Float32)

(assert
  (= x6_0
     (fp.add RNE (fp.add RNE (fp.mul RNE x0_0 (fp #b1 #b01111001 #b01111000010100110010011)) (fp.mul RNE x0_1 (fp #b0 #b01111100 #b01010100110010100101100))) (fp.mul RNE x0_2 (fp #b0 #b01111011 #b00110000100010000100000)))
  )
)
(assert
  (= x6_1
     (fp.add RNE (fp.add RNE (fp.mul RNE x0_0 (fp #b1 #b01111101 #b10110011000101111001000)) (fp.mul RNE x0_1 (fp #b1 #b01111100 #b11000111011010010110010))) (fp.mul RNE x0_2 (fp #b0 #b01111100 #b00111101000100101010100)))
  )
)
(assert
  (= x6_2
     (fp.add RNE (fp.add RNE (fp.mul RNE x0_0 (fp #b1 #b01111110 #b00001001101110100110011)) (fp.mul RNE x0_1 (fp #b0 #b01111110 #b00001000111101010001000))) (fp.mul RNE x0_2 (fp #b0 #b01111101 #b01010011010011101000100)))
  )
)

(assert
  (= x7_0
     (fp.add RNE (fp.add RNE (fp.mul RNE x1_0 (fp #b1 #b01111001 #b01111000010100110010011)) (fp.mul RNE x1_1 (fp #b0 #b01111100 #b01010100110010100101100))) (fp.mul RNE x1_2 (fp #b0 #b01111011 #b00110000100010000100000)))
  )
)
(assert
  (= x7_1
     (fp.add RNE (fp.add RNE (fp.mul RNE x1_0 (fp #b1 #b01111101 #b10110011000101111001000)) (fp.mul RNE x1_1 (fp #b1 #b01111100 #b11000111011010010110010))) (fp.mul RNE x1_2 (fp #b0 #b01111100 #b00111101000100101010100)))
  )
)
(assert
  (= x7_2
     (fp.add RNE (fp.add RNE (fp.mul RNE x1_0 (fp #b1 #b01111110 #b00001001101110100110011)) (fp.mul RNE x1_1 (fp #b0 #b01111110 #b00001000111101010001000))) (fp.mul RNE x1_2 (fp #b0 #b01111101 #b01010011010011101000100)))
  )
)

;;np.dot(V,FM) + b_V
;; declare node x8
(declare-const x8_0 Float32)
(declare-const x8_1 Float32)
(declare-const x8_2 Float32)

;; declare node x9
(declare-const x9_0 Float32)
(declare-const x9_1 Float32)
(declare-const x9_2 Float32)

(assert
   (= x8_0
      (fp.add RNE x6_0 (fp #b0 #b01111101 #b01000111101000010010100))
   )
)
(assert
   (= x8_1
      (fp.add RNE x6_1 (fp #b1 #b01111100 #b01100101010101110011110))
   )
)
(assert
   (= x8_2
      (fp.add RNE x6_2 (fp #b0 #b01111100 #b11111100100000001001110))
   )
)

(assert
   (= x9_0
      (fp.add RNE x7_0 (fp #b0 #b01111101 #b01000111101000010010100))
   )
)
(assert
   (= x9_1
      (fp.add RNE x7_1 (fp #b1 #b01111100 #b01100101010101110011110))
   )
)
(assert
   (= x9_2
      (fp.add RNE x7_2 (fp #b0 #b01111100 #b11111100100000001001110))
   )
)

;;np.dot(agg_local,A) yA
;; declare node x10
(declare-const x10_0 Float32)
(declare-const x10_1 Float32)
(declare-const x10_2 Float32)

;; declare node x11
(declare-const x11_0 Float32)
(declare-const x11_1 Float32)
(declare-const x11_2 Float32)

(assert
  (= x10_0
     (fp.add RNE (fp.add RNE (fp.mul RNE x2_0 (fp #b1 #b01111110 #b11101111010000111100110)) (fp.mul RNE x2_1 (fp #b1 #b01111100 #b00101110010001111010010))) (fp.mul RNE x2_2 (fp #b1 #b01111011 #b11100000111100001000111)))
  )
)
(assert
  (= x10_1
     (fp.add RNE (fp.add RNE (fp.mul RNE x2_0 (fp #b0 #b01111001 #b01011110011010000000000)) (fp.mul RNE x2_1 (fp #b0 #b01111100 #b11010011011100110001100))) (fp.mul RNE x2_2 (fp #b0 #b01111101 #b01100010101111001100110)))
  )
)
(assert
  (= x10_2
     (fp.add RNE (fp.add RNE (fp.mul RNE x2_0 (fp #b0 #b01111101 #b10011001011001101101110)) (fp.mul RNE x2_1 (fp #b1 #b01111101 #b01111110101001110101001))) (fp.mul RNE x2_2 (fp #b1 #b01111100 #b11111011101001100101100)))
  )
)

(assert
  (= x11_0
     (fp.add RNE (fp.add RNE (fp.mul RNE x3_0 (fp #b1 #b01111110 #b11101111010000111100110)) (fp.mul RNE x3_1 (fp #b1 #b01111100 #b00101110010001111010010))) (fp.mul RNE x3_2 (fp #b1 #b01111011 #b11100000111100001000111)))
  )
)
(assert
  (= x11_1
     (fp.add RNE (fp.add RNE (fp.mul RNE x3_0 (fp #b0 #b01111001 #b01011110011010000000000)) (fp.mul RNE x3_1 (fp #b0 #b01111100 #b11010011011100110001100))) (fp.mul RNE x3_2 (fp #b0 #b01111101 #b01100010101111001100110)))
  )
)
(assert
  (= x11_2
     (fp.add RNE (fp.add RNE (fp.mul RNE x3_0 (fp #b0 #b01111101 #b10011001011001101101110)) (fp.mul RNE x3_1 (fp #b1 #b01111101 #b01111110101001110101001))) (fp.mul RNE x3_2 (fp #b1 #b01111100 #b11111011101001100101100)))
  )
)

;;np.dot(agg_local,A) + b_A
;; declare node x12
(declare-const x12_0 Float32)
(declare-const x12_1 Float32)
(declare-const x12_2 Float32)

;; declare node x13
(declare-const x13_0 Float32)
(declare-const x13_1 Float32)
(declare-const x13_2 Float32)

(assert
   (= x12_0
      (fp.add RNE x10_0 (fp #b0 #b01111110 #b01001011000011110100100))
   )
)
(assert
   (= x12_1
      (fp.add RNE x10_1 (fp #b1 #b01111011 #b11100110101011101000100))
   )
)
(assert
   (= x12_2
      (fp.add RNE x10_2 (fp #b0 #b01111110 #b10010110011011110101100))
   )
)

(assert
   (= x13_0
      (fp.add RNE x11_0 (fp #b0 #b01111110 #b01001011000011110100100))
   )
)
(assert
   (= x13_1
      (fp.add RNE x11_1 (fp #b1 #b01111011 #b11100110101011101000100))
   )
)
(assert
   (= x13_2
      (fp.add RNE x11_2 (fp #b0 #b01111110 #b10010110011011110101100))
   )
)

;;np.dot(agg_global,R) zR
;; declare node x14
(declare-const x14_0 Float32)
(declare-const x14_1 Float32)
(declare-const x14_2 Float32)

;; declare node x15
(declare-const x15_0 Float32)
(declare-const x15_1 Float32)
(declare-const x15_2 Float32)

(assert
  (= x14_0
     (fp.add RNE (fp.add RNE (fp.mul RNE x4_0 (fp #b0 #b01111011 #b00101111100101101000101)) (fp.mul RNE x4_1 (fp #b0 #b01111010 #b11110010110011111110011))) (fp.mul RNE x4_2 (fp #b0 #b01111010 #b11110100100001010110011)))
  )
)
(assert
  (= x14_1
     (fp.add RNE (fp.add RNE (fp.mul RNE x4_0 (fp #b1 #b01111110 #b00010010001110001111001)) (fp.mul RNE x4_1 (fp #b1 #b01111101 #b01110100001011111110000))) (fp.mul RNE x4_2 (fp #b1 #b01111100 #b00101011010110001001000)))
  )
)
(assert
  (= x14_2
     (fp.add RNE (fp.add RNE (fp.mul RNE x4_0 (fp #b0 #b01111100 #b00011000000001001110110)) (fp.mul RNE x4_1 (fp #b1 #b01111001 #b01100001010001001001110))) (fp.mul RNE x4_2 (fp #b1 #b01111010 #b10110010100001100001110)))
  )
)

(assert
  (= x15_0
     (fp.add RNE (fp.add RNE (fp.mul RNE x5_0 (fp #b0 #b01111011 #b00101111100101101000101)) (fp.mul RNE x5_1 (fp #b0 #b01111010 #b11110010110011111110011))) (fp.mul RNE x5_2 (fp #b0 #b01111010 #b11110100100001010110011)))
  )
)
(assert
  (= x15_1
     (fp.add RNE (fp.add RNE (fp.mul RNE x5_0 (fp #b1 #b01111110 #b00010010001110001111001)) (fp.mul RNE x5_1 (fp #b1 #b01111101 #b01110100001011111110000))) (fp.mul RNE x5_2 (fp #b1 #b01111100 #b00101011010110001001000)))
  )
)
(assert
  (= x15_2
     (fp.add RNE (fp.add RNE (fp.mul RNE x5_0 (fp #b0 #b01111100 #b00011000000001001110110)) (fp.mul RNE x5_1 (fp #b1 #b01111001 #b01100001010001001001110))) (fp.mul RNE x5_2 (fp #b1 #b01111010 #b10110010100001100001110)))
  )
)

;;np.dot(agg_global,R) + b_R
;; declare node x16
(declare-const x16_0 Float32)
(declare-const x16_1 Float32)
(declare-const x16_2 Float32)

;; declare node x17
(declare-const x17_0 Float32)
(declare-const x17_1 Float32)
(declare-const x17_2 Float32)

(assert
   (= x16_0
      (fp.add RNE x14_0 (fp #b1 #b01111011 #b10010011110110010100111))
   )
)
(assert
   (= x16_1
      (fp.add RNE x14_1 (fp #b1 #b01111101 #b10011101000010100111100))
   )
)
(assert
   (= x16_2
      (fp.add RNE x14_2 (fp #b1 #b01111100 #b01101110011110100111000))
   )
)

(assert
   (= x17_0
      (fp.add RNE x15_0 (fp #b1 #b01111011 #b10010011110110010100111))
   )
)
(assert
   (= x17_1
      (fp.add RNE x15_1 (fp #b1 #b01111101 #b10011101000010100111100))
   )
)
(assert
   (= x17_2
      (fp.add RNE x15_2 (fp #b1 #b01111100 #b01101110011110100111000))
   )
)

;;(np.dot(V,FM) + b_V)+(np.dot(A,agg_local) + b_A)+(np.dot(R,agg_global) + b_R)
;; declare node x18
(declare-const x18_0 Float32)
(declare-const x18_1 Float32)
(declare-const x18_2 Float32)

;; declare node x19
(declare-const x19_0 Float32)
(declare-const x19_1 Float32)
(declare-const x19_2 Float32)

(assert
   (= x18_0
      (fp.add RNE (fp.add RNE x8_0 x12_0) x16_0)
   )
)
(assert
   (= x18_1
      (fp.add RNE (fp.add RNE x8_1 x12_1) x16_1)
   )
)
(assert
   (= x18_2
      (fp.add RNE (fp.add RNE x8_2 x12_2) x16_2)
   )
)

(assert
   (= x19_0
      (fp.add RNE (fp.add RNE x9_0 x13_0) x17_0)
   )
)
(assert
   (= x19_1
      (fp.add RNE (fp.add RNE x9_1 x13_1) x17_1)
   )
)
(assert
   (= x19_2
      (fp.add RNE (fp.add RNE x9_2 x13_2) x17_2)
   )
)

;; applying activation function
;; activation function: ReLU
(define-fun ReLU ((x Float32)) Float32
  (ite (fp.gt x fp0) x fp0)
)
;; declare node x20
(declare-const x20_0 Float32)
(declare-const x20_1 Float32)
(declare-const x20_2 Float32)

;; declare node x21
(declare-const x21_0 Float32)
(declare-const x21_1 Float32)
(declare-const x21_2 Float32)

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
(declare-const x22_0 Float32)
(declare-const x22_1 Float32)
(declare-const x22_2 Float32)

;; declare node x23
(declare-const x23_0 Float32)
(declare-const x23_1 Float32)
(declare-const x23_2 Float32)

(assert
   (= x22_0
      (fp.add RNE (fp.mul RNE x20_0 (fp #b0 #b10000001 #b00110101100100100000100)) (fp #b1 #b10000000 #b00011010001100110011010))
   )
)
(assert
   (= x22_1
      (fp.add RNE (fp.mul RNE x20_1 (fp #b0 #b10000111 #b00111100001110100101000)) (fp #b0 #b01111100 #b10100011100001011111011))
   )
)
(assert
   (= x22_2
      (fp.add RNE (fp.mul RNE x20_2 (fp #b0 #b10000000 #b01011001011100101000001)) (fp #b1 #b10000000 #b00111110011101011111001))
   )
)

(assert
   (= x23_0
      (fp.add RNE (fp.mul RNE x21_0 (fp #b0 #b10000001 #b00110101100100100000100)) (fp #b1 #b10000000 #b00011010001100110011010))
   )
)
(assert
   (= x23_1
      (fp.add RNE (fp.mul RNE x21_1 (fp #b0 #b10000111 #b00111100001110100101000)) (fp #b0 #b01111100 #b10100011100001011111011))
   )
)
(assert
   (= x23_2
      (fp.add RNE (fp.mul RNE x21_2 (fp #b0 #b10000000 #b01011001011100101000001)) (fp #b1 #b10000000 #b00111110011101011111001))
   )
)

;; end layer

;; Linear Prediction np.dot(BN, W_LP) + b_LP
;; declare node x24
(declare-const x24_0 Float32)
(declare-const x24_1 Float32)

;; declare node x25
(declare-const x25_0 Float32)
(declare-const x25_1 Float32)

;; np.dot(BN, W_LP)
(assert
  (= x24_0
     (fp.add RNE (fp.add RNE (fp.mul RNE x22_0 (fp #b1 #b01111111 #b00101011000001001101110)) (fp.mul RNE x22_1 (fp #b0 #b01111110 #b01110011101011101011011))) (fp.mul RNE x22_2 (fp #b0 #b01111110 #b11110000101100011111000)))
  )
)
(assert
  (= x24_1
     (fp.add RNE (fp.add RNE (fp.mul RNE x22_0 (fp #b0 #b01111111 #b00011100110111000001001)) (fp.mul RNE x22_1 (fp #b0 #b01110111 #b11000011000100111010101))) (fp.mul RNE x22_2 (fp #b1 #b01111111 #b00000010100110110101000)))
  )
)

(assert
  (= x25_0
     (fp.add RNE (fp.add RNE (fp.mul RNE x23_0 (fp #b1 #b01111111 #b00101011000001001101110)) (fp.mul RNE x23_1 (fp #b0 #b01111110 #b01110011101011101011011))) (fp.mul RNE x23_2 (fp #b0 #b01111110 #b11110000101100011111000)))
  )
)
(assert
  (= x25_1
     (fp.add RNE (fp.add RNE (fp.mul RNE x23_0 (fp #b0 #b01111111 #b00011100110111000001001)) (fp.mul RNE x23_1 (fp #b0 #b01110111 #b11000011000100111010101))) (fp.mul RNE x23_2 (fp #b1 #b01111111 #b00000010100110110101000)))
  )
)

;;np.dot(BN, W_LP) + b_LP
;; declare node x26
(declare-const x26_0 Float32)
(declare-const x26_1 Float32)

;; declare node x27
(declare-const x27_0 Float32)
(declare-const x27_1 Float32)

(assert
   (= x26_0
      (fp.add RNE x24_0 (fp #b0 #b01111101 #b01001111000000101000000))
   )
)
(assert
   (= x26_1
      (fp.add RNE x24_1 (fp #b1 #b01111101 #b11001100001100011111000))
   )
)

(assert
   (= x27_0
      (fp.add RNE x25_0 (fp #b0 #b01111101 #b01001111000000101000000))
   )
)
(assert
   (= x27_1
      (fp.add RNE x25_1 (fp #b1 #b01111101 #b11001100001100011111000))
   )
)

;; end linear prediction layer

;;Binary classification
(define-fun argmax ((x Float32) (y Float32)) Int
  (ite (fp.gt x y) 0 1)
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
