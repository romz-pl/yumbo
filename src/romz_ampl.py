from amplpy import AMPL, modules
import numpy as np
import os
import pandas as pd
import streamlit as st
import tempfile
import time
import uuid

import glb

quarters_in_hour = 4


def check_and_round(f):
    v = int(round(f))

    if abs(f - v) > 0.001:
        Exception(f"Invalid data in AMPL model")

    return v


def task(f):
    task = st.session_state.mprob["task"]

    # Compute the formatted rows using vectorized operations.
    # Multiply the Work column by quarters_in_hour and convert both columns to strings.
    formatted_rows = (
        "'" + task["Name"].astype(str) + "' " +
        (task["Work"] * quarters_in_hour).astype(str) + "\n"
    )

    # Write the header, the concatenated rows, and the footer.
    f.write("param:\nTNAME: TWORK :=\n")
    f.write(formatted_rows.str.cat(sep=""))
    f.write(";\n\n")


def tscope(f):
    today = glb.today()
    task_df = st.session_state.mprob["task"]
    # Using a set for fast membership checking
    holiday = set(st.session_state.mprob["holiday"]["Date"])

    output_lines = []
    for row in task_df.itertuples(index=False):
        # Compute the list of business day differences as a NumPy array.
        days = (pd.bdate_range(start=row.Start, end=row.End, freq='C', holidays=holiday) - today).days

        # Prepare header for the TSCOPE entry.
        header = f"set TSCOPE['{row.Name}'] :="
        output_lines.append(header)

        # Create chunks of 50 numbers per line.
        for i in range(0, len(days), 50):
            # Convert the slice of days to strings and join with a space.
            chunk = " ".join(map(str, days[i:i+50]))
            output_lines.append(chunk)

        # Append the terminating semicolon and a blank line.
        output_lines.append(";\n")

    # Write all lines at once.
    f.write("\n".join(output_lines))


def expert(f):
    ename = st.session_state.mprob["expert"]["Name"]
    output = (
        "\nset ENAME :=\n" +
        "\n".join(f"'{name}'" for name in ename) +
        "\n;\n\n"
    )
    f.write(output)


def assign(f):
    df = st.session_state.mprob["assign"]

    result = []
    expert = None
    for row in df.itertuples(index=False):
        if expert != row.Expert:
            result.append(f"('{row.Expert}',*)")
            expert = row.Expert
        result.append(f"'{row.Task}'")
    output = "set ASSIGN :=\n" + "\n".join(result) + "\n;\n\n"
    f.write(output)


def xbday(f):
    today = glb.today()
    df = st.session_state.mprob["xbday"]

    result = []
    for id, row in enumerate(df.itertuples(index=False), start=1):
        start = (row.Start - today).days
        end = (row.End - today).days
        lower = check_and_round(row.Lower * quarters_in_hour)
        upper = check_and_round(row.Upper * quarters_in_hour)
        result.append(f"{id} '{row.Expert}' '{row.Task}' {start} {end} {lower} {upper}")

    # Build the output string once and perform a single I/O write.
    output = "param:\nXBID: XBEXPERT XBTASK XBS XBE XBL XBU :=\n" + "\n".join(result) + "\n;\n\n"
    f.write(output)


def ubday(f):
    if not glb.is_ampl_model_ubday():
        return

    today = glb.today()
    df = st.session_state.mprob["ubday"]

    result = []
    for id, row in enumerate(df.itertuples(index=False), start=1):
        start = (row.Start - today).days
        end = (row.End - today).days
        lower = check_and_round(row.Lower * quarters_in_hour)
        upper = check_and_round(row.Upper * quarters_in_hour)
        result.append(f"{id} '{row.Expert}' {start} {end} {lower} {upper}")

    # Build the output string once and perform a single I/O write.
    output = "param:\nUBID: UBEXPERT UBS UBE UBL UBU :=\n" + "\n".join(result) + "\n;\n\n"
    f.write(output)



def ebday(f):
    today = glb.today()
    df = st.session_state.mprob["ebday"]

    result = []
    for id, row in enumerate(df.itertuples(index=False), start=1):
        start = (row.Start - today).days
        end = (row.End - today).days
        lower = check_and_round(row.Lower * quarters_in_hour)
        upper = check_and_round(row.Upper * quarters_in_hour)
        result.append(f"{id} '{row.Expert}' {start} {end} {lower} {upper}")

    # Build the output string once and perform a single I/O write.
    output = "param:\nEBID: EBEXPERT EBS EBE EBL EBU :=\n" + "\n".join(result) + "\n;\n\n"
    f.write(output)


def period(f):
    today = glb.today()
    df = st.session_state.mprob["period"]

    result = []
    expert = None
    for row in df.itertuples(index=False):
        start = (row.Start - today).days
        end = (row.End - today).days
        result.append(f"'{row.Name}' {start} {end}")

    output = "param:\nPNAME: PERS PERE :=\n" + "\n".join(result) + "\n;\n\n"
    f.write(output)


def pbsum(f):
    df = st.session_state.mprob["pbsum"]
    result = []
    expert = None
    for row in df.itertuples(index=False):
        if expert != row.Expert:
            result.append(f"['{row.Expert}',*]")
            expert = row.Expert

        lower = check_and_round(row.Lower * quarters_in_hour)
        upper = check_and_round(row.Upper * quarters_in_hour)
        result.append(f"'{row.Period}' {lower} {upper}")

    output = "param:\nEXPPER: PBL PBU :=\n" + "\n".join(result) + "\n;\n\n"
    f.write(output)


def create_data_file(ff):
    ff.write(
        f"# AMPL MODEL: {glb.get_ampl_model_file()}\n\n"
        f"# Timestamp: {pd.Timestamp.now().strftime('%d %B %Y, %H:%M:%S %p')}\n\n"
        f"param MAXWORK := {glb.hours_per_day() * quarters_in_hour};\n\n"
    )

    task(ff)
    tscope(ff)
    expert(ff)
    assign(ff)
    xbday(ff)
    ubday(ff)
    ebday(ff)
    period(ff)
    pbsum(ff)

    ff.seek(0)
    data = ff.read()
    ff.seek(0)
    #st.write(ampl_data_file)

    return data


def save_schedule(ampl):
    # Build a dictionary where keys are (Expert, Task) tuples and values are the corresponding schedule Series.
    schedule_dict = {}
    for row in st.session_state.mprob["assign"].itertuples(index=False):
        # Retrieve the schedule series from AMPL.
        schedule = (
            ampl.get_data(f"{{d in TSCOPE['{row.Task}']}} X['{row.Expert}', '{row.Task}', d]")
            .to_pandas()
            .iloc[:, 0]
        )
        # Adjust the schedule index to actual dates.
        schedule.index = pd.to_datetime(glb.today()) + pd.to_timedelta(schedule.index, unit='D')

        # Convert values to np.float16 and apply scaling.
        schedule_dict[(row.Expert, row.Task)] = schedule.astype(np.float16) / quarters_in_hour

    # Create the index for the schedule DataFrame.
    days = pd.date_range(start=glb.tomorrow(), end=glb.last_day(), freq='D')

    # Create the full DataFrame at once, aligning on the given 'days' index.
    df = pd.DataFrame(schedule_dict, index=days).fillna(0)

    # Set a MultiIndex on the columns with names "Expert" and "Task".
    df.columns = pd.MultiIndex.from_tuples(df.columns, names=["Expert", "Task"])

    return df


def save_overflow(ampl):
    if not glb.is_ampl_model_overflow():
        return pd.Series()


    # Retrieve the overflow series from AMPL.
    overflow = (
        ampl.get_data(f"{{t in TNAME}} F[t]")
        .to_pandas()
        .iloc[:, 0]
    )

    # Convert values to np.float16 and apply scaling.
    overflow = overflow.astype(np.float16) / quarters_in_hour
    overflow.index.name = 'Task'
    overflow.name='Overflow'

    return overflow


# activate AMPL license
def set_ampl_license():
    uuid = os.environ.get("AMPLKEY_UUID")
    if uuid is not None:
        modules.activate(uuid)


def set_ampl_options(ampl):
    ampl.set_option('presolve', 10)
    ampl.set_option('show_stats', 7);
    # ampl.set_option('times', 1);

    solver = st.session_state.mprob["misc"].iloc[0]["Solver"]
    ampl.set_option("solver", solver)

    # Set solver-specific options
    solver_options = {
        "highs": "outlev=1",
        "gcg": "tech:outlev-native=4",
        "scip": "tech:outlev-native=5",
    }

    if solver in solver_options:
        ampl.option[f"{solver}_options"] = solver_options[solver]



def set_model_and_data(ampl):
    # Change directory to AMPL's working directory
    ampl.cd(os.path.dirname(os.path.dirname(__file__)))

    model_file = glb.get_ampl_model_file()
    ampl.read(model_file)

    # Temporary file is required for storing AMPL data file
    ff = tempfile.NamedTemporaryFile(mode='w+', prefix="yumbo-")

    ampl_data_file = create_data_file(ff)
    ampl.read_data(ff.name)
    ff.close()

    return ampl_data_file


# @st.cache_resource(max_entries=99)
def solve_ampl(mm_hash):
    set_ampl_license()
    ampl = AMPL()
    set_ampl_options(ampl)
    ampl_data_file = set_model_and_data(ampl)

    # Capture solver log
    solver_log = ampl.get_output("solve;")

    # Check if solving was successful
    if ampl.solve_result != "solved":
        raise Exception(f"Failed to solve AMPL problem. AMPL returned flag: {ampl.solve_result}")

    schedule = save_schedule(ampl)
    overflow = save_overflow(ampl)

    return ampl_data_file, solver_log, schedule, overflow


def solve():
    time_start = time.perf_counter()

    mm_hash = st.session_state.mm_hash
    ampl_data_file, solver_log, schedule, overflow = solve_ampl(mm_hash)

    st.session_state.mprob["ampl_data_file"] = ampl_data_file

    st.session_state.schedule = schedule
    st.session_state.overflow = overflow

    st.session_state.stats["solver_log"] = solver_log
    st.session_state.stats["solver_timestamp"] = pd.Timestamp.now().strftime("%d %B %Y, %H:%M:%S %p")

    time_end = time.perf_counter()
    st.session_state.stats["ampl:ttime"] += time_end - time_start
