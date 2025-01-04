import datetime
import pandas as pd
import os
import romz_datetime
from amplpy import AMPL, modules


def tasks(today, data):
    buf = str()
    to_skip = set()
    df = data["tasks"]
    for j in df.index:
        row = df.loc[j]
        start = (row["Start day"] - today).days
        end = (row["End day"] - today).days
        if end <= 0:
            to_skip.add(row["Name"])
            continue
        if start <= 0:
            start = 1
        buf += "'{name}' {start} {end} {work}\n".format(
            name=row["Name"], start=start, end=end, work=row["Work"])


    data["tasks"] = data["tasks"][ ~data["tasks"]["Name"].isin(to_skip) ]
    data["links"] = data["links"][ ~data["links"]["Task"].isin(to_skip) ]

    return buf


def offday(today, data):
    # Determine the date range
    min_date = max(data["tasks"]["Start day"].min(), today)
    max_date = data["tasks"]["End day"].max()

    # Generate weekends within the range using a mask for Saturdays and Sundays
    weekends = pd.bdate_range(start=min_date, end=max_date, freq='C', weekmask='Sat Sun')

    # Filter holidays to include only dates after 'today'
    holidays = data["public holidays"]["Date"]
    holidays = holidays[holidays > today]

    # Combine weekends and holidays into a sorted list
    # The set off_days is the union of weekends and holidays.
    # Sorting is not necessary. However, it does give deterministic (repetitive) results.
    off_days = sorted(set(weekends.union(holidays)))

    # Create the result buffer
    buf = "\n".join(f"{idx + 1} {(day - today).days}" for idx, day in enumerate(off_days))

    return len(off_days), buf


def xbday(today, data):
    id = 0
    buf = str()
    df = data["xbday"]
    df_tasks = data["tasks"]
    holidays = data["public holidays"]["Date"].to_numpy()
    for j in df.index:
        row = df.loc[j]
        task_name = row["Task"]
        expert_name = row["Expert"]
        lower = row["Lower"]
        upper = row["Upper"]
        task_row = df_tasks[ df_tasks["Name"] == task_name ]
        task_start_day = task_row["Start day"].array[0]
        task_end_day = task_row["End day"].array[0]
        d = row["Start day"]
        while d <= row["End day"]:
            if d < task_start_day or d > task_end_day:
                d += datetime.timedelta(days=1)
                continue
            if d.weekday() >= 5 or d in holidays:
                d += datetime.timedelta(days=1)
                continue
            day = (d - today).days
            id += 1
            buf += f"{id} '{expert_name}' '{task_name}' {day} {lower} {upper}\n"
            d += datetime.timedelta(days=1)

    return id, buf


def xbsum(today, data):
    id = 0
    buf = str()
    df = data["xbsum"]
    for j in df.index:
        row = df.loc[j]
        expert = row["Expert"]
        task = row["Task"]
        start = (row["Start day"] - today).days
        end = (row["End day"] - today).days
        lower = row["Lower"]
        upper = row["Upper"]
        id += 1
        buf += f"{id} '{expert}' '{task}' {start} {end} {lower} {upper}\n"

    return id, buf


def ubday(today, data):
    id = 0
    buf = str()
    holidays = data["public holidays"]["Date"].to_numpy()
    df = data["ubday"]
    for j in df.index:
        row = df.loc[j]
        expert = row["Expert"]
        lower = row["Lower"]
        upper = row["Upper"]
        d = row["Start day"]
        while d <= row["End day"]:
            if d.weekday() < 5 and d not in holidays:
                day = (d - today).days
                id += 1
                buf += f"{id} '{expert}' {day} {lower} {upper}\n"
            d += datetime.timedelta(days=1)

    return id, buf


def ubsum(today, data):
    id = 0
    buf = str()
    holidays = data["public holidays"]["Date"].to_numpy()
    df = data["ubsum"]
    for j in df.index:
        row = df.loc[j]
        expert = row["Expert"]
        task = row["Task"]
        start = (row["Start day"] - today).days
        end = (row["End day"] - today).days
        lower = row["Lower"]
        upper = row["Upper"]
        id += 1
        buf += f"{id} '{expert}' '{task}' {start} {end} {lower} {upper}\n"

    return id, buf


def experts(data):
    return "\n".join(f"'{name}'" for name in data["experts"]["Name"])


def expert_bounds(today, data):
    id = 0
    buf = str()
    df = data["expert bounds"]
    for j in df.index: 
        row = df.loc[j]
        start = (row["Start day"] - today).days
        end = (row["End day"] - today).days
        if end <= 0:
            continue
        if start <= 0:
            start = 1

        id += 1
        buf += "{id} '{expert}' {start} {end} {lower} {upper}\n".format(
            id=id, expert=row["Expert"], start=start, end=end, lower=row["Lower"], upper=row["Upper"])

    return id, buf


def links(data):
    df = data["links"]
    return "\n".join(f"'{expert}' '{task}'" for expert, task in zip(df["Expert"], df["Task"]))


def invoicing_periods(today, data):
    buf = str()
    df = data["invoicing periods"]
    for j in df.index:
        row = df.loc[j]
        start = (row["Start day"] - today).days
        end = (row["End day"] - today).days
        if end <= 0:
            continue
        if start <= 0:
            start = 1
        buf += "'{name}' {start} {end}\n".format(name=row["Name"], start=start, end=end)

    return buf


def invoicing_periods_bounds(today, data):
    df = data["invoicing periods bounds"]
    return "\n".join(
        f"'{expert}' '{period}' {lower} {upper}"
        for expert, period, lower, upper in zip(df["Expert"], df["Period"], df["Lower"], df["Upper"])
    )


def data_file(name, today, data):
    ampl_data_file = "./ampl-translated-from-excel/{}.dat".format(name)
    with open(ampl_data_file, 'w') as f:
        f.write('param HOURS_PER_DAY := {};\n\n'.format(data["misc"].loc[0, "Hours per day"]))

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
    days = pd.date_range(start=today + pd.Timedelta(days=1), periods=day_no, freq='D')

    for en in experts_name:
        schedule = {
            tn: ampl.get_data(f"{{d in 1..DAY_NO}} X['{en}', d, '{tn}']").to_pandas().iloc[:, 0]
            for tn in tasks_name
        }
        # Create DataFrame from fetched data
        df = pd.DataFrame(schedule).T
        df.columns = days
        data[f"schedule {en}"] = df


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


def solve(name, today, data):
    file = data_file(name, today, data)

    set_ampl_license()
    ampl = AMPL()
    solver = data["misc"].loc[0, "Solver"]
    ampl.set_option("solver", solver)

    if solver == "highs":
        ampl.option["highs_options"] = "outlev=1"

    if solver == "scip":
        ampl.option["scip_options"] = "tech:outlev-native=5"


    dirname1 = os.path.dirname(__file__)
    dirname2 = os.path.dirname(dirname1)
    ampl.cd(dirname2)

    ampl.read("./res/ampl_mathematical_model.mod.py")
    ampl.read_data(file)
    # ampl.solve()
    data["solver output"] = ampl.get_output("solve;")
    data["solver timestamp"] = "{d}".format(d=datetime.datetime.now().strftime("%d %B %Y, %H:%M:%S %p"))
    if ampl.solve_result != "solved":
        raise Exception(f"Failed to solve AMPL problem. AMPL returned flag: {ampl.solve_result}")
    save(ampl, data)
