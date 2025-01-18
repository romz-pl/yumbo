
# Optimal generation of daily schedules

As a Principal Data Scientist, I am involved in a project that focuses on the optimal generation of daily schedules. The software developed should solve the problem of optimal schedule generation for project managers, solution architects, or any expert involved in more than one task or project simultaneously.

The assumption is that each task is defined by its start date and its end date. During the **fixed task period**, the expert is obliged to complete the fixed number of working hours, which is usually less than 30% of the total working hours available. It is also assumed that the tasks can overlap and that the start and end dates of the tasks are independent of each other. The lifetime of a task can be up to 200 working days. However, there is no limit to the lifetime of a task in the software.

The project has two objectives. The first objective is to check that the schedule is in compliance with the constraints of the **business rules**. The following business rules are taken into account: the permitted number of working hours per day, the availability of experts, the holidays of experts and public holidays. Secondly, once the existence of the schedule has been checked, the daily schedule must be generated. It is assumed that the smallest working time unit is one hour. This means that during a normal working day, the expert can be involved in up to eight tasks, each of which takes exactly one hour to complete.

Both **short and long-term planning** is possible with the software. By using this software, we ensure that the expert has sufficient resources to meet the long-term requirements of each task. For the convenience of the expert, short-term planning and scheduling is also provided. Of course, the schedule can be updated if the expert's availability changes or a new task is added to the task pool. 

The above problem is solved by a mathematical model based on Mixed Integer Linear Programming, implemented in **AMPL language** and solved by HiGHS, a high performance software for linear optimisation.

You can find out more about the broad topics of operations research in the book M.W. Carter, C.C. Price, G.R. **Operations Research A Practical Introduction** https://lnkd.in/dh8tvJKh

```
#OperationsResearch 
#DataScience 
#Optimization
#MathematicalModelling
```

