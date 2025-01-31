
# The maximal total number of working hours per day
param HOURS_PER_DAY > 0 integer;

# Set of task names to be included in the schedule
set TASKN;

# The scope of each task
set SCOPE{TASKN} ordered;

# The work of a task:
param WORK{TASKN} integer, >= 0;



# Set of expert names to be included in the schedule
set EXPERTN ordered;

set LINK within {EXPERTN, TASKN};

set XBDAY within {(e, t) in LINK, SCOPE[t]};

# The set of bounds definition: LOWER, UPPER
param XBL{XBDAY};
param XBU{XBDAY};


# X[e, t, d] means the number of hours assigned to expert "e" for task "t" on day "d" 
var X{(e, t) in LINK, SCOPE[t]} integer, >= 0, <= HOURS_PER_DAY;

# Objective function.
# This function encourages the early completion of tasks.
minimize objective_function:
    sum {(e, t) in LINK, d in SCOPE[t]} ((d + 1 - first(SCOPE[t]))^(1/3)) * X[e, t, d];


# The total number of working hours per day
subject to C_hours_per_day {e in EXPERTN, d in union {t in TASKN: (e,t) in LINK} SCOPE[t] }:
    sum {(e, t) in LINK} (if d in SCOPE[t] then X[e, t, d] else 0) <= HOURS_PER_DAY;

# The total number of working hours in the task
subject to C_work {t in TASKN}:
    sum {(e, t) in LINK, d in SCOPE[t]} X[e, t, d] = WORK[t];

# Constraines for number of hours
subject to C_xbday {(e, t, d) in XBDAY}:
    XBL[e, t, d] <= X[e, t, d ] <= XBU[e, t, d];

 
