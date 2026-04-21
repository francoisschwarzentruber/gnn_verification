;;This is the file of the Z3 for the demonstration

;; adjacency matrix of known graph 
;; adj_matrix=np.array([[0,1],[1,0]], dtype=np.float32)

(declare-const e0_0 Bool)
(declare-const e0_1 Bool)
(declare-const e1_0 Bool)
(declare-const e1_1 Bool)

;; hard code the example one.
(assert (= e0_0 false))
(assert (= e0_1 true))
(assert (= e1_0 true))
(assert (= e1_1 false))

;; Feature Matrix
;;[[0,0,1]
;; [1,0,0]]

;; declare feature f0
(declare-const f0_0 Float32)
(declare-const f0_1 Float32)

;; precondition f0[0] == 0 
(assert (= f0_0 (fp #b0 #b00000000 #b00000000000000000000000)))

;; precondition f0[1] == 1
(assert (= f0_1 (fp #b0 #b01111111 #b00000000000000000000000)))

;; declare feature f1
(declare-const f1_0 Float32)
(declare-const f1_1 Float32)

;; precondition f1[0] == 0 
(assert (= f1_0 (fp #b0 #b00000000 #b00000000000000000000000)))

;; precondition f1[1] == 0 
(assert (= f1_1 (fp #b0 #b00000000 #b00000000000000000000000)))

;; declare feature f2
(declare-const f2_0 Float32)
(declare-const f2_1 Float32)

;; precondition f2[0] == 1 
(assert (= f2_0 (fp #b0 #b01111111 #b00000000000000000000000)))

;; precondition f2[1] == 0 
(assert (= f2_1 (fp #b0 #b00000000 #b00000000000000000000000)))

;; Local aggregation (across neighbours) 

;; agg_local(f3,f0) 
(declare-const f3_0 Float32)
(declare-const f3_1 Float32)

(assert
  (= f3_0
     (fp.add RNE
        (ite e0_0 f0_0 (fp #b0 #b00000000 #b00000000000000000000000))
        (ite e0_1 f0_1 (fp #b0 #b00000000 #b00000000000000000000000))
     )
  )
)

(assert
  (= f3_1
     (fp.add RNE
        (ite e0_1 f0_0 (fp #b0 #b00000000 #b00000000000000000000000))
        (ite e1_1 f0_1 (fp #b0 #b00000000 #b00000000000000000000000))
     )
  )
)

;; agg_local(f4,f1) 
(declare-const f4_0 Float32)
(declare-const f4_1 Float32)

(assert
  (= f4_0
     (fp.add RNE
        (ite e0_0 f1_0 (fp #b0 #b00000000 #b00000000000000000000000))
        (ite e0_1 f1_1 (fp #b0 #b00000000 #b00000000000000000000000))
     )
  )
)

(assert
  (= f4_1
     (fp.add RNE
        (ite e0_1 f1_0 (fp #b0 #b00000000 #b00000000000000000000000))
        (ite e1_1 f1_1 (fp #b0 #b00000000 #b00000000000000000000000))
     )
  )
)

;; agg_local(f5,f2) 
(declare-const f5_0 Float32)
(declare-const f5_1 Float32)

(assert
  (= f5_0
     (fp.add RNE
        (ite e0_0 f2_0 (fp #b0 #b00000000 #b00000000000000000000000))
        (ite e0_1 f2_1 (fp #b0 #b00000000 #b00000000000000000000000))
     )
  )
)

(assert
  (= f5_1
     (fp.add RNE
        (ite e0_1 f2_0 (fp #b0 #b00000000 #b00000000000000000000000))
        (ite e1_1 f2_1 (fp #b0 #b00000000 #b00000000000000000000000))
     )
  )
)

;; Global aggregation (across graph)


;; agg_global(f6,f0) 
(declare-const f6_0 Float32)
(declare-const f6_1 Float32)

(assert
  (= f6_0
     (fp.add RNE f0_0 f0_1)
  )
)

(assert
  (= f6_1
     (fp.add RNE f0_0 f0_1)
  )
)

;; agg_global(f7,f1) 
(declare-const f7_0 Float32)
(declare-const f7_1 Float32)

(assert
  (= f7_0
     (fp.add RNE f1_0 f1_1)
  )
)

(assert
  (= f7_1
     (fp.add RNE f1_0 f1_1)
  )
)

;; agg_global(f8,f2) 
(declare-const f8_0 Float32)
(declare-const f8_1 Float32)

(assert
  (= f8_0
     (fp.add RNE f2_0 f2_1)
  )
)

(assert
  (= f8_1
     (fp.add RNE f2_0 f2_1)
  )
)

;; matrix multiplication

;;np.dot(V,FM)

(declare-const f9_0 Float32)
(declare-const f9_1 Float32)

(assert
  (= f9_0
     (fp.add RNE
       (fp.add RNE
         (fp.mul RNE (fp #b1 #b01111001 #b01111000010100110010011) f0_0)
         (fp.mul RNE (fp #b0 #b01111100 #b01010100110010100101100) f1_0)
       )
       (fp.mul RNE (fp #b0 #b01111011 #b00110000100010000100000) f2_0)
     )
  )
)

(assert
  (= f9_1
     (fp.add RNE
       (fp.add RNE
         (fp.mul RNE (fp #b1 #b01111001 #b01111000010100110010011) f0_1)
         (fp.mul RNE (fp #b0 #b01111100 #b01010100110010100101100) f1_1)
       )
       (fp.mul RNE (fp #b0 #b01111011 #b00110000100010000100000) f2_1)
     )
  )
)

(declare-const f10_0 Float32)
(declare-const f10_1 Float32)

(assert
  (= f10_0
     (fp.add RNE
       (fp.add RNE
         (fp.mul RNE (fp #b1 #b01111101 #b10110011000101111001000) f0_0)
         (fp.mul RNE (fp #b1 #b01111100 #b11000111011010010110010) f1_0)
       )
       (fp.mul RNE (fp #b0 #b01111100 #b00111101000100101010100) f2_0)
     )
  )
)

(assert
  (= f10_1
     (fp.add RNE
       (fp.add RNE
         (fp.mul RNE (fp #b1 #b01111101 #b10110011000101111001000) f0_1)
         (fp.mul RNE (fp #b1 #b01111100 #b11000111011010010110010) f1_1)
       )
       (fp.mul RNE (fp #b0 #b01111100 #b00111101000100101010100) f2_1)
     )
  )
)

(declare-const f11_0 Float32)
(declare-const f11_1 Float32)

(assert
  (= f11_0
     (fp.add RNE
       (fp.add RNE
         (fp.mul RNE (fp #b1 #b01111110 #b00001001101110100110011) f0_0)
         (fp.mul RNE (fp #b0 #b01111110 #b00001000111101010001000) f1_0)
       )
       (fp.mul RNE (fp #b0 #b01111101 #b01010011010011101000100) f2_0)
     )
  )
)

(assert
  (= f11_1
     (fp.add RNE
       (fp.add RNE
         (fp.mul RNE (fp #b1 #b01111110 #b00001001101110100110011) f0_1)
         (fp.mul RNE (fp #b0 #b01111110 #b00001000111101010001000) f1_1)
       )
       (fp.mul RNE (fp #b0 #b01111101 #b01010011010011101000100) f2_1)
     )
  )
)

;;np.dot(V,FM) + b_V
(declare-const f12_0 Float32)
(declare-const f12_1 Float32)

(assert
   (= f12_0
      (fp.add RNE f9_0 (fp #b0 #b01111101 #b01000111101000010010100))
   )
)

(assert
   (= f12_1
      (fp.add RNE f9_1 (fp #b0 #b01111101 #b01000111101000010010100))
   )
)

(declare-const f13_0 Float32)
(declare-const f13_1 Float32)

(assert
   (= f13_0
      (fp.add RNE f10_0 (fp #b1 #b01111100 #b01100101010101110011110))
   )
)

(assert
   (= f13_1
      (fp.add RNE f10_1 (fp #b1 #b01111100 #b01100101010101110011110))
   )
)


(declare-const f14_0 Float32)
(declare-const f14_1 Float32)

(assert
   (= f14_0
      (fp.add RNE f11_0 (fp #b0 #b01111100 #b11111100100000001001110))
   )
)

(assert
   (= f14_1
      (fp.add RNE f11_1 (fp #b0 #b01111100 #b11111100100000001001110))
   )
)


;;np.dot(A,agg_local)

(declare-const f15_0 Float32)
(declare-const f15_1 Float32)

(assert
  (= f15_0
     (fp.add RNE
       (fp.add RNE
         (fp.mul RNE (fp #b1 #b01111110 #b11101111010000111100110) f3_0)
         (fp.mul RNE (fp #b1 #b01111100 #b00101110010001111010010) f4_0)
       )
       (fp.mul RNE (fp #b1 #b01111011 #b11100000111100001000111) f5_0)
     )
  )
)

(assert
  (= f15_1
     (fp.add RNE
       (fp.add RNE
         (fp.mul RNE (fp #b1 #b01111110 #b11101111010000111100110) f3_1)
         (fp.mul RNE (fp #b1 #b01111100 #b00101110010001111010010) f4_1)
       )
       (fp.mul RNE (fp #b1 #b01111011 #b11100000111100001000111) f5_1)
     )
  )
)

(declare-const f16_0 Float32)
(declare-const f16_1 Float32)

(assert
  (= f16_0
     (fp.add RNE
       (fp.add RNE
         (fp.mul RNE (fp #b0 #b01111001 #b01011110011010000000000) f3_0)
         (fp.mul RNE (fp #b0 #b01111100 #b11010011011100110001100) f4_0)
       )
       (fp.mul RNE (fp #b0 #b01111101 #b01100010101111001100110) f5_0)
     )
  )
)

(assert
  (= f16_1
     (fp.add RNE
       (fp.add RNE
         (fp.mul RNE (fp #b0 #b01111001 #b01011110011010000000000) f3_1)
         (fp.mul RNE (fp #b0 #b01111100 #b11010011011100110001100) f4_1)
       )
       (fp.mul RNE (fp #b0 #b01111101 #b01100010101111001100110) f5_1)
     )
  )
)

(declare-const f17_0 Float32)
(declare-const f17_1 Float32)

(assert
  (= f17_0
     (fp.add RNE
       (fp.add RNE
         (fp.mul RNE (fp #b0 #b01111101 #b10011001011001101101110) f3_0)
         (fp.mul RNE (fp #b1 #b01111101 #b01111110101001110101001) f4_0)
       )
       (fp.mul RNE (fp #b1 #b01111100 #b11111011101001100101100) f5_0)
     )
  )
)

(assert
  (= f17_1
     (fp.add RNE
       (fp.add RNE
         (fp.mul RNE (fp #b0 #b01111101 #b10011001011001101101110) f3_1)
         (fp.mul RNE (fp #b1 #b01111101 #b01111110101001110101001) f4_1)
       )
       (fp.mul RNE (fp #b1 #b01111100 #b11111011101001100101100) f5_1)
     )
  )
)

;;np.dot(A,agg_local) + b_A
(declare-const f18_0 Float32)
(declare-const f18_1 Float32)

(assert
   (= f18_0
      (fp.add RNE f15_0 (fp #b0 #b01111110 #b01001011000011110100100))
   )
)

(assert
   (= f18_1
      (fp.add RNE f15_1 (fp #b0 #b01111110 #b01001011000011110100100))
   )
)

(declare-const f19_0 Float32)
(declare-const f19_1 Float32)

(assert
   (= f19_0
      (fp.add RNE f16_0 (fp #b1 #b01111011 #b11100110101011101000100))
   )
)

(assert
   (= f19_1
      (fp.add RNE f16_1 (fp #b1 #b01111011 #b11100110101011101000100))
   )
)

(declare-const f20_0 Float32)
(declare-const f20_1 Float32)

(assert
   (= f20_0
      (fp.add RNE f17_0 (fp #b0 #b01111110 #b10010110011011110101100))
   )
)

(assert
   (= f20_1
      (fp.add RNE f17_1 (fp #b0 #b01111110 #b10010110011011110101100))
   )
)


;;np.dot(R,agg_global)

(declare-const f21_0 Float32)
(declare-const f21_1 Float32)

(assert
  (= f21_0
     (fp.add RNE
       (fp.add RNE
         (fp.mul RNE (fp #b0 #b01111011 #b00101111100101101000101) f6_0)
         (fp.mul RNE (fp #b0 #b01111010 #b11110010110011111110011) f7_0)
       )
       (fp.mul RNE (fp #b0 #b01111010 #b11110100100001010110011) f8_0)
     )
  )
)

(assert
  (= f21_1
     (fp.add RNE
       (fp.add RNE
         (fp.mul RNE (fp #b0 #b01111011 #b00101111100101101000101) f6_1)
         (fp.mul RNE (fp #b0 #b01111010 #b11110010110011111110011) f7_1)
       )
       (fp.mul RNE (fp #b0 #b01111010 #b11110100100001010110011) f8_1)
     )
  )
)

(declare-const f22_0 Float32)
(declare-const f22_1 Float32)

(assert
  (= f22_0
     (fp.add RNE
       (fp.add RNE
         (fp.mul RNE (fp #b1 #b01111110 #b00010010001110001111001) f6_0)
         (fp.mul RNE (fp #b1 #b01111101 #b01110100001011111110000) f7_0)
       )
       (fp.mul RNE (fp #b1 #b01111100 #b00101011010110001001000) f8_0)
     )
  )
)

(assert
  (= f22_1
     (fp.add RNE
       (fp.add RNE
         (fp.mul RNE (fp #b1 #b01111110 #b00010010001110001111001) f6_1)
         (fp.mul RNE (fp #b1 #b01111101 #b01110100001011111110000) f7_1)
       )
       (fp.mul RNE (fp #b1 #b01111100 #b00101011010110001001000) f8_1)
     )
  )
)

(declare-const f23_0 Float32)
(declare-const f23_1 Float32)

(assert
  (= f23_0
     (fp.add RNE
       (fp.add RNE
         (fp.mul RNE (fp #b0 #b01111100 #b00011000000001001110110) f6_0)
         (fp.mul RNE (fp #b1 #b01111001 #b01100001010001001001110) f7_0)
       )
       (fp.mul RNE (fp #b1 #b01111010 #b10110010100001100001110) f8_0)
     )
  )
)

(assert
  (= f23_1
     (fp.add RNE
       (fp.add RNE
         (fp.mul RNE (fp #b0 #b01111100 #b00011000000001001110110) f6_1)
         (fp.mul RNE (fp #b1 #b01111001 #b01100001010001001001110) f7_1)
       )
       (fp.mul RNE (fp #b1 #b01111010 #b10110010100001100001110) f8_1)
     )
  )
)

;;np.dot(R,agg_global) + b_R
(declare-const f24_0 Float32)
(declare-const f24_1 Float32)

(assert
   (= f24_0
      (fp.add RNE f21_0 (fp #b1 #b01111011 #b10010011110110010100111))
   )
)

(assert
   (= f24_1
      (fp.add RNE f21_1 (fp #b1 #b01111011 #b10010011110110010100111))
   )
)

(declare-const f25_0 Float32)
(declare-const f25_1 Float32)

(assert
   (= f25_0
      (fp.add RNE f22_0 (fp #b1 #b01111101 #b10011101000010100111100))
   )
)

(assert
   (= f25_1
      (fp.add RNE f22_1 (fp #b1 #b01111101 #b10011101000010100111100))
   )
)

(declare-const f26_0 Float32)
(declare-const f26_1 Float32)

(assert
   (= f26_0
      (fp.add RNE f23_0 (fp #b1 #b01111100 #b01101110011110100111000))
   )
)

(assert
   (= f26_1
      (fp.add RNE f23_1 (fp #b1 #b01111100 #b01101110011110100111000))
   )
)

;; (np.dot(V,FM) + b_V)+(np.dot(A,agg_local) + b_A)+(np.dot(R,agg_global) + b_R)
(declare-const f27_0 Float32)
(declare-const f27_1 Float32)

(assert
  (= f27_0
     (fp.add RNE
       (fp.add RNE
         f12_0
         f18_0
       )
       f24_0
     )
  )
)

(assert
  (= f27_1
     (fp.add RNE
       (fp.add RNE
         f12_1
         f18_1
       )
       f24_1
     )
  )
)

(declare-const f28_0 Float32)
(declare-const f28_1 Float32)

(assert
  (= f28_0
     (fp.add RNE
       (fp.add RNE
         f13_0
         f19_0
       )
       f25_0
     )
  )
)

(assert
  (= f28_1
     (fp.add RNE
       (fp.add RNE
         f13_1
         f19_1
       )
       f25_1
     )
  )
)

(declare-const f29_0 Float32)
(declare-const f29_1 Float32)
(assert
  (= f29_0
     (fp.add RNE
       (fp.add RNE
         f14_0
         f20_0
       )
       f26_0
     )
  )
)

(assert
  (= f29_1
     (fp.add RNE
       (fp.add RNE
         f14_1
         f20_1
       )
       f26_1
     )
  )
)

;; applying activation function
(define-fun fp0 () Float32 (fp #b0 #b00000000 #b00000000000000000000000))

(define-fun relu ((x Float32)) Float32
  (ite (fp.gt x fp0) x fp0)
)

(declare-const f30_0 Float32)
(declare-const f30_1 Float32)

(assert (= f30_0 (relu f27_0)))
(assert (= f30_1 (relu f27_1)))

(declare-const f31_0 Float32)
(declare-const f31_1 Float32)

(assert (= f31_0 (relu f28_0)))
(assert (= f31_1 (relu f28_1)))

(declare-const f32_0 Float32)
(declare-const f32_1 Float32)

(assert (= f32_0 (relu f29_0)))
(assert (= f32_1 (relu f29_1)))

;; applyinh Batch Normalization. Linear form: bn_a * act + bn_c
;; a * act + c
(declare-const f33_0 Float32)
(declare-const f33_1 Float32)

(assert
  (= f33_0
     (fp.add RNE
       (fp.mul RNE (fp #b0 #b10000001 #b00110101100100100000100) f30_0)
       (fp #b1 #b10000000 #b00011010001100110011010)
     )
  )
)

(assert
  (= f33_1
     (fp.add RNE
       (fp.mul RNE (fp #b0 #b10000001 #b00110101100100100000100) f30_1)
       (fp #b1 #b10000000 #b00011010001100110011010)
     )
  )
)

(declare-const f34_0 Float32)
(declare-const f34_1 Float32)

(assert
  (= f34_0
     (fp.add RNE
       (fp.mul RNE (fp #b0 #b10000111 #b00111100001110100101000) f31_0)
       (fp #b0 #b01111100 #b10100011100001011111011)
     )
  )
)

(assert
  (= f34_1
     (fp.add RNE
       (fp.mul RNE (fp #b0 #b10000111 #b00111100001110100101000) f31_1)
       (fp #b0 #b01111100 #b10100011100001011111011)
     )
  )
)

(declare-const f35_0 Float32)
(declare-const f35_1 Float32)

(assert
  (= f35_0
     (fp.add RNE
       (fp.mul RNE (fp #b0 #b10000000 #b01011001011100101000001) f32_0)
       (fp #b1 #b10000000 #b00111110011101011111001)
     )
  )
)

(assert
  (= f35_1
     (fp.add RNE
       (fp.mul RNE (fp #b0 #b10000000 #b01011001011100101000001) f32_1)
       (fp #b1 #b10000000 #b00111110011101011111001)
     )
  )
)

;;Layer finishes

;; Conv before final classification np.dpt(W_LP, BN) + b_LP
;; np.dpt(W_LP, BN)
(declare-const f36_0 Float32)
(declare-const f36_1 Float32)

(assert
  (= f36_0
     (fp.add RNE
       (fp.add RNE
         (fp.mul RNE (fp #b1 #b01111111 #b00101011000001001101110) f33_0)
         (fp.mul RNE (fp #b0 #b01111110 #b01110011101011101011011) f34_0)
       )
       (fp.mul RNE (fp #b0 #b01111110 #b11110000101100011111000) f35_0)
     )
  )
)

(assert
  (= f36_1
     (fp.add RNE
       (fp.add RNE
         (fp.mul RNE (fp #b1 #b01111111 #b00101011000001001101110) f33_1)
         (fp.mul RNE (fp #b0 #b01111110 #b01110011101011101011011) f34_1)
       )
       (fp.mul RNE (fp #b0 #b01111110 #b11110000101100011111000) f35_1)
     )
  )
)

(declare-const f37_0 Float32)
(declare-const f37_1 Float32)

(assert
  (= f37_0
     (fp.add RNE
       (fp.add RNE
         (fp.mul RNE (fp #b0 #b01111111 #b00011100110111000001001) f33_0)
         (fp.mul RNE (fp #b0 #b01110111 #b11000011000100111010101) f34_0)
       )
       (fp.mul RNE (fp #b1 #b01111111 #b00000010100110110101000) f35_0)
     )
  )
)

(assert
  (= f37_1
     (fp.add RNE
       (fp.add RNE
         (fp.mul RNE (fp #b0 #b01111111 #b00011100110111000001001) f33_1)
         (fp.mul RNE (fp #b0 #b01110111 #b11000011000100111010101) f34_1)
       )
       (fp.mul RNE (fp #b1 #b01111111 #b00000010100110110101000) f35_1)
     )
  )
)

;;np.dpt(W_LP, BN) + b_LP
(declare-const f38_0 Float32)
(declare-const f38_1 Float32)

(assert
   (= f38_0
      (fp.add RNE f36_0 (fp #b0 #b01111101 #b01001111000000101000000))
   )
)

(assert
   (= f38_1
      (fp.add RNE f36_1 (fp #b0 #b01111101 #b01001111000000101000000))
   )
)


(declare-const f39_0 Float32)
(declare-const f39_1 Float32)

(assert
   (= f39_0
      (fp.add RNE f37_0 (fp #b1 #b01111101 #b11001100001100011111000))
   )
)

(assert
   (= f39_1
      (fp.add RNE f37_1 (fp #b1 #b01111101 #b11001100001100011111000))
   )
)

;;Binary classification

(define-fun argmax ((x Float32) (y Float32)) Int
  (ite (fp.gt x y) 0 1)
)

(declare-const f40_0 Int)
(declare-const f40_1 Int)

(assert (= f40_0 (argmax f38_0 f39_0)))
(assert (= f40_1 (argmax f38_1 f39_1)))

(check-sat)
(get-value (f22_1 f19_0 f40_0 f40_1))