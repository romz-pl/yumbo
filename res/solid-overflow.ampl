#
# The mathematic optimisation model that generates the schedule
# for a set of tasks and a set of experts with many-to-many relations.
#
# Authors: Zbigniew Romanowski; Paweł Koczyk;
#
# Model: SOLID and OVERFLOW
#

# The maximal total number of working units per day
param MAXWORK integer, > 0;


# Set of task names to be included in the schedule
set TNAME;
check: card(TNAME) > 0;


# The scope of the task
set TSCOPE{TNAME} ordered within integer[1, Infinity];


# The work of a task:
param TWORK{TNAME} integer, >= 0;


# Set of expert names to be included in the schedule
set ENAME;
check: card(ENAME) > 0;


# Pairs of "expert name" and "task name"
set ASSIGN within {ENAME, TNAME};


# The set of XBDAY bounds
set XBID within integer[1, Infinity];       # ID
param XBEXPERT{XBID} symbolic within ENAME; # Expert
param XBTASK  {XBID} symbolic within TNAME; # Task
param XBS{j in XBID} integer, >= 1;         # START
param XBE{j in XBID} integer, >= XBS[j];    # END
param XBL{j in XBID} integer, >= 0;         # LOWER
param XBU{j in XBID} integer, >= XBL[j];    # UPPER


# Check XBDAY definition
check {j in XBID}:
    (XBEXPERT[j], XBTASK[j]) in ASSIGN;


# The set of EBDAY bounds for expert
set EBID within integer[1, Infinity];       # ID
param EBEXPERT{EBID} symbolic within ENAME; # Expert
param EBS{j in EBID} integer, >= 1;         # START
param EBE{j in EBID} integer, >= EBS[j];    # END
param EBL{j in EBID} integer, >= 0;         # LOWER
param EBU{j in EBID} integer, >= EBL[j];    # UPPER


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
var X{(e, t) in ASSIGN, TSCOPE[t]} integer, >= 0, <= MAXWORK;

# The overflow work for each task
var F{TNAME} integer, >= 0;


# Last day to be investigated, i.e. last day in the scope of each task
param LASTDAY = max{t in TNAME} last(TSCOPE[t]);


# The objective function.
# This function encourages the early completion of tasks.
minimize objective_function:
    sum {(e, t) in ASSIGN, d in TSCOPE[t]}
    ((d + 1 - first(TSCOPE[t]))^(1/3)) * X[e, t, d] +
    ((LASTDAY + 1)^(1/3)) * sum{t in TNAME} F[t];


# The total number of working hours per day
subject to C_maxwork {e in ENAME, d in union {t in TNAME: (e,t) in ASSIGN} TSCOPE[t] }:
    sum {(e, t) in ASSIGN} (if d in TSCOPE[t] then X[e, t, d] else 0)
    <= MAXWORK;


# The total number of working hours in the task
subject to C_work {t in TNAME}:
    sum {(e, t) in ASSIGN, d in TSCOPE[t]} X[e, t, d] + F[t]
    = TWORK[t];


# Constraines for number of hours
subject to C_xbday {j in XBID, d in (XBS[j]..XBE[j]) inter TSCOPE[ XBTASK[j] ] }:
    XBL[j] <=
    X[ XBEXPERT[j], XBTASK[j], d ]
    <= XBU[j];


# The upper and lower limit on the total number of working hours in the period
subject to C_period {(e, i) in EXPPER}:
    PBL[e, i] <=
    sum {d in PERS[i]..PERE[i], (e, t) in ASSIGN} (if d in TSCOPE[t] then X[e, t, d] else 0)
    <= PBU[e, i];
 

# The lower and upper bounds on the total number of working hours per day
subject to C_ebound {j in EBID, d in (EBS[j]..EBE[j]) inter (union {(EBEXPERT[j],t) in ASSIGN} TSCOPE[t]) }:
    EBL[j] <=
    sum{(e, t) in ASSIGN: e = EBEXPERT[j]} (if d in TSCOPE[t] then X[e, t, d] else 0)
    <= EBU[j];
