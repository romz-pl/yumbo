## :green[Intro]
The primary objective of the project is the development of software that will facilitate the creation of :blue[**optimal daily schedules**]. This software will address the challenge faced by project managers, solution architects, and other professionals working on multiple tasks or projects simultaneously, enabling them to manage their time and resources more efficiently.


## :green[Assumptions]
It is assumed that each task is defined by its :blue[**start date and end date**], and that the expert is required to complete the :blue[**fixed number of working hours**] during the lifetime of the task. It is also assumed that tasks can overlap and that the start and end dates of tasks are independent of each other. The lifetime of a task in the use cases studied so far was typically about 200 business days. Note, however, that the software does not impose any restrictions on the duration of a task.


## :green[Objectives]
The project has two goals. The first is to :blue[**verify**] that the schedule meets the constraints of the business rules. The current version of Yumbo takes into account the following business rules: the allowed number of working hours per day, the availability of experts, and the experts' vacations and holidays. Second, once the existence of the schedule has been verified, the daily schedule must be :blue[**generated**]. It is assumed that the smallest working time unit is a quarter of an hour. This assumption is made with the understanding that during a standard working day, an expert's engagement with the task is not shorter than a quarter of an hour.


## :green[Planning horizon]
The software facilitates both :blue[**short-term and long-term planning**]. The use of Yumbo ensures that the expert is equipped with adequate resources to meet the long-term requirements of each task. In addition, the software facilitates short-term planning and scheduling, thereby increasing the expert's comfort level. It is recommended to use Yumbo frequently and regularly, e.g. weekly. For example, the schedule should be updated when the expert's availability changes or when a new task is added to the task pool.


## :green[Mathematical models]
The above problem is solved by a mathematical model based on Integer Linear Programming, implemented in the language [AMPL](https://ampl.com/) (A Modeling Language for Mathematical Programming) and solved by [HiGHS](https://highs.dev/), a powerful software for linear optimization. At the moment there are four mathematical models. They differ in memory consumption and functionality. Two of the models are equipped with a feature to search for overflowing tasks, where the task is overflowing when there are not enough experts assigned to the task. In addition, there is a mathematical model that can be used to impose the constraints on the number of tasks per day.



## :green[Mathematical model formulation]
The definition of the problem that Yumbo solves is as follows. A set of :blue[**tasks**] is defined, each task being characterized by three properties: (a) the start date; (b) the end date; (c) the work (i.e., effort) expressed in hours. Each task in the set is assigned to at least one :blue[**expert**], and an expert can be assigned to one or more tasks. Thus, there is a :blue[**many-to-many relationship**] between tasks and experts. The constraints are further categorized into four classes, each of which is optional. The goal is to determine the expert's daily schedule that satisfies the following constraints:
- The number of work hours per day may not be in excess of the limit.
- The total number of hours worked must be within the limit for each billing period.
- The number of hours worked per day must be within the limit for each day, for each task.
- For each expert, the number of hours worked per day must be within the limit for each day.


## :green[Implementation details]
1. The problem is formulated as a :blue[**linear integer programming problem**]. The objective function favors early completion of the task.
2. The solution to this problem is a daily work schedule. This schedule specifies the number of hours each expert should work on the task each day.
3. The mathematical problem is implemented as a [AMPL](https://ampl.com/) program and solved by [HiGHS](https://highs.dev/) solver.
4. The graphical user interface is written in [Python](https://www.python.org/) within the [Streamlit](https://streamlit.io/) framework.
5. The plots are generated using the [Matplotlib](https://matplotlib.org/) library, and the data is processed using the [Pandas](https://pandas.pydata.org/) and [NumPy](https://numpy.org/) Python libraries.


## :green[List of tools and libraries]
- [AMPL](https://ampl.com/) a mathematical programming language; 
- [HiGHS](https://highs.dev/) a high performance software for linear optimization; 
- [SCIP](https://www.scipopt.org/) one of the fastest non-commercial solvers for mixed integer programming and mixed integer nonlinear programming;
- [GCG](https://gcg.or.rwth-aachen.de/) a generic decomposition solver for mixed-integer programs;
- [Streamlit](https://streamlit.io/) a faster way to build and share data apps; 
- [Python](https://www.python.org/) a programming language that lets you work quickly; 
- [Pandas](https://pandas.pydata.org/) a fast, powerful, flexible and easy to use open source data analysis and manipulation tool; 
- [Matplotlib](https://matplotlib.org/) a comprehensive library for creating static, animated, and interactive visualizations in Python; 
- [NumPy](https://numpy.org/) the fundamental package for scientific computing with Python;


## :green[Source code]
[Yumbo](https://github.com/romz-pl/yambo/) is implemented in Python. The source code is available in the GitHub repository as :blue[**open source**] under the MIT license.


## :green[Yumbo dedicated posts]

- [Optimal generation of daily schedules](https://github.com/romz-pl/yumbo/tree/main/doc/post-01/text.md)
- [Operations Research and Project Management](https://github.com/romz-pl/yumbo/tree/main/doc/post-02/text.md)
- [Mathematical model of the scheduling problem](https://github.com/romz-pl/yumbo/tree/main/doc/post-03/text.md)
- [Scheduling and timetable generation](https://github.com/romz-pl/yumbo/tree/main/doc/post-04/text.md)
- [Python for data scientists](https://github.com/romz-pl/yumbo/tree/main/doc/post-05/text.md)
- [Why every data scientist should be aware of Streamlit](https://github.com/romz-pl/yumbo/tree/main/doc/post-06/text.md)
- [Integer Programming: Lessons from Computational Mathematics](https://github.com/romz-pl/yumbo/tree/main/doc/post-07/text.md)
- [AMPL facilitates the formulation of optimisation problems](https://github.com/romz-pl/yumbo/tree/main/doc/post-08/text.md)
- [Value of the NEOS Server for operations research](https://github.com/romz-pl/yumbo/tree/main/doc/post-09/text.md)
- [Diversity of mathematical programming languages](https://github.com/romz-pl/yumbo/tree/main/doc/post-10/text.md)
- [Open source linear programming solvers](https://github.com/romz-pl/yumbo/tree/main/doc/post-11/text.md)
