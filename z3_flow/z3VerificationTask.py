""" This program creates verification tasks for GNNs. It has flow

Python programm -[generate]-> Z3 programm -[parse]-> Z3 solver -[obtain]-> Results SAT or non SAT.

Returns:
    _type_: _description_
"""

import subprocess
import sys
from pathlib import Path as PathlibPath
sys.path.insert(0, str(PathlibPath(__file__).parent.parent))

# Add parent directory to path to import validity
from z3_flow.support_funcitons import *
from validity import checking_input_matrices


Number = int | float

class Z3VerificationTask:
    index_of_feature=0

    def __init__(self,Nbound=2, filename="main.smt",bitvect= 8,activation='ReLU'):
        self.Nbound = Nbound
        self.filename = filename
        self.start_of_program = "w"
        self.bitvect = bitvect
        self.features =[]
        self.activation =activation
        self.write_saturation_helpers()
        self.adj_matrix()
        
    def _addLineInMain(self,line):
        with open(self.filename, self.start_of_program) as smt_file:
            smt_file.write(f"{line}\n")
        self.start_of_program ="a"
    
    def write_saturation_helpers(self):
        n = self.bitvect
        max_int = (1 << (n - 1)) - 1
        min_int = -(1 << (n - 1))

        max_n = int_to_bv_hex(max_int, n)   # n-bit
        min_n = int_to_bv_hex(min_int, n)   # n-bit (two's complement)

        # 2n-bit versions (sign-extended constants)
        # easiest: just sign-extend the n-bit literal inside SMT
        self._addLineInMain(f";; Saturating arithmetic helpers for signed (_ BitVec {n})")
        self._addLineInMain(f";; Saturating for addition")
        self._addLineInMain(f"(define-fun saturating-add ((x (_ BitVec {n})) (y (_ BitVec {n}))) (_ BitVec {n})")
        self._addLineInMain(f"  (let ((sx ((_ sign_extend {n}) x))")
        self._addLineInMain(f"        (sy ((_ sign_extend {n}) y))")
        self._addLineInMain(f"        (max ((_ sign_extend {n}) {max_n}))")
        self._addLineInMain(f"        (min ((_ sign_extend {n}) {min_n})))")
        self._addLineInMain(f"    (let ((s (bvadd sx sy)))")
        self._addLineInMain(f"      (let ((clamped (ite (bvslt s min) min (ite (bvsgt s max) max s))))")
        self._addLineInMain(f"        ((_ extract {n-1} 0) clamped)))))")
        self._addLineInMain("")
        self._addLineInMain(f";; Saturating for multiplication")
        self._addLineInMain(f"(define-fun saturating-mul ((x (_ BitVec {n})) (y (_ BitVec {n}))) (_ BitVec {n})")
        self._addLineInMain(f"  (let ((sx ((_ sign_extend {n}) x))")
        self._addLineInMain(f"        (sy ((_ sign_extend {n}) y))")
        self._addLineInMain(f"        (max ((_ sign_extend {n}) {max_n}))")
        self._addLineInMain(f"        (min ((_ sign_extend {n}) {min_n})))")
        self._addLineInMain(f"    (let ((p (bvmul sx sy)))")
        self._addLineInMain(f"      (let ((clamped (ite (bvslt p min) min (ite (bvsgt p max) max p))))")
        self._addLineInMain(f"        ((_ extract {n-1} 0) clamped)))))")
        self._addLineInMain("")


    def adj_matrix(self):  
        self._addLineInMain(f";; adjacency matrix of unknown graph")        
        for i in range(self.Nbound):
            for j in range(self.Nbound):
                self._addLineInMain(f"(declare-const e{i}_{j} Bool)")
        self._addLineInMain(f"")

    def _get_new_featurename(self):
        self.index_of_feature = self.index_of_feature + 1
        featureName = f"x{self.index_of_feature}"
        self.features.append(featureName)
        return featureName
    
    def add_input_feature(self):
        x_feature=self._get_new_featurename()
        self._addLineInMain(f";; declare feature {x_feature}") 
        for j in range(self.Nbound):
            self._addLineInMain(f"(declare-const {x_feature}_{j} (_ BitVec {self.bitvect}))")
        self._addLineInMain(f"")
        return x_feature

    def _add_feature(self):
        x_feature=self._get_new_featurename()
        self._addLineInMain(f";; declare feature {x_feature}") 
        for j in range(self.Nbound):
            self._addLineInMain(f"(declare-const {x_feature}_{j} (_ BitVec {self.bitvect}))")
        self._addLineInMain(f"")
        return x_feature
    
    def add_precondition(self, cond: str):
        self._addLineInMain(f";; precondition {cond}") 
        smt_line = convert_condition_to_smt(cond,self.features,"precondition", self.bitvect)
        self._addLineInMain(f"{smt_line}")
        self._addLineInMain(f"")

    def apply_activation(self,input_feature):
        self._addLineInMain(f";; declare feature to store the results after applying AF")
        feature_of_activationFunction=self._add_feature()
        self._addLineInMain(f";; calculate {feature_of_activationFunction}= {self.activation}({input_feature})")
        if self.activation == "ReLU":
            zero_hex = int_to_bv_hex(0, self.bitvect)
            for i in range(self.Nbound):
                self._addLineInMain(f"(assert (= {feature_of_activationFunction}_{i}")
                self._addLineInMain(f"        (ite (bvsge {input_feature}_{i} {zero_hex})   ;; if x_number_index >= 0 (signed)")
                self._addLineInMain(f"             {input_feature}_{i}                ;; keep ")
                self._addLineInMain(f"             {zero_hex})))            ;; else return 0")
        elif self.activation.startswith("ReLU"):
            
            param_str = self.activation[4:]  # after 'ReLU'
            if not param_str.isdigit():
                raise ValueError(f"Unsupported ReLU variant: {self.activation}")
            if param_str.isdigit():
                param = int(param_str)
                zero_hex = int_to_bv_hex(0, self.bitvect)
                cap_hex  = int_to_bv_hex(param, self.bitvect)

                for i in range(self.Nbound):
                    self._addLineInMain(f"(assert (= {feature_of_activationFunction}_{i}")
                    self._addLineInMain(f"        (ite (bvslt {input_feature}_{i} {zero_hex})   ;; if x < 0")
                    self._addLineInMain(f"             {zero_hex}                              ;; then 0")
                    self._addLineInMain(f"             (ite (bvsle {input_feature}_{i} {cap_hex})  ;; else if x <= cap")
                    self._addLineInMain(f"                  {input_feature}_{i}                 ;;      keep x")
                    self._addLineInMain(f"                  {cap_hex}))))                         ;;  else cap")
        elif self.activation == "trReLU":
            # trReLU: f(x) = min(max(0, x), 1)
            zero_hex = int_to_bv_hex(0, self.bitvect)
            one_hex  = int_to_bv_hex(1, self.bitvect)

            for i in range(self.Nbound):
                self._addLineInMain(f"(assert (= {feature_of_activationFunction}_{i}")
                self._addLineInMain(f"        (ite (bvslt {input_feature}_{i} {zero_hex})         ;; if x < 0")
                self._addLineInMain(f"             {zero_hex}                                    ;;   -> 0")
                self._addLineInMain(f"             (ite (bvsle {input_feature}_{i} {one_hex})     ;; else if x <= 1")
                self._addLineInMain(f"                  {input_feature}_{i}                       ;;        -> x")
                self._addLineInMain(f"                  {one_hex}))))                         ;; else -> 1")

        else:
            raise ValueError(
                "Activation function wrong or unsupported. "
                "Supported: ReLU, ReLU{p} (e.g. ReLU6), trReLU"
            )

    def add_layer(self,C: list[list[Number]],
                  A: list[list[Number]], 
                  R: list[list[Number]],
                  b: list[list[Number]]):
        input_dimension = len(C[0])
        output_dimension = len(C)
        # validity
        if checking_input_matrices(input_dimension, C, A, R, b) != 'fine':
            raise ValueError("Something wrong. Check your input.")
        
        

        previousFeatures = self.features[-input_dimension:]
        self._addLineInMain(f";; decline features for the local aggregation.")
        aggPreviousFeatures = [self._add_feature() for j in range(input_dimension)]
        self._addLineInMain(f";; decline features for the global aggregation.")
        aggGPreviousFeatures = [self._add_feature() for j in range(input_dimension)]
        
        #block of local aggregation
        zero = int_to_bv_hex(0, self.bitvect)
        for agg in range(len(aggPreviousFeatures)):
            self._addLineInMain(f";; Compute agg({aggPreviousFeatures[agg]},{previousFeatures[agg]})")
            for v in range(self.Nbound):
                self._addLineInMain(f"(assert (= {aggPreviousFeatures[agg]}_{v}")
                self._addLineInMain(f"          (saturating-add ")
                for j in range (self.Nbound):
                    self._addLineInMain(f"             (ite e{v}_{j} {previousFeatures[agg]}_{j} {zero})")
                self._addLineInMain(f"          )))") 
            self._addLineInMain(f";; end agg({aggPreviousFeatures[agg]},{previousFeatures[agg]})")
            self._addLineInMain(f"")
            
        #block of global aggregation
        for agg in range(len(aggGPreviousFeatures)):
            self._addLineInMain(f";; compute aggG({aggGPreviousFeatures[agg] },{previousFeatures[agg]})")
            args = " ".join(f"{previousFeatures[agg]}_{j}" for j in range(self.Nbound))
            agg_term = f"(saturating-add {args})"

            for v in range(self.Nbound):
                self._addLineInMain(f"(assert (= {aggGPreviousFeatures[agg]}_{v}")
                self._addLineInMain(f"         {agg_term} ))")

            self._addLineInMain(f";; end aggG({aggGPreviousFeatures[agg]},{previousFeatures[agg]})")
            self._addLineInMain("")
        
        #block of the matrix multiplication
        self._addLineInMain(f";; Calcolate (A(previousFeatures) + Magg(aggPreviousFeatures) + MaggG(aggGPreviousFeatures) + b)")
        """
        Encodes, for each position i = 0..Nbound-1 and each output o:

            u_o(i) = sum_j C[o][j] * x_j(i)
                + sum_j A[o][j] * y_j(i)
                + sum_j R[o][j] * z_j(i)
                + b[o][0]

        where:
        - previousFeatures[j]      = base name of x_j (e.g., "x1")
        - aggPreviousFeatures[j]   = base name of y_j
        - aggGPreviousFeatures[j]  = base name of z_j
        - outputFeatures[o]        = base name of u_o (e.g., "x5", "x6")
        - C, A, R have shape [k][input_dimension]
        - b has shape [k][1]
        """
        
        # create k new output feature vectors (one per row of C/A/R/b)
        outputFeatures = [self._add_feature() for _ in range(output_dimension)]
        
        for o in range(output_dimension):         # for each output row (0..k-1)
            out_base = outputFeatures[o]         # base name of output feature vector
            self._addLineInMain(f";; linear layer output {out_base} from previous, agg, aggG (row {o})")

            for i in range(self.Nbound):          # for each position i
                out_var = f"{out_base}_{i}"

                self._addLineInMain(f"(assert (= {out_var}")
                

                # C * x(i)
                for j in range(input_dimension):
                    coef_hex = int_to_bv_hex(C[o][j], self.bitvect)
                    self._addLineInMain(f"         (saturating-add")
                    self._addLineInMain(
                        f"           (saturating-mul {previousFeatures[j]}_{i} {coef_hex})"
                    )

                # A * y(i)
                for j in range(input_dimension):
                    coef_hex = int_to_bv_hex(A[o][j], self.bitvect)
                    self._addLineInMain(f"         (saturating-add")
                    self._addLineInMain(
                        f"           (saturating-mul {aggPreviousFeatures[j]}_{i} {coef_hex})"
                    )

                # R * z(i)
                for j in range(input_dimension):
                    coef_hex = int_to_bv_hex(R[o][j], self.bitvect)
                    self._addLineInMain(f"         (saturating-add")
                    self._addLineInMain(
                        f"           (saturating-mul {aggGPreviousFeatures[j]}_{i} {coef_hex})"
                    )

                # bias term b[o][0]
                bias_hex = int_to_bv_hex(b[o][0], self.bitvect)
                self._addLineInMain(f"           {bias_hex}")

                self._addLineInMain(f"  " + ")"*(2 + 3*input_dimension))  # close all parentheses

            self._addLineInMain(f";; end linear layer for {out_base}")
            self._addLineInMain("")
        #apply activation function
        for out_base in outputFeatures:
            self.apply_activation(out_base)
        self._addLineInMain(f";; end")
        self._addLineInMain("")

    def get_last_feature(self):
        return (self.features[-1]) 
    
    def add_postcondition(self, cond: str): #add checker if there is this feature
        self._addLineInMain(f";; postcondition {cond}") 
        smt_line = convert_condition_to_smt(cond,self.features,"postcondition", self.bitvect)
        self._addLineInMain(f"{smt_line}")
        self._addLineInMain(f"")
    
    def check(self):
        """
        Run Z3 on the generated SMT file, ask for intermediate values
        of all feature and activation variables after (check-sat).

        Returns:
            status: 'sat', 'unsat', or 'unknown'
            values: dict { "x1_0": int, "x1_1": int, "a1_0": int, ... } if sat,
                    empty dict otherwise.
        """
        # Build the list of variables we want to inspect
        vars_to_get: list[str] = []

        # All feature vectors xk_j
        for feat in self.features:
            for j in range(self.Nbound):
                vars_to_get.append(f"{feat}_{j}")

        # Append check-sat and get-value to the SMT file
        self._addLineInMain("(check-sat)")
        if vars_to_get:
            self._addLineInMain(f"(get-value ({' '.join(vars_to_get)}))")

        # Run Z3 and capture output; hide stderr to avoid noisy
        # "model is not available" messages in unsat case.
        proc = subprocess.run(
            ["z3", self.filename],
            capture_output=True,
            text=True
        )

        stdout = proc.stdout.strip()
        stderr = proc.stderr.strip()

        # For debugging you can uncomment:
        # print("=== Z3 STDOUT ===")
        # print(stdout)
        # print("=== Z3 STDERR ===")
        # print(stderr)

        if not stdout:
            raise RuntimeError("Z3 produced no output. Check your Z3 installation / path.")

        lines = stdout.splitlines()
        status = lines[0].strip()  # 'sat', 'unsat', or 'unknown'

        # If unsat or unknown, there is no model → no values to parse
        if status != "sat":
            return status, {}

        # For sat: the remaining lines are the response to (get-value ...)
        get_value_text = "\n".join(lines[1:])
        values = parse_get_value_output(get_value_text, self.bitvect)

        return status, values