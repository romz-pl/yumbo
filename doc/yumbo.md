## :green[Intro]
The primary objective of the project is the development of software that will facilitate the creation of :blue[**optimal daily schedules**]. This software will address the challenge faced by project managers, solution architects, and other professionals working on multiple tasks or projects simultaneously, enabling them to manage their time and resources more efficiently.


## :green[Assumptions]
It is assumed that each task is defined by its :blue[**start date and end date**], and that the expert is required to complete the :blue[**fixed number of working hours**] during the lifetime of the task. It is also assumed that tasks can overlap and that the start and end dates of tasks are independent of each other. The lifetime of a task in the use cases studied so far was typically about 200 business days. Note, however, that the software does not impose any restrictions on the duration of a task.


## :green[Objectives]
The project has two goals. The first is to :blue[**verify**] that the schedule meets the constraints of the business rules. The current version of Yumbo takes into account the following business rules: the allowed number of working hours per day, the availability of experts, and the experts' vacations and holidays. Second, once the existence of the schedule has been verified, the daily schedule must be :blue[**generated**]. It is assumed that the smallest working time unit is a quarter of an hour. This assumption is made with the understanding that during a standard working day, an expert's engagement with the task is not shorter than a quarter of an hour.


## :green[Planning horizon]
The software facilitates both :blue[**short-term and long-term planning**]. The use of Yumbo ensures that the expert is equipped with adequate resources to meet the long-term requirements of each task. In addition, the software facilitates short-term planning and scheduling, thereby increasing the expert's comfort level. It is recommended to use Yumbo frequently and regularly, e.g. weekly. For example, the schedule should be updated when the expert's availability changes or when a new task is added to the task pool.


## :green[Mathematical models]
The above problem is solved by a mathematical model based on Integer Linear Programming, implemented in the language [AMPL](https://ampl.com/) (A Modeling Language for Mathematical Programming) and solved by [HiGHS](https://highs.dev/), a powerful software for linear optimization. At the moment there are four mathematical models:
- [solid](https://github.com/romz-pl/yumbo/tree/main/res/solid.ampl),
- [solid + overflow](https://github.com/romz-pl/yumbo/tree/main/res/solid-overflow.ampl),
- [solid + ubday](https://github.com/romz-pl/yumbo/tree/main/res/solid-ubday.ampl),
- [solid + ubday + overflow](https://github.com/romz-pl/yumbo/tree/main/res/solid-ubday-overflow.ampl).

The mathematical models differ in memory consumption and functionality. Two of the models (i.e., :blue[**solid**] and :blue[**solid + ubday + overflow**]) are equipped with a feature to search for overflowing tasks, where the task is overflowing when there are not enough experts assigned to the task. In addition, there are two mathematical models (i.e., :blue[**solid + ubday**] and :blue[**solid + ubday + overflow**]) that can be used to impose the constraints on the number of tasks per day.



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

- Optimal Generation of Daily Schedules, [post-01](https://github.com/romz-pl/yumbo/tree/main/doc/post-01/text.md)
- Operations Research and Project Management, [post-02](https://github.com/romz-pl/yumbo/tree/main/doc/post-02/text.md)
- Mathematical Model of the Scheduling Problem, [post-03](https://github.com/romz-pl/yumbo/tree/main/doc/post-03/text.md)
- Scheduling and Timetable Generation, [post-04](https://github.com/romz-pl/yumbo/tree/main/doc/post-04/text.md)
- Python for Data Scientists, [post-05](https://github.com/romz-pl/yumbo/tree/main/doc/post-05/text.md)
- Streamlit for Data Scientists, [post-06](https://github.com/romz-pl/yumbo/tree/main/doc/post-06/text.md)
- Integer Programming: Lessons from Computational Mathematics, [post-07](https://github.com/romz-pl/yumbo/tree/main/doc/post-07/text.md)
- AMPL, A Mathematical Programming Language, [post-08](https://github.com/romz-pl/yumbo/tree/main/doc/post-08/text.md)
- Value of the NEOS Server for Operations Research, [post-09](https://github.com/romz-pl/yumbo/tree/main/doc/post-09/text.md)
- Diversity of Mathematical Programming Languages, [post-10](https://github.com/romz-pl/yumbo/tree/main/doc/post-10/text.md)
- Open Source Linear Programming Solvers, [post-11](https://github.com/romz-pl/yumbo/tree/main/doc/post-11/text.md)
- Commercial Linear Programming Solvers, [post-12](https://github.com/romz-pl/yumbo/tree/main/doc/post-12/text.md)
- Yumbo. Scheduling, Planning and Resource Allocation, [post-13](https://github.com/romz-pl/yumbo/tree/main/doc/post-13/text.md)
- Yumbo. Input Parameters for Efficient Scheduling, [post-14](https://github.com/romz-pl/yumbo/tree/main/doc/post-14/text.md)
- Yumbo. Expert Availability and Preferences, [post-15](https://github.com/romz-pl/yumbo/tree/main/doc/post-15/text.md)


## :green[What others say about Yumbo]
- Eryk Makowski, Expert Software Engineer at Infopulse, [LinkedIn post](https://www.linkedin.com/feed/update/urn:li:share:7304112503754559488)


## :green[Yumbo's evolution. From Concept to Maturity]


The important thing is that Yumbo has gone through the entire cycle of advanced software development and can now be treated as a mature program. 
Below is the chronological order of the development stages:
- :blue[**The business problem has been identified!**]
- Natural language was used to formulate the business problem.
- The process of formulating the business problem with a mathematical rigor has been set in motion.
- To help formulate the problem, the tools of operations research were chosen.
- :blue[**Linear programming was used to develop the first version of the mathematical model.**]
- The more precise version of the mathematical model using integer linear programming was proposed.
- :blue[**The objective function that favors the early completion of the task was invented.**]
- Business requirements were incorporated into the mathematical model as integer linear problem constraints.
- Constraints XBDAY, UBDAY, PBSUM, XBSUM, UBSUM were introduced to represent the requirements and expectations of the business.
- A suitable name for the program was found. Yumbo was born!
- Additional mathematical constraints (XBSUM and UBSUM) were proposed and implemented.
- Designing schedules through the set of constraints was invented.
- Focusing on constraints as a means to design flexible schedules has been the subject of in-depth analysis.
- Integer linear mathematical model was implemented as AMPL program.
- A text mode prototype running on the NEOS service has been created and tested extensively.
- It has been observed that text mode is not sufficient for presenting complex constraints and schedules.
- :blue[**The process of finding the right framework for building web applications suitable for our purpose began. Streamlit was chosen.**]
- A prototype of the application has been created with the help of the Streamlit framework.
- :blue[**AMPL Python modules have been integrated into the program.**]
- Support for a HiGHS solver through AMPL Python modules has been implemented.
- A json file was used to formulate the input data.
- A Microsoft Excel was used as the input format, which provides extensive editing capabilities and allows for the validation of the input data.
- The Pandas and Numpy libraries were used for the analysis of the data.
- Extensive set of sample input data has been prepared as Excel files.
- The complete source code of Yumbo has been moved to GitHub as an open source project under the MIT license.
- A sophisticated reporting system was one of the requirements.
- To generate high quality professional plots and charts, the matplotlib library was chosen.
- Design and implementation of a sophisticated reporting system using the matplotlib library began.
- User-friendly customization of the generated charts has been added.
- To further customize the reporting system, a "Look and Fill" section has been added.
- The st.columns object from the Streamlit framework has been in heavy use.
- The testbed with increasing number of experts, tasks and constraints was prepared and run on Yumbo.
- For some use cases, memory consumption as high as 14 GiB has been observed in the pre-solve phase of the AMPL engine.
- The process of finding a model capable of finding a schedule with more than 3,000 experts, tasks, and constraints has begun.
- :blue[**A memory efficient mathematical model was designed and implemented.**]
- Two mathematical models with different profiles of memory usage have been introduced: one with and one without UBDAY constraints.
- The XBSUM and UBSUM constraints are not included in the mathematical model because they are rarely used in planning.
- Added support for three open source solvers HiGHS, GCG, SCIP via AMPL Python modules.
- The process of extensive testing with three solvers HiGHS, GCG, SCIP has begun.
- It has been observed that many use cases have more than one schedule with the same value of the objective function.
- The tests clearly showed that different solvers can produce different schedules with the same objective value.
- Report in Streamlit framework is divided into sections: Problem, Summary, Experts, Tasks, Statistics, Model.
- Further improvements to the reporting system were proposed and developed.
- Data processing has been optimized for speed by using vectorized versions of functions from the Pandas and NumPy libraries.
- Unified handling of the date data type by the Pandas library has been implemented.
- Date format as "%Y-%m-%d" was enforced.
- The program has been modularized and the modularization process has resulted in two sets of Python modules: img*, report*.
- For further visualization improvements, the st.tabs and st.pills objects from the Streamlit framework were used.
- :blue[**The Yumbo program is available as a WEB service on the Streamlit Community Cloud, https://yumbo-ampl.streamlit.app/.**]
- The mathematical model was extended by the introduction of "overflow tasks".
- The overflowing task model enabled us to create a schedule for tasks with insufficient number of assigned experts to complete the tasks on time.
- For performance reasons, the ax.bar function has been replaced by the ax.fill_between function from the matplotlib library.
- For matplotlib charts, the image compression process has been optimized by using the WebP file format instead of PNG.
- Session variables in the Streamlit framework were used to allow simultaneous multi-user program execution.
- Caching system in Streamlit framework was used to speed up the second time process of image generation.
- The hash of selected session variables was passed as a function argument to enforce correct caching system behavior in Streamlit.
- The hashlib.md5 was replaced with hashlib.blake2s.
- Convolution of sizes 7, 15, 21 has been implemented for the "Hours per day" chart in the summary section.
- Export of the entire schedule to a compressed CSV file is implemented.
- Further adjustment and refinement of the reporting system is required.
- :blue[**Yumbo solved the real case with 41 experts, 282 tasks, 423 assignments and 186 XBDAY constraints in less than 3 minutes on moderate CPU and generated a complete report without any problems.**]
- More complex and involved input cases have been prepared.
- The study of the behavior with the walking time has been under investigation.
- The statistics for reporting the running time are implemented.
- Validation of input data from Excel files has been implemented.
- The caching process of generated images and tables has been improved and simplified.
- Material icons have been used to improve the visual appeal of the reporting module.
- The input data file generator has been implemented as an Excel spreadsheet.

