# Open source linear programming solvers

For my projects dedicated to solving optimisation problems, I use the **HiGHS** solver. It is the open source serial and parallel solver for large sparse linear programming (LP), mixed integer programming (MIP), and quadratic programming (QP) models. The solver is written in C++ and integrates seamlessly with AMPL. HiGHS is freely available under the MIT licence and can be downloaded from GitHub https://highs.dev/ 

HiGHS is not the only option available in open source community when solving optimisation problems. The second favuorite of mine is **SCIP** developed in Zuse Institute Berlin (ZIB). SCIP is a framework for constraint integer programming that caters to the requirements of mathematical programming experts. It enables these experts to exercise complete control over the solution process and access detailed information regarding the inner workings of the solver. Additionally, SCIP can be utilised as a standalone mixed-integer programming (MIP) and mixed-integer nonlinear programming (MINLP) solver, or as a framework for branch-and-cut and price-seeking https://scipopt.org/

In my optimisation projects I also use **GCG**, which extends the SCIP solver and is also available as open source. GCG is a generic decomposition solver for mixed integer programs (MIPs). It automatically performs a Dantzig-Wolfe reformulation. It then runs a full branch-price-and-cut algorithm to solve to optimality https://gcg.or.rwth-aachen.de/


It should be noted that there are other open source solvers available. The following list contains descriptions of four of them:

+ [**CBC (COIN-OR Branch and Cut)**](https://github.com/coin-or/Cbc)
The CBC solver is part of the COIN-OR (Computational Infrastructure for Operations Research) project. It specialises in solving mixed integer linear programming (MILP) problems using branch and cut algorithms. CBC supports extensive customisation and is well suited for research and practical applications. It integrates with Python through the Pyomo and PuLP libraries.

+ [**GLPK (GNU Linear Programming Kit)**](https://www.gnu.org/software/glpk/)
GLPK is a versatile solver for large-scale linear programming (LP), mixed integer programming (MIP), and other related optimisation problems. Developed as part of the GNU project, it is written in C and provides a robust API. GLPK is widely used for academic purposes and supports integration with modelling languages such as MathProg.

+ [**LP_SOLVE**](https://lpsolve.sourceforge.net/)
LP_SOLVE is a lightweight solver for LP and MILP problems, supporting a wide range of constraints and optimisation techniques. Developed in C, it is known for its simplicity and ease of use. LP_SOLVE is widely used in educational contexts and is compatible with many programming languages and modelling environments.

+ [**Bonmin**](https://github.com/coin-or/Bonmin)
Bonmin (Basic Open-source Nonlinear Mixed Integer Programming) is a solver for mixed integer nonlinear programming (MINLP) problems, but can handle ILP as a subset of its capabilities. Developed within the COIN-OR project, it combines branch-and-bound and nonlinear programming methods, making it suitable for specialised optimisation tasks.


There is a large and vibrant open source community involved in the development of linear programming solvers. Visit the [**COIN-OR**](https://www.coin-or.org/) website to learn more about open source for the operations research community.


```
#OpenSource
#OpenSourceSolvers
#OperationsResearch
#LinearOptimization
#IntegerProgramming
```

![Open source linear programming solvers](./img.webp)

Image created by ChatGPT.

 
