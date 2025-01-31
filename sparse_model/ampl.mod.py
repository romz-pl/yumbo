# Set of task names to be included in the schedule
set TASKN ordered;


set TASKD{TASKN};



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

set LINK within {EXPERTN, TASKN};


param BOUND{(e, t) in LINK, TASKD[t]} >= 0 integer;

param BBWW{t in TASKN, TASKD[t]} >= 0 integer;

# Objective function. This function has the clear meaning, fortunatelly.
#minimize objective_function:
#    sum {e in EXPERTN, t in TASKN} TASKDEV[e, t];


