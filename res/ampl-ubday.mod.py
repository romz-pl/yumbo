#
# The mathematic optimisation model that generates the schedule
# for a set of tasks and a set of experts with many-to-many relations.
#
# Authors: Zbigniew Romanowski; Paweł Koczyk;
#
# Model: UBDAY
#

# The maximal total number of working units per day
param MAXWORK integer, > 0;


# Set of task names to be included in the schedule
set TNAME;
check: card(TNAME) > 0;


# The scope of the task
set TSCOPE{TNAME} ordered;


# The work of a task:
param TWORK{TNAME} integer, >= 0;


# Set of expert names to be included in the schedule
set ENAME;
check: card(ENAME) > 0;


# Pairs of "expert name" and "task name"
set ASSIGN within {ENAME, TNAME};


# The set of XBDAY bounds
set XBID within {(e, t) in ASSIGN, TSCOPE[t]}; # ID
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


# Number of days to be investigated, i.e. time horizon
param DAYNO = max( max{i in PNAME} PERE[i], max{t in TNAME} TWORK[t] );


# The set of UBDAY bounds
set UBID within {ENAME, 1..DAYNO}; # ID
param UBL{UBID}, >= 0; # LOWER
param UBU{(e, d) in UBID} integer, >= UBL[e, d]; # UPPER


# X[e, t, d] means the number of hours assigned to expert "e" for task "t" on day "d" 
var X{(e, t) in ASSIGN, TSCOPE[t]} integer, >= 0, <= MAXWORK;


#
#              | 0 iff X[e, t, d] = 0
# U[e, t, d] = |
#              | 1 iff X[e, t, d] => 1
#
var U{(e, t) in ASSIGN, TSCOPE[t]} binary;


# The objective function.
# This function encourages the early completion of tasks.
minimize objective_function:
    sum {(e, t) in ASSIGN, d in TSCOPE[t]} ((d + 1 - first(TSCOPE[t]))^(1/3)) * X[e, t, d];


# The total number of working hours per day
subject to C_maxwork {e in ENAME, d in union {t in TNAME: (e,t) in ASSIGN} TSCOPE[t] }:
    sum {(e, t) in ASSIGN} (if d in TSCOPE[t] then X[e, t, d] else 0) <= MAXWORK;


# The total number of working hours in the task
subject to C_work {t in TNAME}:
    sum {(e, t) in ASSIGN, d in TSCOPE[t]} X[e, t, d] = TWORK[t];


# Constraines for number of hours
subject to C_xbday {(e, t, d) in XBID}:
    XBL[e, t, d] <= X[e, t, d ] <= XBU[e, t, d];


# The upper and lower limit on the total number of working hours in the period
subject to C_period {(e, i) in EXPPER}:
    PBL[e, i] <=
    sum {d in PERS[i]..PERE[i], (e, t) in ASSIGN} (if d in TSCOPE[t] then X[e, t, d] else 0)
    <= PBU[e, i];
 

# The lower and upper bounds on the total number of working hours per day
subject to C_ebound {j in EBID, d in (EBS[j]..EBE[j]) inter (union {(EBN[j],t) in ASSIGN} TSCOPE[t]) }:
    EBL[j] <=
    sum{(e, t) in ASSIGN: e = EBN[j]} (if d in TSCOPE[t] then X[e, t, d] else 0)
    <= EBU[j];


# Constraint enforcing the value of U: lower bound
subject to C_use_lower {(e, t) in ASSIGN, d in TSCOPE[t]}:
    U[e, t, d] <= X[e, t, d];


# Constraint enforcing the value of U: upper bound
subject to C_use_upper {(e, t) in ASSIGN, d in TSCOPE[t]}:
    U[e, t, d] * MAXWORK >= X[e, t, d];


# The lower and upper bounds on the number of tasks per day
subject to C_ubday {(e, d) in UBID}:
    UBL[e, d] <=
    sum {(e, t) in ASSIGN} (if d in TSCOPE[t] then U[e, t, d] else 0)
    <= UBU[e, d];
