import datetime
import pandas as pd
import os
import romz_datetime
from amplpy import AMPL, modules
import glb

quarters_in_hour = 4

def tasks(today, data):
    df = data["tasks"]

    # Calculate start and end days relative to today
    df["Start Relative"] = (df["Start day"] - today).dt.days
    df["End Relative"] = (df["End day"] - today).dt.days

    # Use vectorized string formatting for better performance
    formatted_rows = df.apply(
        lambda row: f"'{row['Name']}' {row['Start Relative']} {row['End Relative']} "
        f"{row['Work'] * quarters_in_hour}\n",
        axis=1,
    )

    df.drop(columns=["Start Relative", "End Relative"], inplace=True)

    return ''.join(formatted_rows)


def offday(today, data):
    # Determine the date range
    min_date = data["tasks"]["Start day"].min()
    max_date = data["tasks"]["End day"].max()

    # Generate weekends within the range using a mask for Saturdays and Sundays
    weekends = pd.bdate_range(start=min_date, end=max_date, freq='C', weekmask='Sat Sun')
    holidays = data["public holidays"]["Date"]

    # Combine weekends and holidays into a sorted list
    # The set off_days is the union of weekends and holidays.
    # Sorting is not necessary. However, it does give deterministic (repetitive) results.
    off_days = sorted(set(weekends.union(holidays)))

    # Create the result buffer
    buf = "\n".join(f"{idx + 1} {(day - today).days}" for idx, day in enumerate(off_days))

    return len(off_days), buf


def xbday(today, data):
    # Preprocessing for efficient lookups
    df = data["xbday"]
    df_tasks = data["tasks"].set_index("Name")  # Set "Name" as index for quick task lookup
    holidays = set(data["public holidays"]["Date"])  # Convert holidays to a set for faster checks

    result = []
    id_counter = 0

    # Iterate efficiently using itertuples
    for row in df.itertuples(index=False):
        task_name = row.Task
        expert_name = row.Expert
        lower = row.Lower * quarters_in_hour
        upper = row.Upper * quarters_in_hour

        # Calculate valid date range considering task bounds and xbday range
        task_start, task_end = df_tasks.loc[task_name, ["Start day", "End day"]]
        range_start = max(row._2, task_start)  # _2 corresponds to "Start day" in xbday
        range_end = min(row._3, task_end)      # _3 corresponds to "End day" in xbday

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




def xbsum(today, data):
    df = data["xbsum"]
    result = []

    # Iterate over rows using itertuples for better performance
    for idx, row in enumerate(df.itertuples(index=False), start=1):
        expert = row.Expert
        task = row.Task
        start = (row._2 - today).days # _2 <- Start day
        end = (row._3 - today).days # _3 <- End day
        lower = row.Lower * quarters_in_hour
        upper = row.Upper * quarters_in_hour

        # Append formatted string to result list
        result.append(f"{idx} '{expert}' '{task}' {start} {end} {lower} {upper}")

    # Join the result list with newline characters
    return len(result), "\n".join(result)



def ubday(today, data):
    df = data["ubday"]
    holidays = set(data["public holidays"]["Date"])

    result = []
    id = 0

    for _, row in df.iterrows():
        expert = row["Expert"]
        lower = row["Lower"]
        upper = row["Upper"]

        # Generate business days excluding holidays
        valid_days = pd.bdate_range(start=row["Start day"], end=row["End day"], freq='C', holidays=holidays)

        # Format the output
        for day in valid_days:
            id += 1
            relative_day = (day - today).days
            result.append(f"{id} '{expert}' {relative_day} {lower} {upper}")

    return id, "\n".join(result)


def ubsum(today, data):
    df = data["ubsum"]
    result = [
        f"{id+1} '{row['Expert']}' '{row['Task']}' {(row['Start day'] - today).days} "
        f"{(row['End day'] - today).days} "
        f"{row.Lower} {row.Upper}"
        for id, row in df.iterrows()
    ]
    return len(result), "\n".join(result)


def experts(data):
    return "\n".join(f"'{name}'" for name in data["experts"]["Name"])


def expert_bounds(today, data):
    df = data["expert bounds"]
    result = [
        f"{id+1} '{row['Expert']}' {(row['Start day'] - today).days} "
        f"{(row['End day'] - today).days} "
        f"{row['Lower'] * quarters_in_hour} "
        f"{row['Upper'] * quarters_in_hour}"
        for id, row in df.iterrows()
    ]
    return len(result), "\n".join(result)


def links(data):
    df = data["links"]
    return "\n".join(f"'{expert}' '{task}'" for expert, task in zip(df["Expert"], df["Task"]))


def invoicing_periods(today, data):
    df = data["invoicing periods"]
    result = [
        f"'{row['Name']}' {(row['Start day'] - today).days} {(row['End day'] - today).days}"
        for _, row in df.iterrows()
    ]
    return "\n".join(result)


def invoicing_periods_bounds(today, data):
    df = data["invoicing periods bounds"]
    return "\n".join(
        f"'{expert}' '{period}' "
        f"{lower * quarters_in_hour} "
        f"{upper * quarters_in_hour}"
        for expert, period, lower, upper in zip(df["Expert"], df["Period"], df["Lower"], df["Upper"])
    )


def data_file(name, today, data):
    ampl_data_file = "./ampl-translated-from-excel/{}.dat".format(name)
    with open(ampl_data_file, 'w') as f:
        f.write('param HOURS_PER_DAY := {};\n\n'.format(data["misc"].loc[0, "Hours per day"] * quarters_in_hour))

        buf = experts(data)
        f.write('set EXPERTN :=\n')
        f.write(buf)
        f.write(';\n\n')

        expert_bound_no, buf = expert_bounds(today, data)
        f.write('param EBOUND_NO := {};\n\n'.format(expert_bound_no))
        f.write('param EBOUND:\n')
        f.write('1   2   3   4   5 :=\n')
        f.write(buf)
        f.write(';\n\n')

        buf = tasks(today, data)
        f.write('param:\n')
        f.write('TASKN: TASKS TASKE TASKW :=\n')
        f.write(buf)
        f.write(';\n\n')

        buf = invoicing_periods(today, data)
        f.write('param:\n')
        f.write('PAYROLLN: PAYROLLS PAYROLLE :=\n')
        f.write(buf)
        f.write(';\n\n')

        buf = invoicing_periods_bounds(today, data)
        f.write('param:\n')
        f.write('EXPPAY: PAYROLLBL PAYROLLBU :=\n')
        f.write(buf)
        f.write(';\n\n')

        offday_no, buf = offday(today, data)
        f.write('param OFFDAY_NO := {};\n\n'.format(offday_no))
        f.write('param OFFDAY :=\n')
        f.write(buf)
        f.write(';\n\n')

        xbday_no, buf = xbday(today, data)
        f.write('param XBDAY_NO := {};\n\n'.format(xbday_no))
        f.write('param XBDAY:\n')
        f.write('1   2   3   4   5 :=\n')
        f.write(buf)
        f.write(';\n\n')

        xbsum_no, buf = xbsum(today, data)
        f.write('param XBSUM_NO := {};\n\n'.format(xbsum_no))
        f.write('param XBSUM:\n')
        f.write('1   2   3   4   5   6 :=\n')
        f.write(buf)
        f.write(';\n\n')

        ubday_no, buf = ubday(today, data)
        f.write('param UBDAY_NO := {};\n\n'.format(ubday_no))
        f.write('param UBDAY:\n')
        f.write('1   2   3   4 :=\n')
        f.write(buf)
        f.write(';\n\n')

        ubsum_no, buf = ubsum(today, data)
        f.write('param UBSUM_NO := {};\n\n'.format(ubsum_no))
        f.write('param UBSUM:\n')
        f.write('1   2   3   4   5   6 :=\n')
        f.write(buf)
        f.write(';\n\n')

        buf = links(data)
        f.write('set LINKS :=\n')
        f.write(buf)
        f.write(';\n\n')

    return ampl_data_file


def save_schedule(ampl, data):
    today = data["misc"].loc[0, "Today"]
    tasks_name = data["tasks"]["Name"]
    experts_name = data["experts"]["Name"]

    day_no = int(ampl.get_data("DAY_NO").to_pandas().iloc[0, 0])
    days = pd.date_range(start=today + pd.Timedelta(days=1), periods=day_no, freq='D').astype("str")

    for en in experts_name:
        schedule = {
            tn: ampl.get_data(f"{{d in 1..DAY_NO}} X['{en}', d, '{tn}']").to_pandas().iloc[:, 0]
            for tn in tasks_name
        }
        # Create DataFrame from fetched data
        df = pd.DataFrame(schedule).T
        df.columns = days
        data[f"schedule {en}"] = df / quarters_in_hour


def save_day_no(ampl, data):
    data["DAY_NO"] = ampl.get_parameter("DAY_NO").to_pandas().astype(int).iat[0,0]


def save(ampl, data):
    save_schedule(ampl, data)
    save_day_no(ampl, data)


# activate AMPL license
def set_ampl_license():
    uuid = os.environ.get("AMPLKEY_UUID")
    if uuid is not None:
        modules.activate(uuid)


def solve(name):
    file = data_file(name, glb.today(), glb.data)

    set_ampl_license()
    ampl = AMPL()
    solver = glb.data["misc"].iloc[0]["Solver"]
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
    glb.data["solver output"] = ampl.get_output("solve;")
    glb.data["solver timestamp"] = datetime.datetime.now().strftime("%d %B %Y, %H:%M:%S %p")

    # Check if solving was successful
    if ampl.solve_result != "solved":
        raise Exception(f"Failed to solve AMPL problem. AMPL returned flag: {ampl.solve_result}")

    save(ampl, glb.data)

