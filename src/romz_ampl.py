from amplpy import AMPL, modules
import datetime
import glb
import numpy as np
import os
import pandas as pd
import streamlit as st
import time
import uuid

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
    df = st.session_state.mprob["assign"]
    # Build the formatted string for each (expert, task) pair.
    formatted_pairs = "\n".join(
        f"'{expert}' '{task}'"
        for expert, task in zip(df["Expert"], df["Task"])
    )
    # Build the complete output string.
    output = f"set ASSIGN :=\n{formatted_pairs}\n;\n\n"
    f.write(output)


def xbday(f):
    today = glb.today()
    df = st.session_state.mprob["xbday"]
    holiday = set(st.session_state.mprob["holiday"]["Date"])  # Faster holiday lookups

    result = []
    for row in df.itertuples(index=False):
        # Generate business days and compute day differences.
        days = (pd.bdate_range(start=row.Start, end=row.End, freq="C", holidays=holiday) - today).days

        # Pre-compute values used repeatedly for the current row.
        lower = row.Lower * quarters_in_hour
        upper = row.Upper * quarters_in_hour

        # Use list comprehension to extend the result list for each day.
        result.extend(
            f"'{row.Expert}' '{row.Task}' {d} {lower} {upper}" for d in days
        )

    # Build the output string once and perform a single I/O write.
    output = "param:\nXBID: XBL XBU :=\n" + "\n".join(result) + "\n;\n\n"
    f.write(output)


def ubday():
    assert False
    # today = glb.today()
    # df = st.session_state.mprob["ubday"]
    # holiday = set(st.session_state.mprob["holidays"]["Date"])

    # result = []
    # for row in df.itertuples(index=False):
    #     # Generate business days and compute day differences.
    #     days = (pd.bdate_range(start=row.Start, end=row.End, freq="C", holidays=holiday) - today).days

    #     # Pre-compute values used repeatedly for the current row.
    #     lower = row.Lower * quarters_in_hour
    #     upper = row.Upper * quarters_in_hour

    #     # Use list comprehension to extend the result list for each day.
    #     result.extend(
    #         f"'{row.Expert}' '{row.Task}' {d} {lower} {upper}" for d in days
    #     )

    # # Build the output string once and perform a single I/O write.
    # output = "param:\nXBID: XBL XBU :=\n" + "\n".join(result) + "\n;\n\n"
    # f.write(output)




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
    df = st.session_state.mprob["period"]

    # Vectorized computation of day differences
    start_days = (df["Start"] - today).dt.days.astype(str)
    end_days = (df["End"] - today).dt.days.astype(str)
    names = df["Name"].astype(str)

    # Vectorized string construction for each row
    result = ("'" + names + "' " + start_days + " " + end_days).to_list()

    # Build the complete output and write it in one call
    output = "param:\nPNAME: PERS PERE :=\n" + "\n".join(result) + "\n;\n\n"
    f.write(output)


def pbsum(f):
    df = st.session_state.mprob["pbsum"]
    # Build the formatted strings using vectorized operations.
    formatted = (
        "'" + df["Expert"].astype(str) + "' '" +
        df["Period"].astype(str) + "' " +
        (df["Lower"] * quarters_in_hour).astype(str) + " " +
        (df["Upper"] * quarters_in_hour).astype(str)
    )

    # Concatenate the header, the formatted lines, and the footer.
    output = "param:\nEXPPER: PBL PBU :=\n" + "\n".join(formatted) + "\n;\n\n"
    f.write(output)


def data_file(name):
    random_uuid = uuid.uuid4()
    # ampl_data_file = f"./ampl-translated-from-excel/{name}-{random_uuid}.dat"
    ampl_data_file = f"./ampl-translated-from-excel/{name}.dat"
    with open(ampl_data_file, 'w') as f:
        f.write(f'param MAXWORK := {glb.hours_per_day() * quarters_in_hour};\n\n')

        task(f)
        tscope(f)
        expert(f)
        assign(f)
        xbday(f)
        # ubday(f)
        ebday(f)
        period(f)
        pbsum(f)

    return ampl_data_file



def save_schedule(ampl):
    #today = glb.today()
    assign_df = st.session_state.mprob["assign"]
    # task_df = st.session_state.mprob["task"]

    # day_no = int(ampl.get_data("DAY_NO").to_pandas().iloc[0, 0])
    # days = pd.date_range(start=today + pd.Timedelta(days=1), periods=day_no, freq='D')

    # holiday = set(st.session_state.mprob["holiday"]["Date"])

    #sol = ampl.get_solution(flat=True, zeros=True)

    #for key, value in sol.items():
    #    st.write(type(key), type(value))

    # Get the variable object for 'x'
    #x_var = ampl.getVariable("X")

    # Retrieve the solution values as an amplpy DataFrame (which you can also convert to a pandas DataFrame)
    #x_values = x_var.getValues()

    # Optionally convert to a pandas DataFrame for further processing
    #x_df = x_values.toPandas()
    #st.write(x_df)

    #level0 = ["bar", "bar", "baz", "baz", "foo", "foo", "qux", "qux"]
    #level1 = ["one", "two", "one", "two", "one", "two", "one", "two"]







    days = pd.date_range(start=glb.tomorrow(), end=glb.last_day(), freq='D')
    amplsol = pd.DataFrame(index=days)

    level0 = []
    level1 = []

    for row in assign_df.itertuples(index=False):
        level0.append(row.Expert)
        level1.append(row.Task)

        # schedule = ampl.get_data(f"{{d in 1..DAY_NO}} X['{row.Expert}', '{row.Task}', d]").to_pandas().iloc[:, 0]
        #schedule = ampl.get_data(f"X['{row.Expert}', '{row.Task}']")
        #st.write(schedule)


        schedule = ampl.get_data(f"{{d in TSCOPE['{row.Task}']}} X['{row.Expert}', '{row.Task}', d]").to_pandas().iloc[:, 0]
        # st.write(type(schedule))
        #st.write(schedule.to_list(skip_index=True))
        # st.write(schedule.to_pandas().iloc[:, 0])
        # schedule.columns = ["X"]
        # st.write(schedule.columns)

        # st.write(schedule.index)
        # schedule.index = glb.today() + schedule.index

        schedule.index = pd.to_datetime(glb.today()) + pd.to_timedelta(schedule.index, unit='D')

        amplsol[f"{row.Expert};{row.Task}"] = schedule.astype(np.float16) / quarters_in_hour
        # st.write(sol.dtypes)



        # # Create DataFrame from fetched data
        # df = pd.DataFrame(schedule, dtype=np.float16) / quarters_in_hour
        # task_start = task_df[task_df["Name"] == row.Task]["Start"].iloc[0]
        # task_end = task_df[task_df["Name"] == row.Task]["End"].iloc[0]
        # # st.write(task_start, task_end)

        # df.index = pd.bdate_range(start=task_start, end=task_end, freq='C', holidays=holiday)
        # df.columns = ["X"]
        # st.write(df)
        # all_schedules[(f"{row.Expert}", f"{row.Task}")] = df

    amplsol = amplsol.fillna(0)
    #st.write(amplsol)

    tuples = list(zip(level0, level1))
    twoLevelIndex = pd.MultiIndex.from_tuples(tuples, names=["Expert", "Task"])
    #st.write(twoLevelIndex.get_level_values(0))
    #st.write(twoLevelIndex.get_level_values(1))

    amplsol.columns = twoLevelIndex

    # st.write(amplsol["DEV.Jarosław"])
    #st.write(amplsol.xs("DEV.Jarosław", level="Expert", axis=1))
    #st.write(amplsol.xs("DEV.p18.m", level="Task", axis=1))
    # st.markdown(amplsol.to_html(), unsafe_allow_html=True)

    return amplsol



# activate AMPL license
def set_ampl_license():
    uuid = os.environ.get("AMPLKEY_UUID")
    if uuid is not None:
        modules.activate(uuid)


def solve(uploaded_file):
    time_start = time.perf_counter()

    ampl_output, amplsol = solve_ampl(uploaded_file.name, uploaded_file.getvalue())
    st.session_state.amplsol = amplsol
    st.session_state.glb["solver output"] = ampl_output
    st.session_state.glb["solver timestamp"] = datetime.datetime.now().strftime("%d %B %Y, %H:%M:%S %p")

    time_end = time.perf_counter()
    st.session_state.glb["time:ampl:ttime"] += time_end - time_start

    # st.write(st.session_state.amplsol)


# @st.cache_resource(max_entries=99)
def solve_ampl(name, file_data):
    set_ampl_license()
    ampl = AMPL()

    # Customise AMPL run
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

    # Change directory to AMPL's working directory
    ampl.cd(os.path.dirname(os.path.dirname(__file__)))

    ampl.read("./res/ampl.mod.py")
    file = data_file(name)
    ampl.read_data(file)

    # Capture solver output
    ampl_output = ampl.get_output("solve;")

    # Check if solving was successful
    if ampl.solve_result != "solved":
        raise Exception(f"Failed to solve AMPL problem. AMPL returned flag: {ampl.solve_result}")

    amplsol = save_schedule(ampl)
    return ampl_output, amplsol

