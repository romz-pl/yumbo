The project is focuses on the optimal generation of daily schedules. The software developed should solve the problem of optimal schedule generation for project managers, solution architects, or any expert involved in more than one task or project simultaneously.

The assumption is that each task is defined by its start date and its end date. During the fixed task period, the expert is obliged to complete the fixed number of working hours, which is usually less than 40% of the total working hours available. It is also assumed that the tasks can overlap and that the start and end dates of the tasks are independent of each other. The lifetime of a task can be up to 200 working days. However, there is no limit to the lifetime of a task in the software.

The project has two objectives. The first objective is to check that the schedule is in compliance with the constraints of the business rules. The following business rules are taken into account: the permitted number of working hours per day, the availability of experts, the holidays of experts and public holidays. Secondly, once the existence of the schedule has been checked, the daily schedule must be generated. It is assumed that the smallest working time unit is one hour. This means that during a normal working day, the expert can be involved in up to eight tasks, each of which takes exactly one hour to complete.

Both short and long-term planning is possible with the software. By using this software, we ensure that the expert has sufficient resources to meet the long-term requirements of each task. For the convenience of the expert, short-term planning and scheduling is also provided. Of course, the schedule can be updated if the expert's availability changes or a new task is added to the task pool. 

The above problem is solved by a mathematical model based on Mixed Integer Linear Programming, implemented in AMPL language and solved by HiGHS, a high performance software for linear optimisation.



The more formal definition of problem solved is as follows. A set of tasks T is defined, each task being characterised by three properties:
- the start date
- the end date;
- the work expressed in hours.

Each task from the set T is assigned an employee.
In addition, there are four classes of constraints, each of which is optional.
The problem is to find the employee's daily schedule that satisfies the following constraints:
- The number of hours worked per day must not exceed the limit.
- For each invocing period, the total number of hours worked must be within the limit.
- Each day, for each task the number of hours worked per day must be within the limit.
- For an employee, for each day the number of hours worked per day must be within the limit.



The problem is formulated as a linear mixed-integer problem with an objective function that favours early task completion.
The solution to the problem is a daily work schedule that specifies the number of hours to be worked on the task for each day.
The mathematical problem is implemented as a [AMPL](https://ampl.com/) program
and solved by [HiGHS](https://highs.dev/) solver.
The graphical user interface is written in [Python](https://www.python.org/) within the [Streamlit](https://streamlit.io/) framework.
The plots are generated using the [Matplotlib](https://matplotlib.org/) library, 
and the data is processed using the [Pandas](https://pandas.pydata.org/) and [NumPy](https://numpy.org/) Python libraries.


### The list of the tools and libraries that are used

- [AMPL](https://ampl.com/) a mathematical programming language; 
- [HiGHS](https://highs.dev/) a high performance software for linear optimization; 
- [Streamlit](https://streamlit.io/) a faster way to build and share data apps; 
- [Python](https://www.python.org/) a programming language that lets you work quickly; 
- [Pandas](https://pandas.pydata.org/) a fast, powerful, flexible and easy to use open source data analysis and manipulation tool; 
- [Matplotlib](https://matplotlib.org/) a comprehensive library for creating static, animated, and interactive visualizations in Python; 
- [NumPy](https://numpy.org/) the fundamental package for scientific computing with Python;
