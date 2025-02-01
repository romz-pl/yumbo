#
# The mathematical optimisation model that generates the schedule for a set of tasks.
# Authors: Zbigniew Romanowski and Paweł Koczyk
#
# A set of tasks is defined, with each task characterised by three properties:
#    (a) the start date;
#    (b) the end date;
#    (c) the work expressed in hours.
#
# Each task in the set is assigned to at least one expert, and an expert can be assigned to one or more tasks.
# Consequently, there is a many-to-many relationship between tasks and experts.
# 
# It is possible to pefine constrains to change the default behaviour.
# Constraints are further categorised into four classes, each of which is optional.
# The objective is to determine the expert's daily schedule that satisfies the following constraints:
#    - The number of hours worked per day must not exceed the limit.
#    - For each call period, the total number of hours worked must be within the limit.
#    - For each day, for each task, the number of hours worked per day must be within the limit.
#    - For an expert, the number of hours worked per day must be within the limit for each day.
#
#

# The maximal total number of working units per day
param MAXWORK integer, > 0;


# Set of task names to be included in the schedule
set TNAME;


# The scope of the task
set TSCOPE{TNAME} ordered;


# The work of a task:
param TWORK{TNAME} integer, >= 0;


# Set of expert names to be included in the schedule
set ENAME;


# Pairs of "expert name" and "task name"
set EXPTAS within {ENAME, TNAME};


# The set of XBDAY bounds ("expert", "task") pair
set XBID within {(e, t) in EXPTAS, TSCOPE[t]}; # ID
param XBL{XBID}, >= 0; # LOWER
param XBU{(e, t, d) in XBID} integer, >= XBL[e, t, d]; # UPPER


# The set of EBDAY bounds for expert
set EBID; # ID
param EBN{EBID} symbolic within ENAME;
param EBS{EBID} integer, >= 1; # START
param EBE{j in EBID} integer, >= EBS[j]; # END
param EBL{EBID} integer, >= 0; # LOWER
param EBU{j in EBID} integer, >= EBL[j]; # UPPER


# Set of period names
set PNAME;


# The set of period definition
param PERS{PNAME} integer, >= 0; # START
param PERE{k in PNAME} integer, >= PERS[k]; # END


# Pairs of "expert name" and "period name"
set EXPPER within {ENAME, PNAME};


# The set of PBSUM bounds for ("expert", "period") pair
param PBL {EXPPER} integer, >= 0; # LOWER
param PBU {(e, p) in EXPPER} integer, >= PBL[e, p]; # UPPER


# X[e, t, d] means the number of hours assigned to expert "e" for task "t" on day "d" 
var X{(e, t) in EXPTAS, TSCOPE[t]} integer, >= 0, <= MAXWORK;


# The objective function.
# This function encourages the early completion of tasks.
minimize objective_function:
    sum {(e, t) in EXPTAS, d in TSCOPE[t]} ((d + 1 - first(TSCOPE[t]))^(1/3)) * X[e, t, d];


# The total number of working hours per day
subject to C_maxwork {e in ENAME, d in union {t in TNAME: (e,t) in EXPTAS} TSCOPE[t] }:
    sum {(e, t) in EXPTAS} (if d in TSCOPE[t] then X[e, t, d] else 0) <= MAXWORK;


# The total number of working hours in the task
subject to C_work {t in TNAME}:
    sum {(e, t) in EXPTAS, d in TSCOPE[t]} X[e, t, d] = TWORK[t];


# Constraines for number of hours
subject to C_xbday {(e, t, d) in XBID}:
    XBL[e, t, d] <= X[e, t, d ] <= XBU[e, t, d];


# The upper and lower limit on the total number of working hours in the period
subject to C_period {(e, i) in EXPPER}:
    PBL[e, i] <=
    sum {d in PERS[i]..PERE[i], (e, t) in EXPTAS} (if d in TSCOPE[t] then X[e, t, d] else 0)
    <= PBU[e, i];
 

# The lower and upper bounds on the total number of working hours per day
subject to C_ebound {j in EBID, d in (EBS[j]..EBE[j]) inter (union {(EBN[j],t) in EXPTAS} TSCOPE[t]) }:
    EBL[j] <=
    sum{(e, t) in EXPTAS: e = EBN[j]} (if d in TSCOPE[t] then X[e, t, d] else 0)
    <= EBU[j];
