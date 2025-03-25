# 📅 Yumbo. Schedules for Developers



Creating efficient schedules for IT developers is a complex challenge, especially when multiple tasks overlap in time and workload. Developers often prefer to work on one problem at a time, from start to finish, without distractions. In the real world, however, they are often assigned multiple tasks with different start and end dates, making optimal scheduling difficult.

Enter Yumbo, a **powerful scheduling tool** designed to accommodate varying task assignments, employment contracts, and preferences. One of its key features is the UBDAY constraint, which allows schedulers to define the maximum number of tasks assigned to a developer per day.


## What are UBDAY constraints?
UBDAY constraints set upper and lower task limits for each expert on a given day. The most common scenario is to set the upper limit to 1, ensuring that a developer focuses on only one task at a time. However, Yumbo allows flexibility - any integer value can be specified as the upper and lower limit.


## Best practices
While setting the upper and lower bounds to the same number ensures a fixed number of tasks per day, it can sometimes lead to infeasible solutions. For example, if a developer has two overlapping tasks and both bounds are set to 2, scheduling becomes impossible. In such cases, it's advisable to set the lower bound to zero to allow for scheduling flexibility.


💡 Interestingly, due to inherent properties of its mathematical model, Yumbo's naturally produces schedules with one or two tasks per day, even without UBDAY constraints. Because adding constraints increases computation time, it's recommended to first test schedules without UBDAY constraints before selectively implementing them. Minimizing the number of days with UBDAY constraints also improves Yumbo's efficiency. This strategic application ensures better schedule feasibility while maintaining computational performance.


🔗 For those interested in exploring Yumbo, it is available as open source software on GitHub: https://github.com/romz-pl/yumbo/ and as a SaaS solution via Streamlit: https://yumbo-ampl.streamlit.app/.


```
#OperationsResearch
#IntegerProgramming
#Scheduling
#Planning
#MathematicalModeling
#AMPL
```


![Yumbo. Schedules for Developers](./img.webp)

Image created by ChatGPT.

