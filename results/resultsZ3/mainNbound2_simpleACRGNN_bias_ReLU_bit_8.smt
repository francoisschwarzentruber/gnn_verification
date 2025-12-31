;; Saturating arithmetic helpers for signed (_ BitVec 8)
;; Saturating for addition
(define-fun saturating-add ((x (_ BitVec 8)) (y (_ BitVec 8))) (_ BitVec 8)
  (let ((sx ((_ sign_extend 8) x))
        (sy ((_ sign_extend 8) y))
        (max ((_ sign_extend 8) #x7f))
        (min ((_ sign_extend 8) #x80)))
    (let ((s (bvadd sx sy)))
      (let ((clamped (ite (bvslt s min) min (ite (bvsgt s max) max s))))
        ((_ extract 7 0) clamped)))))

;; Saturating for multiplication
(define-fun saturating-mul ((x (_ BitVec 8)) (y (_ BitVec 8))) (_ BitVec 8)
  (let ((sx ((_ sign_extend 8) x))
        (sy ((_ sign_extend 8) y))
        (max ((_ sign_extend 8) #x7f))
        (min ((_ sign_extend 8) #x80)))
    (let ((p (bvmul sx sy)))
      (let ((clamped (ite (bvslt p min) min (ite (bvsgt p max) max p))))
        ((_ extract 7 0) clamped)))))

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
          (saturating-add 
             (ite e0_0 x1_0 #x00)
             (ite e0_1 x1_1 #x00)
          )))
(assert (= x3_1
          (saturating-add 
             (ite e1_0 x1_0 #x00)
             (ite e1_1 x1_1 #x00)
          )))
;; end agg(x3,x1)

;; Compute agg(x4,x2)
(assert (= x4_0
          (saturating-add 
             (ite e0_0 x2_0 #x00)
             (ite e0_1 x2_1 #x00)
          )))
(assert (= x4_1
          (saturating-add 
             (ite e1_0 x2_0 #x00)
             (ite e1_1 x2_1 #x00)
          )))
;; end agg(x4,x2)

;; compute aggG(x5,x1)
(assert (= x5_0
         (saturating-add x1_0 x1_1) ))
(assert (= x5_1
         (saturating-add x1_0 x1_1) ))
;; end aggG(x5,x1)

;; compute aggG(x6,x2)
(assert (= x6_0
         (saturating-add x2_0 x2_1) ))
(assert (= x6_1
         (saturating-add x2_0 x2_1) ))
;; end aggG(x6,x2)

;; Calcolate (A(previousFeatures) + Magg(aggPreviousFeatures) + MaggG(aggGPreviousFeatures) + b)
;; declare feature x7
(declare-const x7_0 (_ BitVec 8))
(declare-const x7_1 (_ BitVec 8))

;; linear layer output x7 from previous, agg, aggG (row 0)
(assert (= x7_0
         (saturating-add
           (saturating-mul x1_0 #x01)
         (saturating-add
           (saturating-mul x2_0 #x02)
         (saturating-add
           (saturating-mul x3_0 #x00)
         (saturating-add
           (saturating-mul x4_0 #x00)
         (saturating-add
           (saturating-mul x5_0 #x00)
         (saturating-add
           (saturating-mul x6_0 #x00)
           #x05
  ))))))))
(assert (= x7_1
         (saturating-add
           (saturating-mul x1_1 #x01)
         (saturating-add
           (saturating-mul x2_1 #x02)
         (saturating-add
           (saturating-mul x3_1 #x00)
         (saturating-add
           (saturating-mul x4_1 #x00)
         (saturating-add
           (saturating-mul x5_1 #x00)
         (saturating-add
           (saturating-mul x6_1 #x00)
           #x05
  ))))))))
;; end linear layer for x7

;; declare feature to store the results after applying AF
;; declare feature x8
(declare-const x8_0 (_ BitVec 8))
(declare-const x8_1 (_ BitVec 8))

;; calculate x8= ReLU(x7)
(assert (= x8_0
        (ite (bvsge x7_0 #x00)   ;; if x_number_index >= 0 (signed)
             x7_0                ;; keep 
             #x00)))            ;; else return 0
(assert (= x8_1
        (ite (bvsge x7_1 #x00)   ;; if x_number_index >= 0 (signed)
             x7_1                ;; keep 
             #x00)))            ;; else return 0
;; end

;; postcondition x8[0] == 0
(assert (not (= x8_0 #x00)))

(check-sat)
(get-value (x1_0 x1_1 x2_0 x2_1 x3_0 x3_1 x4_0 x4_1 x5_0 x5_1 x6_0 x6_1 x7_0 x7_1 x8_0 x8_1))
(check-sat)
(get-value (x1_0 x1_1 x2_0 x2_1 x3_0 x3_1 x4_0 x4_1 x5_0 x5_1 x6_0 x6_1 x7_0 x7_1 x8_0 x8_1))
