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
    df = st.session_state.mprob["assign"].sort_values(["Expert", "Task"])

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
    df = st.session_state.mprob["xbday"].sort_values(["Expert", "Task"])
    holiday = set(st.session_state.mprob["holiday"]["Date"])  # Faster holiday lookups

    result = []
    for row in df.itertuples(index=False):
        # Generate business days and compute day differences.
        days = (pd.bdate_range(start=row.Start, end=row.End, freq="C", holidays=holiday) - today).days

        result.append(f"['{row.Expert}','{row.Task}',*]")

        # Pre-compute values used repeatedly for the current row.
        lower = row.Lower * quarters_in_hour
        upper = row.Upper * quarters_in_hour

        # Use list comprehension to extend the result list for each day.
        result.extend(f"{d} {lower} {upper}" for d in days)

    # Build the output string once and perform a single I/O write.
    output = "param:\nXBID: XBL XBU :=\n" + "\n".join(result) + "\n;\n\n"
    f.write(output)


def ubday(f):
    if not glb.with_ubday():
        return

    today = glb.today()
    df = st.session_state.mprob["ubday"].sort_values("Expert")
    holiday = set(st.session_state.mprob["holiday"]["Date"])

    result = []
    for row in df.itertuples(index=False):
        # Generate business days and compute day differences.
        days = (pd.bdate_range(start=row.Start, end=row.End, freq="C", holidays=holiday) - today).days

        result.append(f"['{row.Expert}',*]")


        # Use list comprehension to extend the result list for each day.
        result.extend(
            f"{d} {row.Lower} {row.Upper}" for d in days
        )

    # Build the output string once and perform a single I/O write.
    output = "param:\nUBID: UBL UBU :=\n" + "\n".join(result) + "\n;\n\n"
    f.write(output)




def ebday(f):
    today = glb.today()
    df = st.session_state.mprob["ebday"]
    result = [
        f"{id+1} '{row.Expert}' {(row.Start - today).days} "
        f"{(row.End - today).days} "
        f"{row.Lower * quarters_in_hour} "
        f"{row.Upper * quarters_in_hour}"
        for id, row in enumerate(df.itertuples(index=False))
    ]

    f.write("param:\nEBID: EBN EBS EBE EBL EBU :=\n")
    buf = "\n".join(result)
    f.write(buf)
    f.write("\n;\n\n")


def period(f):
    today = glb.today()
    df = st.session_state.mprob["period"].sort_values("Name")

    result = []
    expert = None
    for row in df.itertuples(index=False):
        start = (row.Start - today).days
        end = (row.End - today).days
        result.append(f"'{row.Name}' {start} {end}")

    output = "param:\nPNAME: PERS PERE :=\n" + "\n".join(result) + "\n;\n\n"
    f.write(output)


def pbsum(f):

    df = st.session_state.mprob["pbsum"].sort_values(["Expert", "Period"])
    result = []
    expert = None
    for row in df.itertuples(index=False):
        if expert != row.Expert:
            result.append(f"['{row.Expert}',*]")
            expert = row.Expert

        lower = row.Lower * quarters_in_hour
        upper = row.Upper * quarters_in_hour
        result.append(f"'{row.Period}' {lower} {upper}")

    output = "param:\nEXPPER: PBL PBU :=\n" + "\n".join(result) + "\n;\n\n"
    f.write(output)



def data_file():
    ff = tempfile.NamedTemporaryFile(mode='w+', prefix="yumbo-")

    ff.write(f'param MAXWORK := {glb.hours_per_day() * quarters_in_hour};\n\n')

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
    st.session_state.glb["ampl_data_file"] = ff.read()

    return ff


def save_schedule(ampl):
    # Create the index for the schedule DataFrame.
    days = pd.date_range(start=glb.tomorrow(), end=glb.last_day(), freq='D')

    # Build a dictionary where keys are (Expert, Task) tuples and values are the corresponding schedule Series.
    schedule_data = {}
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
        schedule_data[(row.Expert, row.Task)] = schedule.astype(np.float16) / quarters_in_hour

    # Create the full DataFrame at once, aligning on the given 'days' index.
    amplsol = pd.DataFrame(schedule_data, index=days).fillna(0)

    # Set a MultiIndex on the columns with names "Expert" and "Task".
    amplsol.columns = pd.MultiIndex.from_tuples(amplsol.columns, names=["Expert", "Task"])

    return amplsol


# activate AMPL license
def set_ampl_license():
    uuid = os.environ.get("AMPLKEY_UUID")
    if uuid is not None:
        modules.activate(uuid)


def solve():
    time_start = time.perf_counter()

    mm_hash = glb.math_model_hash(None)
    solver_output, amplsol = solve_ampl(mm_hash)
    st.session_state.glb["solver output"] = solver_output
    st.session_state.amplsol = amplsol
    st.session_state.glb["solver timestamp"] = pd.Timestamp.now().strftime("%d %B %Y, %H:%M:%S %p")

    time_end = time.perf_counter()
    st.session_state.stats["ampl:ttime"] += time_end - time_start


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

    if glb.with_ubday():
        ampl.read("./res/ampl-with-ubday.mod.py")
    else:
        ampl.read("./res/ampl.mod.py")

    ff = data_file()
    ampl.read_data(ff.name)
    ff.close()

@st.cache_resource(max_entries=99)
def solve_ampl(mm_hash):
    set_ampl_license()
    ampl = AMPL()
    set_ampl_options(ampl)
    set_model_and_data(ampl)

    # Capture solver output
    solver_output = ampl.get_output("solve;")

    # Check if solving was successful
    if ampl.solve_result != "solved":
        raise Exception(f"Failed to solve AMPL problem. AMPL returned flag: {ampl.solve_result}")

    amplsol = save_schedule(ampl)

    return solver_output, amplsol
