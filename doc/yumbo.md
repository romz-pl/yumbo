## :green[Intro]
The primary objective of the project is to develop software that facilitates the optimal creation of daily schedules. This software will address the challenge faced by project managers, solution architects, and other professionals working on multiple tasks or projects simultaneously, enabling them to manage their time and resources more efficiently.


## :green[Assumptions]
It is assumed that each task is defined by its start date and end date, and that the expert is required to complete the fixed number of working hours during the lifetime of the task. It is also assumed that tasks can overlap and that the start and end dates of tasks are independent of each other. The lifetime of a task in the use cases studied so far was typically about 200 business days. Note, however, that the software does not impose any restrictions on the duration of a task.


## :green[Objectives]
The project has two goals. The first is to verify that the schedule meets the constraints of the business rules. The current version of Yumbo takes into account the following business rules: the allowed number of working hours per day, the availability of experts, and the experts' vacations and holidays. Second, once the existence of the schedule has been verified, the daily schedule must be generated. It is assumed that the smallest working time unit is a quarter of an hour. This assumption is made with the understanding that during a standard working day, an expert's engagement with the task is not shorter than a quarter of an hour.


## :green[Planning horizon]
The software facilitates both short-term and long-term planning. The use of Yumbo ensures that the expert is equipped with adequate resources to meet the long-term requirements of each task. In addition, the software facilitates short-term planning and scheduling, thereby increasing the expert's comfort level. It is recommended to use Yumbo frequently and regularly, e.g. weekly. For example, the schedule should be updated when the expert's availability changes or when a new task is added to the task pool.


## :green[Mathematical model]
The aforementioned problem is resolved by a mathematical model based on Mixed Integer Linear Programming, implemented in AMPL language and solved by HiGHS, a high-performance software for linear optimisation.


## :green[Formulation of the mathematical model]
The following definition of a solved problem is provided. A set of tasks is defined, with each task characterised by three properties: (a) the start date; (b) the end date; (c) the work expressed in hours. Each task in the set is assigned to at least one expert, and an expert can be assigned to one or more tasks. Consequently, there is a many-to-many relationship between tasks and experts. Constraints are further categorised into four classes, each of which is optional. The objective is to determine the expert's daily schedule that satisfies the following constraints:
- The number of hours worked per day must not exceed the limit.
- For each call period, the total number of hours worked must be within the limit.
- For each day, for each task, the number of hours worked per day must be within the limit.
- For an expert, the number of hours worked per day must be within the limit for each day.


## :green[Implementation details]
1. The problem is formulated as a linear mixed-integer problem with an objective function that favours early task completion.
2. The solution to the problem is a daily work schedule that specifies the number of hours to be worked on the task for each day.
3. The mathematical problem is implemented as a [AMPL](https://ampl.com/) program and solved by [HiGHS](https://highs.dev/) solver.
4. The graphical user interface is written in [Python](https://www.python.org/) within the [Streamlit](https://streamlit.io/) framework.
5. The plots are generated using the [Matplotlib](https://matplotlib.org/) library, and the data is processed using the [Pandas](https://pandas.pydata.org/) and [NumPy](https://numpy.org/) Python libraries.


## :green[The list of the tools and libraries that are used]
- [AMPL](https://ampl.com/) a mathematical programming language; 
- [HiGHS](https://highs.dev/) a high performance software for linear optimization; 
- [SCIP](https://www.scipopt.org/) one of the fastest non-commercial solvers for mixed integer programming and mixed integer nonlinear programming;
- [GCG](https://gcg.or.rwth-aachen.de/) a generic decomposition solver for mixed-integer programs (MIPs);
- [Streamlit](https://streamlit.io/) a faster way to build and share data apps; 
- [Python](https://www.python.org/) a programming language that lets you work quickly; 
- [Pandas](https://pandas.pydata.org/) a fast, powerful, flexible and easy to use open source data analysis and manipulation tool; 
- [Matplotlib](https://matplotlib.org/) a comprehensive library for creating static, animated, and interactive visualizations in Python; 
- [NumPy](https://numpy.org/) the fundamental package for scientific computing with Python;


## :green[Source code]
The programme is implemented in Python. The source code is available in the GitHub repository [Yumbo](https://github.com/romz-pl/yambo/).


