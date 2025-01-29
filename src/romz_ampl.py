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

def tasks():
    today = glb.today()
    df = st.session_state.glb["tasks"]

    # Calculate start and end days relative to today
    df["Start Relative"] = (df["Start"] - today).dt.days
    df["End Relative"] = (df["End"] - today).dt.days

    # Use vectorized string formatting for better performance
    formatted_rows = df.apply(
        lambda row: f"'{row['Name']}' {row['Start Relative']} {row['End Relative']} "
        f"{row['Work'] * quarters_in_hour}\n",
        axis=1,
    )

    df.drop(columns=["Start Relative", "End Relative"], inplace=True)

    return ''.join(formatted_rows)


def offday():
    today = glb.today()
    # Determine the date range
    min_date = st.session_state.glb["tasks"]["Start"].min()
    max_date = st.session_state.glb["tasks"]["End"].max()

    # Generate weekends within the range using a mask for Saturdays and Sundays
    weekends = pd.bdate_range(start=min_date, end=max_date, freq='C', weekmask='Sat Sun')
    holidays = st.session_state.glb["public holidays"]["Date"]

    # Combine weekends and holidays into a sorted list
    # The set off_days is the union of weekends and holidays.
    # Sorting is not necessary. However, it does give deterministic (repetitive) results.
    off_days = sorted(set(weekends.union(holidays)))

    # Create the result buffer
    buf = "\n".join(f"{idx + 1} {(day - today).days}" for idx, day in enumerate(off_days))

    return len(off_days), buf


def xbday():
    today = glb.today()
    # Preprocessing for efficient lookups
    df = st.session_state.glb["xbday"]
    df_tasks = st.session_state.glb["tasks"].set_index("Name")  # Set "Name" as index for quick task lookup
    holidays = set(st.session_state.glb["public holidays"]["Date"])  # Convert holidays to a set for faster checks

    result = []
    id_counter = 0

    # Iterate efficiently using itertuples
    for row in df.itertuples(index=False):
        task_name = row.Task
        expert_name = row.Expert
        lower = row.Lower * quarters_in_hour
        upper = row.Upper * quarters_in_hour

        # Calculate valid date range considering task bounds and xbday range
        task_start, task_end = df_tasks.loc[task_name, ["Start", "End"]]
        range_start = max(row.Start, task_start)
        range_end = min(row.End, task_end)
        # Generate business days using pandas
        valid_days = pd.bdate_range(
            start=range_start,
            end=range_end,
            freq="C",
            holidays=holidays,
            weekmask="Mon Tue Wed Thu Fri"
        )

        # Process valid days
        for d in valid_days:
            day_offset = (d - today).days
            id_counter += 1
            result.append(f"{id_counter} '{expert_name}' '{task_name}' {day_offset} {lower} {upper}")

    # Combine results into a single string and return
    return id_counter, "\n".join(result)




def xbsum():
    today = glb.today()
    df = st.session_state.glb["xbsum"]
    result = []

    # Iterate over rows using itertuples for better performance
    for idx, row in enumerate(df.itertuples(index=False), start=1):
        expert = row.Expert
        task = row.Task
        start = (row.Start - today).days
        end = (row.End - today).days
        lower = row.Lower * quarters_in_hour
        upper = row.Upper * quarters_in_hour

        # Append formatted string to result list
        result.append(f"{idx} '{expert}' '{task}' {start} {end} {lower} {upper}")

    # Join the result list with newline characters
    return len(result), "\n".join(result)


def ubday():
    today = glb.today()
    df = st.session_state.glb["ubday"]
    holidays = set(st.session_state.glb["public holidays"]["Date"])

    result = []
    id = 0

    for row in df.itertuples(index=False):
        # Generate business days excluding holidays
        valid_days = pd.bdate_range(start=row.Start, end=row.End, freq='C', holidays=holidays)

        # Format the output
        for day in valid_days:
            id += 1
            relative_day = (day - today).days
            result.append(f"{id} '{row.Expert}' {relative_day} {row.Lower} {row.Upper}")

    return id, "\n".join(result)


def ubsum():
    today = glb.today()
    df = st.session_state.glb["ubsum"]
    result = [
        f"{id+1} '{row.Expert}' '{row.Task}' {(row.Start - today).days} "
        f"{(row.End - today).days} "
        f"{row.Lower} {row.Upper}"
        for id, row in enumerate(df.itertuples(index=False))
    ]
    return len(result), "\n".join(result)


def experts():
    return "\n".join(f"'{name}'" for name in st.session_state.glb["experts"]["Name"])


def expert_bounds():
    today = glb.today()
    df = st.session_state.glb["expert bounds"]
    result = [
        f"{id+1} '{row.Expert}' {(row.Start - today).days} "
        f"{(row.End - today).days} "
        f"{row.Lower * quarters_in_hour} "
        f"{row.Upper * quarters_in_hour}"
        for id, row in enumerate(df.itertuples(index=False))
    ]
    return len(result), "\n".join(result)


def links():
    df = st.session_state.glb["links"]
    return "\n".join(f"'{expert}' '{task}'" for expert, task in zip(df["Expert"], df["Task"]))


def invoicing_periods():
    today = glb.today()
    df = st.session_state.glb["invoicing periods"]
    result = [
        f"'{row.Name}' {(row.Start - today).days} {(row.End - today).days}"
        for row in df.itertuples(index=False)
    ]
    return "\n".join(result)


def invoicing_periods_bounds():
    today = glb.today()
    df = st.session_state.glb["invoicing periods bounds"]
    return "\n".join(
        f"'{expert}' '{period}' "
        f"{lower * quarters_in_hour} "
        f"{upper * quarters_in_hour}"
        for expert, period, lower, upper in zip(df["Expert"], df["Period"], df["Lower"], df["Upper"])
    )


def data_file(name):
    random_uuid = uuid.uuid4()
    ampl_data_file = f"./ampl-translated-from-excel/{name}-{random_uuid}.dat"
    with open(ampl_data_file, 'w') as f:
        f.write(f'param HOURS_PER_DAY := {glb.hours_per_day() * quarters_in_hour};\n\n')

        buf = experts()
        f.write('set EXPERTN :=\n')
        f.write(buf)
        f.write(';\n\n')

        expert_bound_no, buf = expert_bounds()
        f.write(f'param EBOUND_NO := {expert_bound_no};\n\n')
        f.write('param EBOUND:\n')
        f.write('1   2   3   4   5 :=\n')
        f.write(buf)
        f.write(';\n\n')

        buf = tasks()
        f.write('param:\n')
        f.write('TASKN: TASKS TASKE TASKW :=\n')
        f.write(buf)
        f.write(';\n\n')

        buf = invoicing_periods()
        f.write('param:\n')
        f.write('PAYROLLN: PAYROLLS PAYROLLE :=\n')
        f.write(buf)
        f.write(';\n\n')

        buf = invoicing_periods_bounds()
        f.write('param:\n')
        f.write('EXPPAY: PAYROLLBL PAYROLLBU :=\n')
        f.write(buf)
        f.write(';\n\n')

        offday_no, buf = offday()
        f.write(f'param OFFDAY_NO := {offday_no};\n\n')
        f.write('param OFFDAY :=\n')
        f.write(buf)
        f.write(';\n\n')

        xbday_no, buf = xbday()
        f.write(f'param XBDAY_NO := {xbday_no};\n\n')
        f.write('param XBDAY:\n')
        f.write('1   2   3   4   5 :=\n')
        f.write(buf)
        f.write(';\n\n')

        xbsum_no, buf = xbsum()
        f.write(f'param XBSUM_NO := {xbsum_no};\n\n')
        f.write('param XBSUM:\n')
        f.write('1   2   3   4   5   6 :=\n')
        f.write(buf)
        f.write(';\n\n')

        ubday_no, buf = ubday()
        f.write(f'param UBDAY_NO := {ubday_no};\n\n')
        f.write('param UBDAY:\n')
        f.write('1   2   3   4 :=\n')
        f.write(buf)
        f.write(';\n\n')

        ubsum_no, buf = ubsum()
        f.write(f'param UBSUM_NO := {ubsum_no};\n\n')
        f.write('param UBSUM:\n')
        f.write('1   2   3   4   5   6 :=\n')
        f.write(buf)
        f.write(';\n\n')

        buf = links()
        f.write('set LINKS :=\n')
        f.write(buf)
        f.write(';\n\n')

    return ampl_data_file



def save_schedule(ampl):
    today = glb.today()
    tasks_name = st.session_state.glb["tasks"]["Name"]
    experts_name = st.session_state.glb["experts"]["Name"]

    day_no = int(ampl.get_data("DAY_NO").to_pandas().iloc[0, 0])
    days = pd.date_range(start=today + pd.Timedelta(days=1), periods=day_no, freq='D')

    solution = dict()
    for en in experts_name:
        schedule = {
            tn: ampl.get_data(f"{{d in 1..DAY_NO}} X['{en}', d, '{tn}']").to_pandas().iloc[:, 0]
            for tn in tasks_name
        }
        # Create DataFrame from fetched data
        df = pd.DataFrame(schedule, dtype=np.float16).T / quarters_in_hour
        df.columns = days
        solution[f"schedule {en}"] = df / quarters_in_hour

    return solution


# activate AMPL license
def set_ampl_license():
    uuid = os.environ.get("AMPLKEY_UUID")
    if uuid is not None:
        modules.activate(uuid)


def solve(uploaded_file):
    time_start = time.perf_counter()

    solution = solve_ampl(uploaded_file.name, uploaded_file.getvalue())
    st.session_state.glb.update( solution )

    time_end = time.perf_counter()
    st.session_state.glb["time:ampl:ttime"] += time_end - time_start


@st.cache_resource
def solve_ampl(name, file_data):
    file = data_file(name)

    set_ampl_license()
    ampl = AMPL()

    # Customise AMPL run
    ampl.set_option('presolve', 10)
    ampl.set_option('show_stats', 4);
    # ampl.set_option('times', 1);

    solver = st.session_state.glb["misc"].iloc[0]["Solver"]
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

    ampl.read("./res/ampl_mathematical_model.mod.py")
    ampl.read_data(file)

    # Capture solver output and timestamp
    st.session_state.glb["solver output"] = ampl.get_output("solve;")
    st.session_state.glb["solver timestamp"] = datetime.datetime.now().strftime("%d %B %Y, %H:%M:%S %p")

    # Check if solving was successful
    if ampl.solve_result != "solved":
        raise Exception(f"Failed to solve AMPL problem. AMPL returned flag: {ampl.solve_result}")

    return save_schedule(ampl)

