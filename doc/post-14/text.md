# 📅 Yumbo. Input Parameters for Efficient Scheduling

Yumbo is a robust scheduling program that organizes its input parameters through an Excel file, thereby facilitating a streamlined and systematic approach to resource planning. A comprehensive understanding of these parameters is imperative for the effective utilization of Yumbo.



## Mandatory Input Parameters
The number of mandatory parameters for Yumbo is very small. It requires only three sets of parameters: **experts**, **task**, and **assignment**, which defines the many-to-many relationship between tasks and experts. The business problem is related to these three sets.

The next mandatory parameters define the first date of the schedule and the maximum number of working hours per day, which is usually eight. Other parameters, such as the name of the **mathematical model** and the name of the integer programming **solver** used, are directly related to the algorithm. Currently there are four math modules. They differ in memory usage and functionality.



## Optional Input Parameters
To define the characteristics of the designed schedule, Yumbo uses linear constraints of the linear mathematical model. The current version of Yumbo supports four types of constraints: xbday, ubday, ebday, pbsum. The **xbday** constraint is the most common type of constraint and specifies the upper and lower limits of hours an expert can work on a task within a date range. The **ubday** constraint is used to define the number of tasks per day for an expert. Expert availability and preferences are defined by **ebday** constraints. To limit the number of hours per billing period, you can use the **pbsum** constraints.

In addition, if you want to avoid working on holidays, you need to specify the list of dates that define the **holidays**.



## Additional Reporting Parameters
Yumbo also includes eight spreadsheets in the Excel input file that store reporting parameters. These do not affect scheduling, but serve as valuable parameters that influence analysis and insight.



💡 By structuring inputs in this manner, Yumbo ensures a systematic, flexible, and efficient scheduling process. Mastering these parameters enables organizations to **optimize workforce allocation** and project timelines effectively.


🔗 **Source code** of the Yumbo is available at https://github.com/romz-pl/yumbo/




```
#OperationsResearch
#IntegerProgramming
#Scheduling
#Planning
#ProjectManagement
```


Image created by ChatGPT.

