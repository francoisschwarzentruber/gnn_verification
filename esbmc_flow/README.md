# ACR-GNNVerification tool
Our goal is to translate an Aggregate Combine Graph Neural Network with the global Readout (ACR-GNN) to the code that we can pass trought Z3 solver

## Graph Neeural Network
In this code we are using the reference architecture of the paper of the Barcelo et. al.[1] with the implementation[2].

## Logic
For the Logic that we can use to verify chosen models is the modal $q\mathcal{L}$ Logic that was described in the article of [3],[4].

## Verification tool(s)
For these experiments we are using two verification tools: ESBMC[5] and Z3[6]. So in this case we have a comparison between the SMT solvers.

### Flow for Z3 SMT solver

Python programm -[generate]-> Z3 programm -[parse]-> Z3 solver -[obtain]-> Results SAT or non SAT.

### Flow from the ESBMC
Here we have a flow of the programms that e are using to have:

Python program -[generate]-> C program -[parse]-> ESBMC solver -[obtain]-> Result: SAT or UNSAT.

>[!Note]
> This repository provides a Python tool (main.py) that automatically generates C programm of small GNN-like layers and verifies postconditions using the ESBMC SMT solver.


## Reference

[1] Pablo Barceló, Egor V. Kostylev, Mikaël Monet, Jorge Pérez, Juan L. Reutter, and Juan Pablo Silva.  
**The Logical Expressiveness of Graph Neural Networks**, 8th International Conference on Learning Representations (ICLR), 2020.  
Available at: [https://openreview.net/forum?id=r1lZ7AEKvB](https://openreview.net/forum?id=r1lZ7AEKvB)

[2] Pablo Barceló, Egor V. Kostylev, Mikaël Monet, Jorge Pérez, Juan L. Reutter, and Juan Pablo Silva.  
**GNN-logic**, GitHub repository, 2021.  
Available at: [https://github.com/juanpablos/GNN-logic](https://github.com/juanpablos/GNN-logic)

[3]

[4]

[5] Menezes, R., Aldughaim, M., Farias, B., Li, X., Manino, E., Shmarov, F., Song, K., Brauße, F., Gadelha, M. R., Tihanyi, N., Korovin, K., & Cordeiro, L. C. **ESBMC 7.4: Harnessing the Power of Intervals**, TACAS, LNCS 14572, pp. 376–380. Springer,2024.  
Available at: [https://doi.org/10.1007/978-3-031-57256-2_24](https://doi.org/10.1007/978-3-031-57256-2_24)
    

[6] De Moura, Leonardo, and Nikolaj Bjørner. **Z3: An efficient SMT solver.**,TACAS. Springer, 2008.
Available at: [https://link.springer.com/chapter/10.1007/978-3-540-78800-3_24](https://link.springer.com/chapter/10.1007/978-3-540-78800-3_24)

## License

This project is licensed under the [MIT License](LICENSE).
