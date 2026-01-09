;; Saturating arithmetic helpers for signed (_ BitVec 32)
;; Saturating for addition
(define-fun saturating-add ((x (_ BitVec 32)) (y (_ BitVec 32))) (_ BitVec 32)
  (let ((sx ((_ sign_extend 32) x))
        (sy ((_ sign_extend 32) y))
        (max ((_ sign_extend 32) #x7fffffff))
        (min ((_ sign_extend 32) #x80000000)))
    (let ((s (bvadd sx sy)))
      (let ((clamped (ite (bvslt s min) min (ite (bvsgt s max) max s))))
        ((_ extract 31 0) clamped)))))

;; Saturating for multiplication
(define-fun saturating-mul ((x (_ BitVec 32)) (y (_ BitVec 32))) (_ BitVec 32)
  (let ((sx ((_ sign_extend 32) x))
        (sy ((_ sign_extend 32) y))
        (max ((_ sign_extend 32) #x7fffffff))
        (min ((_ sign_extend 32) #x80000000)))
    (let ((p (bvmul sx sy)))
      (let ((clamped (ite (bvslt p min) min (ite (bvsgt p max) max p))))
        ((_ extract 31 0) clamped)))))

;; adjacency matrix of unknown graph
(declare-const e0_0 Bool)
(declare-const e0_1 Bool)
(declare-const e0_2 Bool)
(declare-const e1_0 Bool)
(declare-const e1_1 Bool)
(declare-const e1_2 Bool)
(declare-const e2_0 Bool)
(declare-const e2_1 Bool)
(declare-const e2_2 Bool)

;; declare feature x1
(declare-const x1_0 (_ BitVec 32))
(declare-const x1_1 (_ BitVec 32))
(declare-const x1_2 (_ BitVec 32))

;; precondition x1[0] == 0 || x1[0] == 1
(assert (or (= x1_0 #x00000000) (= x1_0 #x00000001)))

;; precondition x1[1] == 0 || x1[1] == 1
(assert (or (= x1_1 #x00000000) (= x1_1 #x00000001)))

;; precondition x1[2] == 0 || x1[2] == 1
(assert (or (= x1_2 #x00000000) (= x1_2 #x00000001)))

;; declare feature x2
(declare-const x2_0 (_ BitVec 32))
(declare-const x2_1 (_ BitVec 32))
(declare-const x2_2 (_ BitVec 32))

;; precondition x2[0] == 0 || x2[0] == 1
(assert (or (= x2_0 #x00000000) (= x2_0 #x00000001)))

;; precondition x2[1] == 0 || x2[1] == 1
(assert (or (= x2_1 #x00000000) (= x2_1 #x00000001)))

;; precondition x2[2] == 0 || x2[2] == 1
(assert (or (= x2_2 #x00000000) (= x2_2 #x00000001)))

;; declare feature x3
(declare-const x3_0 (_ BitVec 32))
(declare-const x3_1 (_ BitVec 32))
(declare-const x3_2 (_ BitVec 32))

;; precondition x3[0] == 0 || x3[0] == 1
(assert (or (= x3_0 #x00000000) (= x3_0 #x00000001)))

;; precondition x3[1] == 0 || x3[1] == 1
(assert (or (= x3_1 #x00000000) (= x3_1 #x00000001)))

;; precondition x3[2] == 0 || x3[2] == 1
(assert (or (= x3_2 #x00000000) (= x3_2 #x00000001)))

;; declare feature x4
(declare-const x4_0 (_ BitVec 32))
(declare-const x4_1 (_ BitVec 32))
(declare-const x4_2 (_ BitVec 32))

;; precondition x4[0] == 0 || x4[0] == 1
(assert (or (= x4_0 #x00000000) (= x4_0 #x00000001)))

;; precondition x4[1] == 0 || x4[1] == 1
(assert (or (= x4_1 #x00000000) (= x4_1 #x00000001)))

;; precondition x4[2] == 0 || x4[2] == 1
(assert (or (= x4_2 #x00000000) (= x4_2 #x00000001)))

;; declare feature x5
(declare-const x5_0 (_ BitVec 32))
(declare-const x5_1 (_ BitVec 32))
(declare-const x5_2 (_ BitVec 32))

;; precondition x5[0] == 0 || x5[0] == 1
(assert (or (= x5_0 #x00000000) (= x5_0 #x00000001)))

;; precondition x5[1] == 0 || x5[1] == 1
(assert (or (= x5_1 #x00000000) (= x5_1 #x00000001)))

;; precondition x5[2] == 0 || x5[2] == 1
(assert (or (= x5_2 #x00000000) (= x5_2 #x00000001)))

;; declare feature x6
(declare-const x6_0 (_ BitVec 32))
(declare-const x6_1 (_ BitVec 32))
(declare-const x6_2 (_ BitVec 32))

;; precondition x6[0] == 0 || x6[0] == 1
(assert (or (= x6_0 #x00000000) (= x6_0 #x00000001)))

;; precondition x6[1] == 0 || x6[1] == 1
(assert (or (= x6_1 #x00000000) (= x6_1 #x00000001)))

;; precondition x6[2] == 0 || x6[2] == 1
(assert (or (= x6_2 #x00000000) (= x6_2 #x00000001)))

;; declare feature x7
(declare-const x7_0 (_ BitVec 32))
(declare-const x7_1 (_ BitVec 32))
(declare-const x7_2 (_ BitVec 32))

;; precondition x7[0] == 0 || x7[0] == 1
(assert (or (= x7_0 #x00000000) (= x7_0 #x00000001)))

;; precondition x7[1] == 0 || x7[1] == 1
(assert (or (= x7_1 #x00000000) (= x7_1 #x00000001)))

;; precondition x7[2] == 0 || x7[2] == 1
(assert (or (= x7_2 #x00000000) (= x7_2 #x00000001)))

;; declare feature x8
(declare-const x8_0 (_ BitVec 32))
(declare-const x8_1 (_ BitVec 32))
(declare-const x8_2 (_ BitVec 32))

;; precondition x8[0] == 0 || x8[0] == 1
(assert (or (= x8_0 #x00000000) (= x8_0 #x00000001)))

;; precondition x8[1] == 0 || x8[1] == 1
(assert (or (= x8_1 #x00000000) (= x8_1 #x00000001)))

;; precondition x8[2] == 0 || x8[2] == 1
(assert (or (= x8_2 #x00000000) (= x8_2 #x00000001)))

;; declare feature x9
(declare-const x9_0 (_ BitVec 32))
(declare-const x9_1 (_ BitVec 32))
(declare-const x9_2 (_ BitVec 32))

;; precondition x9[0] == 0 || x9[0] == 1
(assert (or (= x9_0 #x00000000) (= x9_0 #x00000001)))

;; precondition x9[1] == 0 || x9[1] == 1
(assert (or (= x9_1 #x00000000) (= x9_1 #x00000001)))

;; precondition x9[2] == 0 || x9[2] == 1
(assert (or (= x9_2 #x00000000) (= x9_2 #x00000001)))

;; declare feature x10
(declare-const x10_0 (_ BitVec 32))
(declare-const x10_1 (_ BitVec 32))
(declare-const x10_2 (_ BitVec 32))

;; precondition x10[0] == 0 || x10[0] == 1
(assert (or (= x10_0 #x00000000) (= x10_0 #x00000001)))

;; precondition x10[1] == 0 || x10[1] == 1
(assert (or (= x10_1 #x00000000) (= x10_1 #x00000001)))

;; precondition x10[2] == 0 || x10[2] == 1
(assert (or (= x10_2 #x00000000) (= x10_2 #x00000001)))

;; declare feature x11
(declare-const x11_0 (_ BitVec 32))
(declare-const x11_1 (_ BitVec 32))
(declare-const x11_2 (_ BitVec 32))

;; precondition x11[0] == 0 || x11[0] == 1
(assert (or (= x11_0 #x00000000) (= x11_0 #x00000001)))

;; precondition x11[1] == 0 || x11[1] == 1
(assert (or (= x11_1 #x00000000) (= x11_1 #x00000001)))

;; precondition x11[2] == 0 || x11[2] == 1
(assert (or (= x11_2 #x00000000) (= x11_2 #x00000001)))

;; declare feature x12
(declare-const x12_0 (_ BitVec 32))
(declare-const x12_1 (_ BitVec 32))
(declare-const x12_2 (_ BitVec 32))

;; precondition x12[0] == 0 || x12[0] == 1
(assert (or (= x12_0 #x00000000) (= x12_0 #x00000001)))

;; precondition x12[1] == 0 || x12[1] == 1
(assert (or (= x12_1 #x00000000) (= x12_1 #x00000001)))

;; precondition x12[2] == 0 || x12[2] == 1
(assert (or (= x12_2 #x00000000) (= x12_2 #x00000001)))

;; declare feature x13
(declare-const x13_0 (_ BitVec 32))
(declare-const x13_1 (_ BitVec 32))
(declare-const x13_2 (_ BitVec 32))

;; precondition x13[0] == 0 || x13[0] == 1
(assert (or (= x13_0 #x00000000) (= x13_0 #x00000001)))

;; precondition x13[1] == 0 || x13[1] == 1
(assert (or (= x13_1 #x00000000) (= x13_1 #x00000001)))

;; precondition x13[2] == 0 || x13[2] == 1
(assert (or (= x13_2 #x00000000) (= x13_2 #x00000001)))

;; declare feature x14
(declare-const x14_0 (_ BitVec 32))
(declare-const x14_1 (_ BitVec 32))
(declare-const x14_2 (_ BitVec 32))

;; precondition x14[0] == 0 || x14[0] == 1
(assert (or (= x14_0 #x00000000) (= x14_0 #x00000001)))

;; precondition x14[1] == 0 || x14[1] == 1
(assert (or (= x14_1 #x00000000) (= x14_1 #x00000001)))

;; precondition x14[2] == 0 || x14[2] == 1
(assert (or (= x14_2 #x00000000) (= x14_2 #x00000001)))

;; declare feature x15
(declare-const x15_0 (_ BitVec 32))
(declare-const x15_1 (_ BitVec 32))
(declare-const x15_2 (_ BitVec 32))

;; precondition x15[0] == 0 || x15[0] == 1
(assert (or (= x15_0 #x00000000) (= x15_0 #x00000001)))

;; precondition x15[1] == 0 || x15[1] == 1
(assert (or (= x15_1 #x00000000) (= x15_1 #x00000001)))

;; precondition x15[2] == 0 || x15[2] == 1
(assert (or (= x15_2 #x00000000) (= x15_2 #x00000001)))

;; declare feature x16
(declare-const x16_0 (_ BitVec 32))
(declare-const x16_1 (_ BitVec 32))
(declare-const x16_2 (_ BitVec 32))

;; precondition x16[0] == 0 || x16[0] == 1
(assert (or (= x16_0 #x00000000) (= x16_0 #x00000001)))

;; precondition x16[1] == 0 || x16[1] == 1
(assert (or (= x16_1 #x00000000) (= x16_1 #x00000001)))

;; precondition x16[2] == 0 || x16[2] == 1
(assert (or (= x16_2 #x00000000) (= x16_2 #x00000001)))

;; decline features for the local aggregation.
;; declare feature x17
(declare-const x17_0 (_ BitVec 32))
(declare-const x17_1 (_ BitVec 32))
(declare-const x17_2 (_ BitVec 32))

;; declare feature x18
(declare-const x18_0 (_ BitVec 32))
(declare-const x18_1 (_ BitVec 32))
(declare-const x18_2 (_ BitVec 32))

;; declare feature x19
(declare-const x19_0 (_ BitVec 32))
(declare-const x19_1 (_ BitVec 32))
(declare-const x19_2 (_ BitVec 32))

;; declare feature x20
(declare-const x20_0 (_ BitVec 32))
(declare-const x20_1 (_ BitVec 32))
(declare-const x20_2 (_ BitVec 32))

;; declare feature x21
(declare-const x21_0 (_ BitVec 32))
(declare-const x21_1 (_ BitVec 32))
(declare-const x21_2 (_ BitVec 32))

;; declare feature x22
(declare-const x22_0 (_ BitVec 32))
(declare-const x22_1 (_ BitVec 32))
(declare-const x22_2 (_ BitVec 32))

;; declare feature x23
(declare-const x23_0 (_ BitVec 32))
(declare-const x23_1 (_ BitVec 32))
(declare-const x23_2 (_ BitVec 32))

;; declare feature x24
(declare-const x24_0 (_ BitVec 32))
(declare-const x24_1 (_ BitVec 32))
(declare-const x24_2 (_ BitVec 32))

;; declare feature x25
(declare-const x25_0 (_ BitVec 32))
(declare-const x25_1 (_ BitVec 32))
(declare-const x25_2 (_ BitVec 32))

;; declare feature x26
(declare-const x26_0 (_ BitVec 32))
(declare-const x26_1 (_ BitVec 32))
(declare-const x26_2 (_ BitVec 32))

;; declare feature x27
(declare-const x27_0 (_ BitVec 32))
(declare-const x27_1 (_ BitVec 32))
(declare-const x27_2 (_ BitVec 32))

;; declare feature x28
(declare-const x28_0 (_ BitVec 32))
(declare-const x28_1 (_ BitVec 32))
(declare-const x28_2 (_ BitVec 32))

;; declare feature x29
(declare-const x29_0 (_ BitVec 32))
(declare-const x29_1 (_ BitVec 32))
(declare-const x29_2 (_ BitVec 32))

;; declare feature x30
(declare-const x30_0 (_ BitVec 32))
(declare-const x30_1 (_ BitVec 32))
(declare-const x30_2 (_ BitVec 32))

;; declare feature x31
(declare-const x31_0 (_ BitVec 32))
(declare-const x31_1 (_ BitVec 32))
(declare-const x31_2 (_ BitVec 32))

;; declare feature x32
(declare-const x32_0 (_ BitVec 32))
(declare-const x32_1 (_ BitVec 32))
(declare-const x32_2 (_ BitVec 32))

;; decline features for the global aggregation.
;; declare feature x33
(declare-const x33_0 (_ BitVec 32))
(declare-const x33_1 (_ BitVec 32))
(declare-const x33_2 (_ BitVec 32))

;; declare feature x34
(declare-const x34_0 (_ BitVec 32))
(declare-const x34_1 (_ BitVec 32))
(declare-const x34_2 (_ BitVec 32))

;; declare feature x35
(declare-const x35_0 (_ BitVec 32))
(declare-const x35_1 (_ BitVec 32))
(declare-const x35_2 (_ BitVec 32))

;; declare feature x36
(declare-const x36_0 (_ BitVec 32))
(declare-const x36_1 (_ BitVec 32))
(declare-const x36_2 (_ BitVec 32))

;; declare feature x37
(declare-const x37_0 (_ BitVec 32))
(declare-const x37_1 (_ BitVec 32))
(declare-const x37_2 (_ BitVec 32))

;; declare feature x38
(declare-const x38_0 (_ BitVec 32))
(declare-const x38_1 (_ BitVec 32))
(declare-const x38_2 (_ BitVec 32))

;; declare feature x39
(declare-const x39_0 (_ BitVec 32))
(declare-const x39_1 (_ BitVec 32))
(declare-const x39_2 (_ BitVec 32))

;; declare feature x40
(declare-const x40_0 (_ BitVec 32))
(declare-const x40_1 (_ BitVec 32))
(declare-const x40_2 (_ BitVec 32))

;; declare feature x41
(declare-const x41_0 (_ BitVec 32))
(declare-const x41_1 (_ BitVec 32))
(declare-const x41_2 (_ BitVec 32))

;; declare feature x42
(declare-const x42_0 (_ BitVec 32))
(declare-const x42_1 (_ BitVec 32))
(declare-const x42_2 (_ BitVec 32))

;; declare feature x43
(declare-const x43_0 (_ BitVec 32))
(declare-const x43_1 (_ BitVec 32))
(declare-const x43_2 (_ BitVec 32))

;; declare feature x44
(declare-const x44_0 (_ BitVec 32))
(declare-const x44_1 (_ BitVec 32))
(declare-const x44_2 (_ BitVec 32))

;; declare feature x45
(declare-const x45_0 (_ BitVec 32))
(declare-const x45_1 (_ BitVec 32))
(declare-const x45_2 (_ BitVec 32))

;; declare feature x46
(declare-const x46_0 (_ BitVec 32))
(declare-const x46_1 (_ BitVec 32))
(declare-const x46_2 (_ BitVec 32))

;; declare feature x47
(declare-const x47_0 (_ BitVec 32))
(declare-const x47_1 (_ BitVec 32))
(declare-const x47_2 (_ BitVec 32))

;; declare feature x48
(declare-const x48_0 (_ BitVec 32))
(declare-const x48_1 (_ BitVec 32))
(declare-const x48_2 (_ BitVec 32))

;; Compute agg(x17,x1)
(assert (= x17_0
          (saturating-add 
             (ite e0_0 x1_0 #x00000000)
             (ite e0_1 x1_1 #x00000000)
             (ite e0_2 x1_2 #x00000000)
          )))
(assert (= x17_1
          (saturating-add 
             (ite e1_0 x1_0 #x00000000)
             (ite e1_1 x1_1 #x00000000)
             (ite e1_2 x1_2 #x00000000)
          )))
(assert (= x17_2
          (saturating-add 
             (ite e2_0 x1_0 #x00000000)
             (ite e2_1 x1_1 #x00000000)
             (ite e2_2 x1_2 #x00000000)
          )))
;; end agg(x17,x1)

;; Compute agg(x18,x2)
(assert (= x18_0
          (saturating-add 
             (ite e0_0 x2_0 #x00000000)
             (ite e0_1 x2_1 #x00000000)
             (ite e0_2 x2_2 #x00000000)
          )))
(assert (= x18_1
          (saturating-add 
             (ite e1_0 x2_0 #x00000000)
             (ite e1_1 x2_1 #x00000000)
             (ite e1_2 x2_2 #x00000000)
          )))
(assert (= x18_2
          (saturating-add 
             (ite e2_0 x2_0 #x00000000)
             (ite e2_1 x2_1 #x00000000)
             (ite e2_2 x2_2 #x00000000)
          )))
;; end agg(x18,x2)

;; Compute agg(x19,x3)
(assert (= x19_0
          (saturating-add 
             (ite e0_0 x3_0 #x00000000)
             (ite e0_1 x3_1 #x00000000)
             (ite e0_2 x3_2 #x00000000)
          )))
(assert (= x19_1
          (saturating-add 
             (ite e1_0 x3_0 #x00000000)
             (ite e1_1 x3_1 #x00000000)
             (ite e1_2 x3_2 #x00000000)
          )))
(assert (= x19_2
          (saturating-add 
             (ite e2_0 x3_0 #x00000000)
             (ite e2_1 x3_1 #x00000000)
             (ite e2_2 x3_2 #x00000000)
          )))
;; end agg(x19,x3)

;; Compute agg(x20,x4)
(assert (= x20_0
          (saturating-add 
             (ite e0_0 x4_0 #x00000000)
             (ite e0_1 x4_1 #x00000000)
             (ite e0_2 x4_2 #x00000000)
          )))
(assert (= x20_1
          (saturating-add 
             (ite e1_0 x4_0 #x00000000)
             (ite e1_1 x4_1 #x00000000)
             (ite e1_2 x4_2 #x00000000)
          )))
(assert (= x20_2
          (saturating-add 
             (ite e2_0 x4_0 #x00000000)
             (ite e2_1 x4_1 #x00000000)
             (ite e2_2 x4_2 #x00000000)
          )))
;; end agg(x20,x4)

;; Compute agg(x21,x5)
(assert (= x21_0
          (saturating-add 
             (ite e0_0 x5_0 #x00000000)
             (ite e0_1 x5_1 #x00000000)
             (ite e0_2 x5_2 #x00000000)
          )))
(assert (= x21_1
          (saturating-add 
             (ite e1_0 x5_0 #x00000000)
             (ite e1_1 x5_1 #x00000000)
             (ite e1_2 x5_2 #x00000000)
          )))
(assert (= x21_2
          (saturating-add 
             (ite e2_0 x5_0 #x00000000)
             (ite e2_1 x5_1 #x00000000)
             (ite e2_2 x5_2 #x00000000)
          )))
;; end agg(x21,x5)

;; Compute agg(x22,x6)
(assert (= x22_0
          (saturating-add 
             (ite e0_0 x6_0 #x00000000)
             (ite e0_1 x6_1 #x00000000)
             (ite e0_2 x6_2 #x00000000)
          )))
(assert (= x22_1
          (saturating-add 
             (ite e1_0 x6_0 #x00000000)
             (ite e1_1 x6_1 #x00000000)
             (ite e1_2 x6_2 #x00000000)
          )))
(assert (= x22_2
          (saturating-add 
             (ite e2_0 x6_0 #x00000000)
             (ite e2_1 x6_1 #x00000000)
             (ite e2_2 x6_2 #x00000000)
          )))
;; end agg(x22,x6)

;; Compute agg(x23,x7)
(assert (= x23_0
          (saturating-add 
             (ite e0_0 x7_0 #x00000000)
             (ite e0_1 x7_1 #x00000000)
             (ite e0_2 x7_2 #x00000000)
          )))
(assert (= x23_1
          (saturating-add 
             (ite e1_0 x7_0 #x00000000)
             (ite e1_1 x7_1 #x00000000)
             (ite e1_2 x7_2 #x00000000)
          )))
(assert (= x23_2
          (saturating-add 
             (ite e2_0 x7_0 #x00000000)
             (ite e2_1 x7_1 #x00000000)
             (ite e2_2 x7_2 #x00000000)
          )))
;; end agg(x23,x7)

;; Compute agg(x24,x8)
(assert (= x24_0
          (saturating-add 
             (ite e0_0 x8_0 #x00000000)
             (ite e0_1 x8_1 #x00000000)
             (ite e0_2 x8_2 #x00000000)
          )))
(assert (= x24_1
          (saturating-add 
             (ite e1_0 x8_0 #x00000000)
             (ite e1_1 x8_1 #x00000000)
             (ite e1_2 x8_2 #x00000000)
          )))
(assert (= x24_2
          (saturating-add 
             (ite e2_0 x8_0 #x00000000)
             (ite e2_1 x8_1 #x00000000)
             (ite e2_2 x8_2 #x00000000)
          )))
;; end agg(x24,x8)

;; Compute agg(x25,x9)
(assert (= x25_0
          (saturating-add 
             (ite e0_0 x9_0 #x00000000)
             (ite e0_1 x9_1 #x00000000)
             (ite e0_2 x9_2 #x00000000)
          )))
(assert (= x25_1
          (saturating-add 
             (ite e1_0 x9_0 #x00000000)
             (ite e1_1 x9_1 #x00000000)
             (ite e1_2 x9_2 #x00000000)
          )))
(assert (= x25_2
          (saturating-add 
             (ite e2_0 x9_0 #x00000000)
             (ite e2_1 x9_1 #x00000000)
             (ite e2_2 x9_2 #x00000000)
          )))
;; end agg(x25,x9)

;; Compute agg(x26,x10)
(assert (= x26_0
          (saturating-add 
             (ite e0_0 x10_0 #x00000000)
             (ite e0_1 x10_1 #x00000000)
             (ite e0_2 x10_2 #x00000000)
          )))
(assert (= x26_1
          (saturating-add 
             (ite e1_0 x10_0 #x00000000)
             (ite e1_1 x10_1 #x00000000)
             (ite e1_2 x10_2 #x00000000)
          )))
(assert (= x26_2
          (saturating-add 
             (ite e2_0 x10_0 #x00000000)
             (ite e2_1 x10_1 #x00000000)
             (ite e2_2 x10_2 #x00000000)
          )))
;; end agg(x26,x10)

;; Compute agg(x27,x11)
(assert (= x27_0
          (saturating-add 
             (ite e0_0 x11_0 #x00000000)
             (ite e0_1 x11_1 #x00000000)
             (ite e0_2 x11_2 #x00000000)
          )))
(assert (= x27_1
          (saturating-add 
             (ite e1_0 x11_0 #x00000000)
             (ite e1_1 x11_1 #x00000000)
             (ite e1_2 x11_2 #x00000000)
          )))
(assert (= x27_2
          (saturating-add 
             (ite e2_0 x11_0 #x00000000)
             (ite e2_1 x11_1 #x00000000)
             (ite e2_2 x11_2 #x00000000)
          )))
;; end agg(x27,x11)

;; Compute agg(x28,x12)
(assert (= x28_0
          (saturating-add 
             (ite e0_0 x12_0 #x00000000)
             (ite e0_1 x12_1 #x00000000)
             (ite e0_2 x12_2 #x00000000)
          )))
(assert (= x28_1
          (saturating-add 
             (ite e1_0 x12_0 #x00000000)
             (ite e1_1 x12_1 #x00000000)
             (ite e1_2 x12_2 #x00000000)
          )))
(assert (= x28_2
          (saturating-add 
             (ite e2_0 x12_0 #x00000000)
             (ite e2_1 x12_1 #x00000000)
             (ite e2_2 x12_2 #x00000000)
          )))
;; end agg(x28,x12)

;; Compute agg(x29,x13)
(assert (= x29_0
          (saturating-add 
             (ite e0_0 x13_0 #x00000000)
             (ite e0_1 x13_1 #x00000000)
             (ite e0_2 x13_2 #x00000000)
          )))
(assert (= x29_1
          (saturating-add 
             (ite e1_0 x13_0 #x00000000)
             (ite e1_1 x13_1 #x00000000)
             (ite e1_2 x13_2 #x00000000)
          )))
(assert (= x29_2
          (saturating-add 
             (ite e2_0 x13_0 #x00000000)
             (ite e2_1 x13_1 #x00000000)
             (ite e2_2 x13_2 #x00000000)
          )))
;; end agg(x29,x13)

;; Compute agg(x30,x14)
(assert (= x30_0
          (saturating-add 
             (ite e0_0 x14_0 #x00000000)
             (ite e0_1 x14_1 #x00000000)
             (ite e0_2 x14_2 #x00000000)
          )))
(assert (= x30_1
          (saturating-add 
             (ite e1_0 x14_0 #x00000000)
             (ite e1_1 x14_1 #x00000000)
             (ite e1_2 x14_2 #x00000000)
          )))
(assert (= x30_2
          (saturating-add 
             (ite e2_0 x14_0 #x00000000)
             (ite e2_1 x14_1 #x00000000)
             (ite e2_2 x14_2 #x00000000)
          )))
;; end agg(x30,x14)

;; Compute agg(x31,x15)
(assert (= x31_0
          (saturating-add 
             (ite e0_0 x15_0 #x00000000)
             (ite e0_1 x15_1 #x00000000)
             (ite e0_2 x15_2 #x00000000)
          )))
(assert (= x31_1
          (saturating-add 
             (ite e1_0 x15_0 #x00000000)
             (ite e1_1 x15_1 #x00000000)
             (ite e1_2 x15_2 #x00000000)
          )))
(assert (= x31_2
          (saturating-add 
             (ite e2_0 x15_0 #x00000000)
             (ite e2_1 x15_1 #x00000000)
             (ite e2_2 x15_2 #x00000000)
          )))
;; end agg(x31,x15)

;; Compute agg(x32,x16)
(assert (= x32_0
          (saturating-add 
             (ite e0_0 x16_0 #x00000000)
             (ite e0_1 x16_1 #x00000000)
             (ite e0_2 x16_2 #x00000000)
          )))
(assert (= x32_1
          (saturating-add 
             (ite e1_0 x16_0 #x00000000)
             (ite e1_1 x16_1 #x00000000)
             (ite e1_2 x16_2 #x00000000)
          )))
(assert (= x32_2
          (saturating-add 
             (ite e2_0 x16_0 #x00000000)
             (ite e2_1 x16_1 #x00000000)
             (ite e2_2 x16_2 #x00000000)
          )))
;; end agg(x32,x16)

;; compute aggG(x33,x1)
(assert (= x33_0
         (saturating-add x1_0 x1_1 x1_2) ))
(assert (= x33_1
         (saturating-add x1_0 x1_1 x1_2) ))
(assert (= x33_2
         (saturating-add x1_0 x1_1 x1_2) ))
;; end aggG(x33,x1)

;; compute aggG(x34,x2)
(assert (= x34_0
         (saturating-add x2_0 x2_1 x2_2) ))
(assert (= x34_1
         (saturating-add x2_0 x2_1 x2_2) ))
(assert (= x34_2
         (saturating-add x2_0 x2_1 x2_2) ))
;; end aggG(x34,x2)

;; compute aggG(x35,x3)
(assert (= x35_0
         (saturating-add x3_0 x3_1 x3_2) ))
(assert (= x35_1
         (saturating-add x3_0 x3_1 x3_2) ))
(assert (= x35_2
         (saturating-add x3_0 x3_1 x3_2) ))
;; end aggG(x35,x3)

;; compute aggG(x36,x4)
(assert (= x36_0
         (saturating-add x4_0 x4_1 x4_2) ))
(assert (= x36_1
         (saturating-add x4_0 x4_1 x4_2) ))
(assert (= x36_2
         (saturating-add x4_0 x4_1 x4_2) ))
;; end aggG(x36,x4)

;; compute aggG(x37,x5)
(assert (= x37_0
         (saturating-add x5_0 x5_1 x5_2) ))
(assert (= x37_1
         (saturating-add x5_0 x5_1 x5_2) ))
(assert (= x37_2
         (saturating-add x5_0 x5_1 x5_2) ))
;; end aggG(x37,x5)

;; compute aggG(x38,x6)
(assert (= x38_0
         (saturating-add x6_0 x6_1 x6_2) ))
(assert (= x38_1
         (saturating-add x6_0 x6_1 x6_2) ))
(assert (= x38_2
         (saturating-add x6_0 x6_1 x6_2) ))
;; end aggG(x38,x6)

;; compute aggG(x39,x7)
(assert (= x39_0
         (saturating-add x7_0 x7_1 x7_2) ))
(assert (= x39_1
         (saturating-add x7_0 x7_1 x7_2) ))
(assert (= x39_2
         (saturating-add x7_0 x7_1 x7_2) ))
;; end aggG(x39,x7)

;; compute aggG(x40,x8)
(assert (= x40_0
         (saturating-add x8_0 x8_1 x8_2) ))
(assert (= x40_1
         (saturating-add x8_0 x8_1 x8_2) ))
(assert (= x40_2
         (saturating-add x8_0 x8_1 x8_2) ))
;; end aggG(x40,x8)

;; compute aggG(x41,x9)
(assert (= x41_0
         (saturating-add x9_0 x9_1 x9_2) ))
(assert (= x41_1
         (saturating-add x9_0 x9_1 x9_2) ))
(assert (= x41_2
         (saturating-add x9_0 x9_1 x9_2) ))
;; end aggG(x41,x9)

;; compute aggG(x42,x10)
(assert (= x42_0
         (saturating-add x10_0 x10_1 x10_2) ))
(assert (= x42_1
         (saturating-add x10_0 x10_1 x10_2) ))
(assert (= x42_2
         (saturating-add x10_0 x10_1 x10_2) ))
;; end aggG(x42,x10)

;; compute aggG(x43,x11)
(assert (= x43_0
         (saturating-add x11_0 x11_1 x11_2) ))
(assert (= x43_1
         (saturating-add x11_0 x11_1 x11_2) ))
(assert (= x43_2
         (saturating-add x11_0 x11_1 x11_2) ))
;; end aggG(x43,x11)

;; compute aggG(x44,x12)
(assert (= x44_0
         (saturating-add x12_0 x12_1 x12_2) ))
(assert (= x44_1
         (saturating-add x12_0 x12_1 x12_2) ))
(assert (= x44_2
         (saturating-add x12_0 x12_1 x12_2) ))
;; end aggG(x44,x12)

;; compute aggG(x45,x13)
(assert (= x45_0
         (saturating-add x13_0 x13_1 x13_2) ))
(assert (= x45_1
         (saturating-add x13_0 x13_1 x13_2) ))
(assert (= x45_2
         (saturating-add x13_0 x13_1 x13_2) ))
;; end aggG(x45,x13)

;; compute aggG(x46,x14)
(assert (= x46_0
         (saturating-add x14_0 x14_1 x14_2) ))
(assert (= x46_1
         (saturating-add x14_0 x14_1 x14_2) ))
(assert (= x46_2
         (saturating-add x14_0 x14_1 x14_2) ))
;; end aggG(x46,x14)

;; compute aggG(x47,x15)
(assert (= x47_0
         (saturating-add x15_0 x15_1 x15_2) ))
(assert (= x47_1
         (saturating-add x15_0 x15_1 x15_2) ))
(assert (= x47_2
         (saturating-add x15_0 x15_1 x15_2) ))
;; end aggG(x47,x15)

;; compute aggG(x48,x16)
(assert (= x48_0
         (saturating-add x16_0 x16_1 x16_2) ))
(assert (= x48_1
         (saturating-add x16_0 x16_1 x16_2) ))
(assert (= x48_2
         (saturating-add x16_0 x16_1 x16_2) ))
;; end aggG(x48,x16)

;; Calcolate (MpreviousFeatures(previousFeatures) + Magg(aggPreviousFeatures) + MaggG(aggGPreviousFeatures) + b)
;; declare feature x49
(declare-const x49_0 (_ BitVec 32))
(declare-const x49_1 (_ BitVec 32))
(declare-const x49_2 (_ BitVec 32))

;; declare feature x50
(declare-const x50_0 (_ BitVec 32))
(declare-const x50_1 (_ BitVec 32))
(declare-const x50_2 (_ BitVec 32))

;; declare feature x51
(declare-const x51_0 (_ BitVec 32))
(declare-const x51_1 (_ BitVec 32))
(declare-const x51_2 (_ BitVec 32))

;; declare feature x52
(declare-const x52_0 (_ BitVec 32))
(declare-const x52_1 (_ BitVec 32))
(declare-const x52_2 (_ BitVec 32))

;; declare feature x53
(declare-const x53_0 (_ BitVec 32))
(declare-const x53_1 (_ BitVec 32))
(declare-const x53_2 (_ BitVec 32))

;; declare feature x54
(declare-const x54_0 (_ BitVec 32))
(declare-const x54_1 (_ BitVec 32))
(declare-const x54_2 (_ BitVec 32))

;; declare feature x55
(declare-const x55_0 (_ BitVec 32))
(declare-const x55_1 (_ BitVec 32))
(declare-const x55_2 (_ BitVec 32))

;; declare feature x56
(declare-const x56_0 (_ BitVec 32))
(declare-const x56_1 (_ BitVec 32))
(declare-const x56_2 (_ BitVec 32))

;; declare feature x57
(declare-const x57_0 (_ BitVec 32))
(declare-const x57_1 (_ BitVec 32))
(declare-const x57_2 (_ BitVec 32))

;; declare feature x58
(declare-const x58_0 (_ BitVec 32))
(declare-const x58_1 (_ BitVec 32))
(declare-const x58_2 (_ BitVec 32))

;; declare feature x59
(declare-const x59_0 (_ BitVec 32))
(declare-const x59_1 (_ BitVec 32))
(declare-const x59_2 (_ BitVec 32))

;; declare feature x60
(declare-const x60_0 (_ BitVec 32))
(declare-const x60_1 (_ BitVec 32))
(declare-const x60_2 (_ BitVec 32))

;; declare feature x61
(declare-const x61_0 (_ BitVec 32))
(declare-const x61_1 (_ BitVec 32))
(declare-const x61_2 (_ BitVec 32))

;; declare feature x62
(declare-const x62_0 (_ BitVec 32))
(declare-const x62_1 (_ BitVec 32))
(declare-const x62_2 (_ BitVec 32))

;; declare feature x63
(declare-const x63_0 (_ BitVec 32))
(declare-const x63_1 (_ BitVec 32))
(declare-const x63_2 (_ BitVec 32))

;; declare feature x64
(declare-const x64_0 (_ BitVec 32))
(declare-const x64_1 (_ BitVec 32))
(declare-const x64_2 (_ BitVec 32))

;; linear layer output x49 from previous, agg, aggG (column 0)
(assert (= x49_0
