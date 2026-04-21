""" This program creates verification tasks for GNNs. It has flow

Python programm -[generate]-> Z3 programm -[parse]-> Z3 solver -[obtain]-> Results SAT or non SAT.

Returns:
    _type_: _description_
"""
import os
import psutil
from datetime import datetime
import time
import subprocess
import sys
import numpy as np
from pathlib import Path as PathlibPath
sys.path.insert(0, str(PathlibPath(__file__).parent.parent))
from z3_flow.utils import convert_condition_to_smt, numpy_float32_to_smt_fp, build_fp_add_chain, build_add_chain

Number = int | float

class Z3VerificationFloat32:
    
    def __init__(self,Nnodes=2,Nfeatures=3,in_filename_smt="main.smt",in_activation='ReLU', in_configurations='xC+b_C',in_dtype="Float32"):  
        self.index_of_feature=0
        self.Nbound = Nnodes
        self.number_of_input_features = Nfeatures
        self.number_of_output_features = Nnodes
        self.filename = in_filename_smt
        self.start_of_program = "w"
        self.features =[]
        self.activation =in_activation
        self.configurations =in_configurations
        self.dtype = in_dtype
        if self.dtype == "Float32":
            self.zero="(fp #b0 #b00000000 #b00000000000000000000000)"
            self.one="(fp #b0 #b01111111 #b00000000000000000000000)"
            self.agg_operation = "fp.add RNE"
            self.mul_operation = "fp.mul RNE"
            self.gt="fp.gt"
        elif self.dtype == "Real":
            self.zero="0.0"
            self.one="1.0"
            self.agg_operation = "+"
            self.mul_operation = "*"
            self.gt=">"
        else:
            raise ValueError("Unsupported dtype")
        self._addLineInMain(f";; SMT encoding for ACR-GNN verification with {self.dtype} precision")
        self._addLineInMain(f";; Activation function: {self.activation}")
        self._addLineInMain(f"(set-option :produce-models true)")
        self._addLineInMain(f"(set-option :produce-unsat-cores true)")
        self._addLineInMain(f"(declare-const fp0 {self.dtype})")
        self._addLineInMain(f"(assert (= fp0 {self.zero}))")
        self._addLineInMain(f"(declare-const fp1 {self.dtype})")
        self._addLineInMain(f"(assert (= fp1 {self.one}))")
        self.adj_matrix()
        
    def _addLineInMain(self,line):
        with open(self.filename, self.start_of_program) as smt_file:
            smt_file.write(f"{line}\n")
        self.start_of_program ="a"
    
    def adj_matrix(self):  
        self._addLineInMain(f";; adjacency matrix of unknown graph")        
        for i in range(self.Nbound):
            for j in range(self.Nbound):
                self._addLineInMain(f"(declare-const e{i}_{j} Bool)")
        self._addLineInMain(f"")

    def _add_adj_matrix(self,matrix):
        self._addLineInMain(";; hard code the example one.")

        rows, cols = matrix.shape

        for i in range(rows):
            for j in range(cols):
                val = "true" if matrix[i, j] == 1 else "false"
                self._addLineInMain(f"(assert (= e{i}_{j} {val}))")
        self._addLineInMain(f"")

    def _get_new_featurename(self):
        featureName = f"x{self.index_of_feature}"
        self.features.append(featureName)
        self.index_of_feature = self.index_of_feature + 1
        return featureName
    
    def add_input_node(self):
        x_feature=self._get_new_featurename()
        if x_feature == "x0":
            self._addLineInMain(f";; declare nodes with dimension of the number of features.")
        self._addLineInMain(f";; declare node {x_feature}") 
        for j in range(self.number_of_input_features):
            self._addLineInMain(f"(declare-const {x_feature}_{j} {self.dtype})")
        self._addLineInMain(f"")
        return x_feature

    def _add_node(self,features):
        x_feature=self._get_new_featurename()
        self._addLineInMain(f";; declare node {x_feature}") 
        for j in range(features):
            self._addLineInMain(f"(declare-const {x_feature}_{j} {self.dtype})")
        self._addLineInMain(f"")
        return x_feature
    
    def _add_node_binary_classification(self,features):
        x_feature=self._get_new_featurename()
        self._addLineInMain(f";; declare node {x_feature}") 
        for j in range(features):
            self._addLineInMain(f"(declare-const {x_feature}_{j} Int)")
        self._addLineInMain(f"")
        return x_feature
    
    def add_precondition(self, cond: str):
        self._addLineInMain(f";; precondition {cond}") 
        smt_line = convert_condition_to_smt(cond,self.features,"precondition", self.dtype)
        self._addLineInMain(f"{smt_line}")
        self._addLineInMain(f"")

    def add_one_hot_row_precondition(self, x_feature, num_features):
        self._addLineInMain(f";; one-hot precondition for {x_feature} with {num_features} features")
        previousFeatures = self.features[-1:]
        for node in previousFeatures:
            if self.dtype == "Float32":
                sum_expr = build_fp_add_chain([f"{node}_{j}" for j in range(self.number_of_input_features)])
                self._addLineInMain(f"(assert (= {sum_expr} fp1))")

            elif self.dtype == "Real":
                sum_expr = build_add_chain([f"{node}_{j}" for j in range(self.number_of_input_features)])
                self._addLineInMain(f"(assert (= {sum_expr} 1.0))")
            else:
                raise ValueError(f"Unsupported dtype for one-hot row precondition: {self.dtype}")

        self._addLineInMain("")



    def add_layer(self,
                  V: list[list[Number]],
                  A: list[list[Number]], 
                  R: list[list[Number]],
                  b_V: list[Number],
                  b_A: list[Number],
                  b_R: list[Number],
                  bn_a: list[Number],
                  bn_c: list[Number]):
        
        previousFeatures = self.features[-self.Nbound:]
        if len(previousFeatures) != self.Nbound:
            raise ValueError("Not enough features allocated for input_dimension.")
        
        features_per_layer = V.shape[1]#!!!!!!!!!!
        
        self._addLineInMain(f";; decline features for the local aggregation.")
        aggPreviousFeatures = [self._add_node(features_per_layer) for j in range(self.Nbound)]
        self._addLineInMain(f";; decline features for the global aggregation.")
        aggGPreviousFeatures = [self._add_node(features_per_layer) for j in range(self.Nbound)]
        
        #block of local aggregation
        self._addLineInMain(";; Local aggregation (across neighbours)")
        self._addLineInMain("")

        for v in range(self.Nbound):
            out_base = aggPreviousFeatures[v]
            in_base_comment = previousFeatures[v]
            self._addLineInMain(f";; agg_local({out_base},{in_base_comment})")

            for f in range(self.number_of_input_features):
                terms = []
                for j in range(self.Nbound):
                    terms.append(
                        f"(ite e{v}_{j} {previousFeatures[j]}_{f} {self.zero})"
                    )

                expr = terms[0]
                for t in terms[1:]:
                    expr = f"({self.agg_operation} {expr} {t})"

                self._addLineInMain(f"(assert")
                self._addLineInMain(f"  (= {out_base}_{f}")
                self._addLineInMain(f"     {expr}")
                self._addLineInMain(f"  )")
                self._addLineInMain(f")")
                self._addLineInMain("")

        self._addLineInMain(";; end local aggregation")
        self._addLineInMain("")
            
        #block of global aggregation
        self._addLineInMain(";; Global aggregation")

        for v in range(self.Nbound):
            out_base = aggGPreviousFeatures[v]
            self._addLineInMain(f";; Compute global agg({out_base})")

            for f in range(self.number_of_input_features):
                terms = []
                for j in range(self.Nbound):
                    terms.append(f"{previousFeatures[j]}_{f}")

                expr = terms[0]
                for t in terms[1:]:
                    expr = f"({self.agg_operation} {expr} {t})"

                self._addLineInMain(f"(assert (= {out_base}_{f}")
                self._addLineInMain(f"          {expr}))")

            self._addLineInMain(f";; end global agg({out_base})")
            self._addLineInMain("")

        #block of the matrix multiplication
        self._addLineInMain(f";; matrix multiplication")
        
        self._addLineInMain(f";;np.dot(FM,V) xV")
        outputFeatures = [self._add_node(features_per_layer) for _ in range(len(previousFeatures))]

        for node_idx, out_base in enumerate(outputFeatures):
            in_base = previousFeatures[node_idx]

            for out_f in range(V.shape[1]):
                terms = []
                for in_f in range(V.shape[0]):
                    if self.dtype == "Float32":
                        coef = numpy_float32_to_smt_fp(V[in_f][out_f])
                    else:
                        coef = format(np.float32(V[in_f][out_f]), ".9g")

                    terms.append(f"({self.mul_operation} {in_base}_{in_f} {coef})")

                expr = terms[0]
                for t in terms[1:]:
                    expr = f"({self.agg_operation} {expr} {t})"

                self._addLineInMain("(assert")
                self._addLineInMain(f"  (= {out_base}_{out_f}")
                self._addLineInMain(f"     {expr}")
                self._addLineInMain("  )")
                self._addLineInMain(")")
            self._addLineInMain("")

        self._addLineInMain(f";;np.dot(V,FM) + b_V")
        num_features = len(b_V)
        outputFeatures_bias = [self._add_node(features_per_layer) for _ in range(len(outputFeatures))]
        for node_idx, out_base in enumerate(outputFeatures_bias):
            in_base = outputFeatures[node_idx]

            for f in range(num_features):

                if self.dtype == "Float32":
                    coef = numpy_float32_to_smt_fp(b_V[f])
                else:
                    coef = format(np.float32(b_V[f]), ".9g")

                self._addLineInMain("(assert")
                self._addLineInMain(f"   (= {out_base}_{f}")
                self._addLineInMain(f"      ({self.agg_operation} {in_base}_{f} {coef})")
                self._addLineInMain("   )")
                self._addLineInMain(")")

            self._addLineInMain("")

        #yA
        self._addLineInMain(f";;np.dot(agg_local,A) yA")
        outputFeatures_agg_local = [self._add_node(features_per_layer) for _ in range(len(aggPreviousFeatures))]

        for node_idx, out_base in enumerate(outputFeatures_agg_local):
            in_base = aggPreviousFeatures[node_idx]

            for out_f in range(A.shape[1]):
                terms = []
                for in_f in range(A.shape[0]):
                    if self.dtype == "Float32":
                        coef = numpy_float32_to_smt_fp(A[in_f][out_f])
                    else:
                        coef = format(np.float32(A[in_f][out_f]), ".9g")

                    terms.append(f"({self.mul_operation} {in_base}_{in_f} {coef})")

                expr = terms[0]
                for t in terms[1:]:
                    expr = f"({self.agg_operation} {expr} {t})"

                self._addLineInMain("(assert")
                self._addLineInMain(f"  (= {out_base}_{out_f}")
                self._addLineInMain(f"     {expr}")
                self._addLineInMain("  )")
                self._addLineInMain(")")
            self._addLineInMain("")

        self._addLineInMain(f";;np.dot(agg_local,A) + b_A")
        num_features = len(b_A)
        outputFeatures_bias_agg_local = [self._add_node(features_per_layer) for _ in range(len(outputFeatures_agg_local))]
        for node_idx, out_base in enumerate(outputFeatures_bias_agg_local):
            in_base = outputFeatures_agg_local[node_idx]

            for f in range(num_features):

                if self.dtype == "Float32":
                    coef = numpy_float32_to_smt_fp(b_A[f])
                else:
                    coef = format(np.float32(b_A[f]), ".9g")

                self._addLineInMain("(assert")
                self._addLineInMain(f"   (= {out_base}_{f}")
                self._addLineInMain(f"      ({self.agg_operation} {in_base}_{f} {coef})")
                self._addLineInMain("   )")
                self._addLineInMain(")")

            self._addLineInMain("")
        #zR
        self._addLineInMain(f";;np.dot(agg_global,R) zR")
        outputFeatures_agg_global = [self._add_node(features_per_layer) for _ in range(len(aggGPreviousFeatures))]

        for node_idx, out_base in enumerate(outputFeatures_agg_global):
            in_base = aggGPreviousFeatures[node_idx]

            for out_f in range(R.shape[1]):
                terms = []
                for in_f in range(R.shape[0]):
                    if self.dtype == "Float32":
                        coef = numpy_float32_to_smt_fp(R[in_f][out_f])
                    else:
                        coef = format(np.float32(R[in_f][out_f]), ".9g")

                    terms.append(f"({self.mul_operation} {in_base}_{in_f} {coef})")

                expr = terms[0]
                for t in terms[1:]:
                    expr = f"({self.agg_operation} {expr} {t})"

                self._addLineInMain("(assert")
                self._addLineInMain(f"  (= {out_base}_{out_f}")
                self._addLineInMain(f"     {expr}")
                self._addLineInMain("  )")
                self._addLineInMain(")")
            self._addLineInMain("")

        self._addLineInMain(f";;np.dot(agg_global,R) + b_R")
        num_features = len(b_R)
        outputFeatures_bias_agg_global = [self._add_node(features_per_layer) for _ in range(len(outputFeatures_agg_global))]
        for node_idx, out_base in enumerate(outputFeatures_bias_agg_global):
            in_base = outputFeatures_agg_global[node_idx]

            for f in range(num_features):

                if self.dtype == "Float32":
                    coef = numpy_float32_to_smt_fp(b_R[f])
                else:
                    coef = format(np.float32(b_R[f]), ".9g")

                self._addLineInMain("(assert")
                self._addLineInMain(f"   (= {out_base}_{f}")
                self._addLineInMain(f"      ({self.agg_operation} {in_base}_{f} {coef})")
                self._addLineInMain("   )")
                self._addLineInMain(")")
            self._addLineInMain("")
        
        # sum of the three terms
        self._addLineInMain(f";;(np.dot(V,FM) + b_V)+(np.dot(A,agg_local) + b_A)+(np.dot(R,agg_global) + b_R)")
        outputFeatures_sum = [self._add_node(features_per_layer) for _ in range(self.Nbound)]
        for node_idx, out_base in enumerate(outputFeatures_sum):
            in_base1 = outputFeatures_bias[node_idx]
            
            in_base2 = outputFeatures_bias_agg_local[node_idx]
            
            in_base3 = outputFeatures_bias_agg_global[node_idx]
            

            for f in range(self.number_of_input_features):
                self._addLineInMain("(assert")
                self._addLineInMain(f"   (= {out_base}_{f}")
                self._addLineInMain(f"      ({self.agg_operation} ({self.agg_operation} {in_base1}_{f} {in_base2}_{f}) {in_base3}_{f})")
                self._addLineInMain("   )")
                self._addLineInMain(")")
            self._addLineInMain("")

        # applying activation function
        self._addLineInMain(f";; applying activation function")
        self._addLineInMain(f";; activation function: {self.activation}")
        if self.activation == "ReLU":
            self._addLineInMain(f"(define-fun {self.activation} ((x {self.dtype})) {self.dtype}")
            self._addLineInMain(f"  (ite ({self.gt} x fp0) x fp0)")
            self._addLineInMain(f")")
           
        outputFeatures_act = [self._add_node(features_per_layer) for _ in range(self.Nbound)]
        for node_idx, out_base in enumerate(outputFeatures_act):
            in_base = outputFeatures_sum[node_idx]

            for f in range(self.number_of_input_features):
                self._addLineInMain("(assert")
                self._addLineInMain(f"   (= {out_base}_{f}")
                self._addLineInMain(f"      ({self.activation} {in_base}_{f})")
                self._addLineInMain("   )")
                self._addLineInMain(")")
            self._addLineInMain("")
        self._addLineInMain(f";; applying Batch Normalization. Linear form: bn_a * act + bn_c")
        self._addLineInMain(f";; bn_a and bn_c are computed from the parameters of the batch normalization layer as follows:")
        self._addLineInMain(f";; bn_a = gamma / sqrt(running_var + eps)")
        self._addLineInMain(f";; bn_c = beta - (gamma * running_mean) / sqrt(running_var + eps)")
        self._addLineInMain(f";; act[i][j]*a[j] + c[j]")
        outputFeatures_BN = [self._add_node(features_per_layer) for _ in range(self.Nbound)]
        for node_idx, out_base in enumerate(outputFeatures_BN):
            in_base = outputFeatures_act[node_idx]

            for f in range(self.number_of_input_features):
                if self.dtype == "Float32":
                    bn_a_coef = numpy_float32_to_smt_fp(bn_a[f])
                    bn_c_coef = numpy_float32_to_smt_fp(bn_c[f])
                else:
                    bn_a_coef = format(np.float32(bn_a[f]), ".9g")
                    bn_c_coef = format(np.float32(bn_c[f]), ".9g")
                self._addLineInMain("(assert")
                self._addLineInMain(f"   (= {out_base}_{f}")
                self._addLineInMain(f"      ({self.agg_operation} ({self.mul_operation} {in_base}_{f} {bn_a_coef}) {bn_c_coef})")
                self._addLineInMain("   )")
                self._addLineInMain(")")
            self._addLineInMain("")
        self._addLineInMain(f";; end layer")
        self._addLineInMain("")
    
    def add_linear_prediction_layer(self,
                                   W: list[list[Number]],
                                   b: list[list[Number]]):    
        self._addLineInMain(f";; Linear Prediction np.dot(BN, W_LP) + b_LP")
        features_per_layer = W.shape[1]
        outputFeatures_BN = self.features[-self.Nbound:]
        outputFeatures_LP = [self._add_node(features_per_layer) for _ in range(len(outputFeatures_BN))]
        self._addLineInMain(f";; np.dot(BN, W_LP)")
        for node_idx, out_base in enumerate(outputFeatures_LP):
            in_base = outputFeatures_BN[node_idx]

            for out_f in range(W.shape[1]):
                terms = []
                for in_f in range(W.shape[0]):
                    if self.dtype == "Float32":
                        coef = numpy_float32_to_smt_fp(W[in_f][out_f])
                    else:
                        coef = format(np.float32(W[in_f][out_f]), ".9g")

                    terms.append(f"({self.mul_operation} {in_base}_{in_f} {coef})")

                expr = terms[0]
                for t in terms[1:]:
                    expr = f"({self.agg_operation} {expr} {t})"

                self._addLineInMain("(assert")
                self._addLineInMain(f"  (= {out_base}_{out_f}")
                self._addLineInMain(f"     {expr}")
                self._addLineInMain("  )")
                self._addLineInMain(")")
            self._addLineInMain("")

        self._addLineInMain(f";;np.dot(BN, W_LP) + b_LP")
        num_features = len(b)
        outputFeatures_bias_LP = [self._add_node(features_per_layer) for _ in range(len(outputFeatures_LP))]
        for node_idx, out_base in enumerate(outputFeatures_bias_LP):
            in_base = outputFeatures_LP[node_idx]

            for f in range(num_features):

                if self.dtype == "Float32":
                    coef = numpy_float32_to_smt_fp(b[f])
                else:
                    coef = format(np.float32(b[f]), ".9g")

                self._addLineInMain("(assert")
                self._addLineInMain(f"   (= {out_base}_{f}")
                self._addLineInMain(f"      ({self.agg_operation} {in_base}_{f} {coef})")
                self._addLineInMain("   )")
                self._addLineInMain(")")

            self._addLineInMain("")
        self._addLineInMain(f";; end linear prediction layer")
        self._addLineInMain(f"")

        self._addLineInMain(f";;Binary classification")
        self._addLineInMain(f"(define-fun argmax ((x {self.dtype}) (y {self.dtype})) Int")
        self._addLineInMain(f"  (ite ({self.gt} x y) 0 1)")
        self._addLineInMain(f")")
        num_features = 1
        Binary_classification = [self._add_node_binary_classification(num_features) for _ in range(len(outputFeatures_bias_LP))]
        
        for node_idx, out_base in enumerate(Binary_classification):
            in_base = outputFeatures_bias_LP[node_idx]
            for f in range(num_features):
                self._addLineInMain("(assert")
                self._addLineInMain(f"   (= {out_base}_{f}")
                self._addLineInMain(f"      (argmax {in_base}_0 {in_base}_1)")
                self._addLineInMain("   )")
                self._addLineInMain(")")

    def get_lasts(self, number_of_features_that_you_need):
        result = self.features[-number_of_features_that_you_need:]    
        return result
    
    def add_postcondition(self, cond: str):
        self._addLineInMain(f";; postcondition {cond}")
        int_features = self.features[-self.Nbound:]   # e.g. ['x28', 'x29']
        smt_line = convert_condition_to_smt(
            cond,
            self.features,
            "postcondition",
            default_dtype=self.dtype,
            int_features=int_features
        )
        self._addLineInMain(smt_line)
        self._addLineInMain("")

    def check(self,get_model=False,get_values=[], model_filename="model.txt",file_performance=f"performance.txt"):
        file_performance = self.filename.replace(".smt2", ".csv")
        file_exists = os.path.isfile(file_performance)
        model_filename = self.filename.replace(".smt2", ".txt")
        print(f"Checking satisfiability with Z3 for {self.filename}, results will be saved in {file_performance} and {model_filename}")
        self._addLineInMain(f"(check-sat)")

        if get_model:
            self._addLineInMain(f";;(get-model)")
            self._addLineInMain(f"(get-model)")
        
        input_nodes = self.features[:self.Nbound]
        
        self._addLineInMain(f";;(Feature Matrix for nodes)")
        for node in input_nodes:
            for i in range(self.number_of_input_features):
                self._addLineInMain(f"(get-value ({node}_{i}))")

        self._addLineInMain(f";;(Adjacency  Matrix for nodes)")
        for i in range(self.Nbound):
            for j in range(self.Nbound):
                self._addLineInMain(f"(get-value (e{i}_{j}))")
        
        #self._addLineInMain(f"(get-unsat-core)")        
        if len(get_values) > 0:
            for feature in get_values:
                self._addLineInMain(f"(get-value ({feature}))")

        # Run Z3 and capture output; hide stderr to avoid noisy
        # "model is not available" messages in unsat case.
        self._addLineInMain(f";; Binary classification result (0 or 1) for each node")
        terms = [f"{name}_0" for name in self.features[-self.Nbound:]]
        self._addLineInMain(f"(get-value ({' '.join(terms)}))")
        
        start_time = time.time()
        proc = subprocess.run(
            ["z3", self.filename],
            capture_output=True,
            text=True
        )
        end_time = time.time()
        with open(file_performance, "a", newline="", encoding="utf-8") as perf_file:
            if not file_exists:
                perf_file.write("DateTime,Nodes,NumConstants,ExecutionTime(s),CPU(%),Memory(%),dType, Activation\n")

            perf_file.write(
                f"{datetime.now().isoformat()},"
                f"{self.Nbound},"
                f"{self.index_of_feature},"
                f"{end_time - start_time},"
                f"{psutil.cpu_percent()},"
                f"{psutil.virtual_memory().percent},"
                f"{self.dtype},"
                f"{self.activation}\n"
            )
        print("Execution time:", end_time - start_time, "seconds")
        print("CPU usage:", psutil.cpu_percent())
        print("Memory usage:", psutil.virtual_memory().percent)
        print("Z3 output:")
        print(proc.stdout)  
        # ---- SAVE MODEL ----
        output = proc.stdout.strip()

        if output.startswith("sat"):
            with open(model_filename, "w") as f:
                f.write(output)

        elif output.startswith("unsat"):
            with open(model_filename, "w") as f:
                f.write(output)

        else:
            print("Unknown result, saving raw output for debugging")
            with open(model_filename, "a", encoding="utf-8") as f:
                f.write(output)