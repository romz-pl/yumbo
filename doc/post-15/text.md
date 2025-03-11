# 📅 Yumbo. Expert Availability and Preferences


In complex scheduling environments where experts are assigned to multiple tasks, managing their availability is a critical factor in achieving realistic schedules. The Yumbo scheduling tool addresses this challenge by incorporating **EBDAY constraints**, an essential input parameter that defines expert availability on a daily basis.

By default, Yumbo assumes a standard workday of **8 hours per day**. However, real-world scenarios often involve deviations from this assumption:
- Experts may be **unavailable** due to vacations, holidays, or personal reasons.
- Experts may have **partial availability**, working less than 8 hours per day due to training, part-time employment, or unforeseen commitments.

The EBDAY constraint allows organizations to **effectively model these variations**. Defined in Yumbo's Excel input file, this constraint specifies expert availability per day within a given date range. Because the granularity of the EBDAY constraint is as small as a quarter of an hour, it provides a high level of flexibility without adding unnecessary complexity.



## How does this affect scheduling?
- **Realistic resource allocation:** EBDAY integration ensures that only available experts are assigned to tasks, reducing scheduling inaccuracies.
- **Dynamic Adjustments:** As time passes and the business evolves, regularly updating the schedule with new EBDAY values allows for seamless adaptation to changes in expert availability.
- **Proactive Risk Management:** Yumbo flags potential **task overflows** - instances where an assigned expert does not have enough hours to complete a task. This feature provides insight into the need for additional resources to ensure timely project completion.



💡 Yumbo's scheduling process is designed for **speed and adaptability**. Because the time it takes to create a new schedule is short, it is a good idea to update your availability constraints frequently. This practice helps companies to incorporate the latest availability of experts and to maintain realistic schedules that are free of conflicts.


🔗 For those looking to improve the operational efficiency of staff scheduling, Yumbo is available as **open source** software on GitHub https://github.com/romz-pl/yumbo/ and as a **SaaS solution** via the Streamlit Community Cloud https://yumbo-ampl.streamlit.app/ .



```
#OperationsResearch
#IntegerProgramming
#Scheduling
#Planning
#ProjectManagement
```

![Yumbo. Expert Availability and Preferences](./img.webp)

Image created by ChatGPT.

