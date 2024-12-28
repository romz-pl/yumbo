#
# The mathematical optimisation model that generates the schedule for a set of jobs.
# Authors: Zbigniew Romanowski and Paweł Koczyk
#
# Each job is defined by three integers: 
#   (1) the start of the job (i.e. the release date);
#   (2) the end of the job (i.e. the deadline);
#   (3) the duration of the job in hours;
#
# The PAYROLL constraints are defined for each defined payroll period.
# The constraint value V is the total number of working hours summed over all jobs and days in the period.
# Each payroll period is defined by four integers:
#   (1) the start of the payroll period;
#   (2) the end of the payroll period;
#   (3) the lower limit of the value V;
#   (4) the upper limit of the value V;
#
# The BOUND constraints are defined for intervals in the job.
# The bound value Q is the number of working hours per day on the specific job.
# Each constraint is defined by four integers:
#   (1) the start of the interval
#   (2) the end of the interval;
#   (3) the lower limit of the value Q;
#   (4) the upper limit of the value Q;
#


# The maximal total number of working hours per day
param HOURS_PER_DAY > 0 integer;

# Set of task names to be included in the schedule
set TASKN ordered;

# The set of tasks definition:
param TASKS{TASKN} >= 0 integer; # START
param TASKE{TASKN} >= 0 integer; # END
param TASKW{TASKN} >= 0 integer; # WORK

check {t in TASKN}:
    0 <= TASKS[t] <= TASKE[t];

check {t in TASKN}:
    0 <= TASKW[t];


# Set of expert names to be included in the schedule
set EXPERTN ordered;

# Set of payroll names
set PAYROLLN ordered;

# The set of payroll definition: START, END
param PAYROLLS{PAYROLLN} integer; # START
param PAYROLLE{PAYROLLN} integer; # END

check {k in PAYROLLN}:
    0 <= PAYROLLS[k] <= PAYROLLE[k];


set LINKS within {EXPERTN, TASKN};

set EXPPAY within {EXPERTN, PAYROLLN};

param PAYROLLBL {EXPPAY} integer, >= 0;
param PAYROLLBU {(e, p) in EXPPAY} integer, >= PAYROLLBL[e, p];


# Number of days to be investigated, i.e. time horizon
param DAY_NO = max( max{i in PAYROLLN} PAYROLLE[i], max{t in TASKN} TASKE[t] );


# The number of bounds for experts
param EBOUND_NO integer, >= 0;

# The set of bounds definition: EXPERT, START, END, LOWER, UPPER
param EBOUND{1..EBOUND_NO, 1..5} symbolic;

check {k in 1..EBOUND_NO}:
    EBOUND[k,1] in EXPERTN;

check {k in 1..EBOUND_NO}:
    1 <= EBOUND[k,2] <= EBOUND[k,3] <= DAY_NO;

check {k in 1..EBOUND_NO}:
    0 <= EBOUND[k,4] <= EBOUND[k,5] <= HOURS_PER_DAY;

param OFFDAY_NO integer, >= 0;

# Weekends and holidays
param OFFDAY{1..OFFDAY_NO} integer, >=1, <= DAY_NO;



# The number of bounds
param XBDAY_NO integer, >= 0;

# The set of bounds definition: EXPERT, TASK, DAY, LOWER, UPPER
param XBDAY{1..XBDAY_NO, 1..5} symbolic;

check {k in 1..XBDAY_NO}:
    XBDAY[k,1] in EXPERTN;
    
check {k in 1..XBDAY_NO}:
    XBDAY[k,2] in TASKN;

check {k in 1..XBDAY_NO}:
    TASKS[XBDAY[k,2]] <= XBDAY[k,3] <= TASKE[XBDAY[k,2]];

check {k in 1..XBDAY_NO}:
    0 <= XBDAY[k,4] <= XBDAY[k,5] <= HOURS_PER_DAY;
    


# The number of bounds
param XBSUM_NO integer, >= 0;

# The set of bounds definition: EXPERT, TASK, START, END, LOWER, UPPER
param XBSUM{1..XBSUM_NO, 1..6} symbolic;

check {k in 1..XBSUM_NO}:
    XBSUM[k,1] in EXPERTN;
    
check {k in 1..XBSUM_NO}:
    XBSUM[k,2] in TASKN;
    
check {k in 1..XBSUM_NO}:
    1 <= XBSUM[k,3] <= XBSUM[k,4] <= DAY_NO;
    
    
    

# The number of bounds
param UBDAY_NO integer, >= 0;

# The set of bounds definition: EXPERT, DAY, LOWER, UPPER
param UBDAY{1..UBDAY_NO, 1..4} symbolic;

check {k in 1..UBDAY_NO}:
    UBDAY[k,1] in EXPERTN;
    
check {k in 1..UBDAY_NO}:
    1 <= UBDAY[k,2] <= DAY_NO;
    
check {k in 1..UBDAY_NO}:
    0 <= UBDAY[k,3] <= UBDAY[k,3];





# The number of bounds
param UBSUM_NO integer, >= 0;

# The set of bounds definition: EXPERT, TASK, START, END, LOWER, UPPER
param UBSUM{1..UBSUM_NO, 1..6} symbolic;

check {k in 1..UBSUM_NO}:
    UBSUM[k,1] in EXPERTN;

check {k in 1..UBSUM_NO}:
    UBSUM[k,2] in TASKN;
    
check {k in 1..UBSUM_NO}:
    1 <= UBSUM[k,3] <= UBSUM[k,4] <= DAY_NO;
    
    
    


# For each expert, the cost for each task
var TASKDEV{EXPERTN, TASKN} >= 0;


# X[e, d, t] means the number of hours assigned to expert "e" on day "d" for task "t"
var X{EXPERTN, 1..DAY_NO, TASKN} integer, >=0, <= HOURS_PER_DAY;



#
#              | 0 iff X[e, d, t] = 0
# U[e, d, j] = |
#              | 1 iff X[e, d, t] => 1
#
var U{EXPERTN, 1..DAY_NO, TASKN} binary;


# Objective function. This function has the clear meaning, fortunatelly.
minimize objective_function:
    sum {e in EXPERTN, t in TASKN} TASKDEV[e, t];


# This is the part of the ojective function
subject to C_CD_minimization {e in EXPERTN, t in TASKN}:
    sum {d in TASKS[t]..TASKE[t]} ((d - TASKS[t])^(1/3)) * X[e, d, t] <= TASKDEV[e, t];


# Dates not within the job have values zero
subject to C_not_within {e in EXPERTN, t in TASKN, d in ({1..DAY_NO} diff {TASKS[t]..TASKE[t]})}:
    X[e, d, t] = 0;


subject to C_off {e in EXPERTN, t in TASKN, k in 1..OFFDAY_NO}:
   X[e, OFFDAY[k], t] = 0;


# The upper and lower limit on the total number of working hours in the payroll
subject to C_payroll {(e, i) in EXPPAY}:
    PAYROLLBL[e, i] <= sum {d in PAYROLLS[i]..PAYROLLE[i], (e, t) in LINKS} X[e, d, t] <= PAYROLLBU[e, i];


# The total number of working hours in the task
subject to C_task_work {t in TASKN}:
    sum {(e, t) in LINKS, d in TASKS[t]..TASKE[t]} X[e, d, t] = TASKW[t];


# The total number of working hours per day
subject to C_hours_per_day {e in EXPERTN, d in 1..DAY_NO}:
    sum {(e, t) in LINKS} X[e, d, t] <= HOURS_PER_DAY;


subject to C_xbday {k in 1..XBDAY_NO}:
    XBDAY[k,4] <= X[ XBDAY[k,1], XBDAY[k,3], XBDAY[k,2] ] <= XBDAY[k,5];
    
    
subject to C_xbsum {k in 1..XBSUM_NO}:
    XBSUM[k,5] <= sum {d in XBSUM[k,3]..XBSUM[k,4]} X[ XBSUM[k,1], d, XBSUM[k,2] ] <= XBSUM[k,6];


# The lower and upper bounds on the total number of working hours per day
subject to C_ebound {k in 1..EBOUND_NO, d in EBOUND[k,2]..EBOUND[k,3]}:
    EBOUND[k,4] <= sum{(e, t) in LINKS: e = EBOUND[k,1]} X[e, d, t] <= EBOUND[k,5];



# Constraint enforcing the value of U: lower bound
subject to C_use_lower {e in EXPERTN, d in 1..DAY_NO, t in TASKN}:
    U[e, d, t] <= X[e, d, t];


# Constraint enforcing the value of U: upper bound
subject to C_use_upper {e in EXPERTN, d in 1..DAY_NO, t in TASKN}:
    U[e, d, t] * HOURS_PER_DAY >= X[e, d, t];


subject to C_ubday {k in 1..UBDAY_NO}:
    UBDAY[k,3] <= sum { (e, t) in LINKS: e = UBDAY[k,1] } U[ e, UBDAY[k,2], t ] <= UBDAY[k,4];


subject to C_ubsum {k in 1..UBSUM_NO}:
    UBSUM[k,5] <= sum { d in UBSUM[k,3]..UBSUM[k,4] } U[ UBSUM[k,1], d, UBSUM[k,2] ] <= UBSUM[k,6];
