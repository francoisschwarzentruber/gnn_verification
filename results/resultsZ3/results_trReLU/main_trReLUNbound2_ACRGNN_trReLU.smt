;; adjacency matrix of unknown graph
(declare-const e0_0 Bool)
(declare-const e0_1 Bool)
(declare-const e1_0 Bool)
(declare-const e1_1 Bool)

;; declare feature x1
(declare-const x1_0 (_ BitVec 8))
(declare-const x1_1 (_ BitVec 8))

;; declare feature x2
(declare-const x2_0 (_ BitVec 8))
(declare-const x2_1 (_ BitVec 8))

;; precondition x1[0] == 1
(assert (= x1_0 #x01))

;; precondition x2[0] == 2
(assert (= x2_0 #x02))

;; decline features for the local aggregation.
;; declare feature x3
(declare-const x3_0 (_ BitVec 8))
(declare-const x3_1 (_ BitVec 8))

;; declare feature x4
(declare-const x4_0 (_ BitVec 8))
(declare-const x4_1 (_ BitVec 8))

;; decline features for the global aggregation.
;; declare feature x5
(declare-const x5_0 (_ BitVec 8))
(declare-const x5_1 (_ BitVec 8))

;; declare feature x6
(declare-const x6_0 (_ BitVec 8))
(declare-const x6_1 (_ BitVec 8))

;; Compute agg(x3,x1)
(assert (= x3_0
          (bvadd 
             (ite e0_0 x1_0 #x00)
             (ite e0_1 x1_1 #x00)
          )))
(assert (= x3_1
          (bvadd 
             (ite e1_0 x1_0 #x00)
             (ite e1_1 x1_1 #x00)
          )))
;; end agg(x3,x1)

;; Compute agg(x4,x2)
(assert (= x4_0
          (bvadd 
             (ite e0_0 x2_0 #x00)
             (ite e0_1 x2_1 #x00)
          )))
(assert (= x4_1
          (bvadd 
             (ite e1_0 x2_0 #x00)
             (ite e1_1 x2_1 #x00)
          )))
;; end agg(x4,x2)

;; compute aggG(x5,x1)
(assert (= x5_0
         (bvadd x1_0 x1_1) ))
(assert (= x5_1
         (bvadd x1_0 x1_1) ))
;; end aggG(x5,x1)

;; compute aggG(x6,x2)
(assert (= x6_0
         (bvadd x2_0 x2_1) ))
(assert (= x6_1
         (bvadd x2_0 x2_1) ))
;; end aggG(x6,x2)

;; Calcolate (A(previousFeatures) + Magg(aggPreviousFeatures) + MaggG(aggGPreviousFeatures) + b)
;; declare feature x7
(declare-const x7_0 (_ BitVec 8))
(declare-const x7_1 (_ BitVec 8))

;; linear layer output x7 from previous, agg, aggG (row 0)
(assert (= x7_0
         (bvadd
           (bvmul x1_0 #x01)
           (bvmul x2_0 #x02)
           (bvmul x3_0 #x00)
           (bvmul x4_0 #x00)
           (bvmul x5_0 #x00)
           (bvmul x6_0 #x00)
           #x05
         )))
(assert (= x7_1
         (bvadd
           (bvmul x1_1 #x01)
           (bvmul x2_1 #x02)
           (bvmul x3_1 #x00)
           (bvmul x4_1 #x00)
           (bvmul x5_1 #x00)
           (bvmul x6_1 #x00)
           #x05
         )))
;; end linear layer for x7

;; declare feature to store the results after applying AF
;; declare feature x8
(declare-const x8_0 (_ BitVec 8))
(declare-const x8_1 (_ BitVec 8))

;; calculate x8= trReLU(x7)
(assert (= x8_0
        (ite (bvslt x7_0 #x00)         ;; if x < 0
             #x00                                    ;;   -> 0
             (ite (bvsle x7_0 #x01)     ;; else if x <= 1
                  x7_0                       ;;        -> x
                  #x01))))                         ;; else -> 1
(assert (= x8_1
        (ite (bvslt x7_1 #x00)         ;; if x < 0
             #x00                                    ;;   -> 0
             (ite (bvsle x7_1 #x01)     ;; else if x <= 1
                  x7_1                       ;;        -> x
                  #x01))))                         ;; else -> 1
;; end

;; postcondition x8[0] == 0
(assert (not (= x8_0 #x00)))

(check-sat)
(get-value (x1_0 x1_1 x2_0 x2_1 x3_0 x3_1 x4_0 x4_1 x5_0 x5_1 x6_0 x6_1 x7_0 x7_1 x8_0 x8_1))
(check-sat)
(get-value (x1_0 x1_1 x2_0 x2_1 x3_0 x3_1 x4_0 x4_1 x5_0 x5_1 x6_0 x6_1 x7_0 x7_1 x8_0 x8_1))
