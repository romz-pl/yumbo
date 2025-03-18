# 📅 Yumbo. Schedules for Project Managers


As software engineers, we often deal with constraints, whether in system architecture, performance tuning, or algorithm design. But constraints also play a critical role in scheduling, especially for project managers (PMs) who juggle multiple tasks every day. This is where **Yumbo**, a powerful scheduling tool, comes into play.

One of the key constraints in Yumbo is **XBDAY**, which helps define the **lower and upper bounds** for a given expert-task pair on a given day. This constraint allows fine-grained control over scheduling by setting different limits for different date ranges. Whether a PM is managing a routine schedule or handling an exceptional case, XBDAY provides the flexibility to model virtually any scenario.



## Why does it matter?
In the domain of project management, the workload assigned to each task is frequently minimal, amounting to less than an hour per day, yet it accumulates over protracted periods. To address this, Yumbo employs **15-minute time units**, recognizing that a quarter of an hour constitutes a minimum reasonable time slot. Assuming an 8-hour workday and considering the minimum time allocation for each assigned task, a project manager could potentially complete up to 32 distinct tasks within an 8-hour workday. However, in real-world scenarios, the simplicity of this approach can quickly become unmanageable without the aid of XBDAY constraints.



## How to use XBDAY effectively?
A pragmatic approach to the organization of a project manager's schedule entails the initial calculation of the **mean daily workload** in hours. Subsequently, this value is rounded up to the nearest multiple of 15 minutes. The rounded value thus obtained serves as the upper limit for task duration, as delineated in the Excel input file utilized by Yumbo. This methodology enables teams to achieve an optimal balance between efficiency and realism, thereby preventing the occurrence of over-scheduling while concurrently maximizing productivity.

💡 Yumbo's assembler-like approach to schedule modeling enables organizations to dynamically **prototype**, **refine**, and **optimize** their workflows by leveraging constraints such as XBDAY. This approach ensures that professionals, whether engaged in the design of standard schedules or the management of unusual edge cases, can operate within well-defined and effective scheduling constraints.



🔗 Yumbo is available in two forms: as **source code** at https://github.com/romz-pl/yumbo and as **software as a service** on the Streamlit Community Cloud at https://yumbo-ampl.streamlit.app .


```
#OperationsResearch
#IntegerProgramming
#Scheduling
#Planning
#ProjectManagement
```

![Yumbo. Schedules for Project Managers](./img.webp)

Image created by ChatGPT.

