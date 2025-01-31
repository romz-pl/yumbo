
# The maximal total number of working hours per day
param HOURS_PER_DAY integer, > 0;

# Set of task names to be included in the schedule
set TNAME;

# The scope of the task
set TSCOPE{TNAME} ordered;

# The work of a task:
param TWORK{TNAME} integer, >= 0;

# Set of expert names to be included in the schedule
set ENAME;

set LINK within {ENAME, TNAME};

# The set of XBDAY bounds definition
set XBID within {(e, t) in LINK, TSCOPE[t]}; # ID
param XBL{XBID}, >= 0; # LOWER
param XBU{(e, t, d) in XBID} integer, >= XBL[e, t, d]; # UPPER

# The set of bounds for EXPERT
set EBID; # ID
param EBN{EBID} symbolic within ENAME;
param EBS{EBID} integer, >= 1; # START
param EBE{j in EBID} integer, >= EBS[j]; # END
param EBL{EBID} integer, >= 0; # LOWER
param EBU{j in EBID} integer, >= EBL[j]; # UPPER


# Set of payroll names
set PAYROLLN ordered;

# The set of payroll definition: START, END
param PAYROLLS{PAYROLLN} integer, >= 0;
param PAYROLLE{k in PAYROLLN} integer, >= PAYROLLS[k];


set EXPPAY within {ENAME, PAYROLLN};

param PAYROLLBL {EXPPAY} integer, >= 0;
param PAYROLLBU {(e, p) in EXPPAY} integer, >= PAYROLLBL[e, p];


# X[e, t, d] means the number of hours assigned to expert "e" for task "t" on day "d" 
var X{(e, t) in LINK, TSCOPE[t]} integer, >= 0, <= HOURS_PER_DAY;

# Objective function.
# This function encourages the early completion of tasks.
minimize objective_function:
    sum {(e, t) in LINK, d in TSCOPE[t]} ((d + 1 - first(TSCOPE[t]))^(1/3)) * X[e, t, d];


# The total number of working hours per day
subject to C_hours_per_day {e in ENAME, d in union {t in TNAME: (e,t) in LINK} TSCOPE[t] }:
    sum {(e, t) in LINK} (if d in TSCOPE[t] then X[e, t, d] else 0) <= HOURS_PER_DAY;

# The total number of working hours in the task
subject to C_work {t in TNAME}:
    sum {(e, t) in LINK, d in TSCOPE[t]} X[e, t, d] = TWORK[t];

# Constraines for number of hours
subject to C_xbday {(e, t, d) in XBID}:
    XBL[e, t, d] <= X[e, t, d ] <= XBU[e, t, d];


# The upper and lower limit on the total number of working hours in the payroll
subject to C_payroll {(e, i) in EXPPAY}:
    PAYROLLBL[e, i] <=
    sum {d in PAYROLLS[i]..PAYROLLE[i], (e, t) in LINK} (if d in TSCOPE[t] then X[e, t, d] else 0)
    <= PAYROLLBU[e, i];
 

# The lower and upper bounds on the total number of working hours per day
subject to C_ebound {j in EBID, d in (EBS[j]..EBE[j]) inter (union {(EBN[j],t) in LINK} TSCOPE[t]) }:
    EBL[j] <=
    sum{(e, t) in LINK: e = EBN[j]} (if d in TSCOPE[t] then X[e, t, d] else 0)
    <= EBU[j];
