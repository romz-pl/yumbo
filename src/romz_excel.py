import pandas as pd
import romz_datetime

# Helper function to handle the date columns parsing
def parse_date_columns(df, date_columns, date_format):
    for column in date_columns:
        df[column] = pd.to_datetime(df[column], format=date_format)
    return df

# Helper function to calculate Days and Workdays
def add_days_and_workdays(df, holidays, date_columns):
    df["Days"] = [pd.bdate_range(start=df.loc[j, date_columns[0]],
                                 end=df.loc[j, date_columns[1]],
                                 freq='D').size for j in df.index]


    df["Workdays"] = [pd.bdate_range(start=df.loc[j, date_columns[0]],
                                     end=df.loc[j, date_columns[1]],
                                     freq='C',
                                     holidays=holidays["Date"]).size for j in df.index]
    return df

def read_tasks(xlsx, holidays):
    df = xlsx.parse(sheet_name="tasks", usecols="A:D")
    df = parse_date_columns(df, ["Start day", "End day"], romz_datetime.format())
    df = add_days_and_workdays(df, holidays, ["Start day", "End day"])
    df["Avg"] = df["Work"] / df["Workdays"]
    return df

def read_invoicing_periods(xlsx, holidays):
    df = xlsx.parse(sheet_name="invoicing periods", usecols="A:C")
    df = parse_date_columns(df, ["Start day", "End day"], romz_datetime.format())
    df = add_days_and_workdays(df, holidays, ["Start day", "End day"])
    return df

def read_xbday(xlsx):
    df = xlsx.parse(sheet_name="xbday", usecols="A:F")
    df = parse_date_columns(df, ["Start day", "End day"], romz_datetime.format())
    return df

def read_xbsum(xlsx):
    df = xlsx.parse(sheet_name="xbsum", usecols="A:F")
    df = parse_date_columns(df, ["Start day", "End day"], romz_datetime.format())
    return df

def read_ubday(xlsx):
    df = xlsx.parse(sheet_name="ubday", usecols="A:E")
    df = parse_date_columns(df, ["Start day", "End day"], romz_datetime.format())
    return df

def read_ubsum(xlsx):
    df = xlsx.parse(sheet_name="ubsum", usecols="A:F")
    df = parse_date_columns(df, ["Start day", "End day"], romz_datetime.format())
    return df

def read_experts(xlsx):
    return xlsx.parse(sheet_name="experts", usecols="A:B")

def read_expert_bounds(xlsx):
    df = xlsx.parse(sheet_name="expert bounds", usecols="A:E")
    df = parse_date_columns(df, ["Start day", "End day"], romz_datetime.format())
    return df

def read_public_holidays(xlsx):
    df = xlsx.parse(sheet_name="public holidays", usecols="A:A")
    df = parse_date_columns(df, ["Date"], romz_datetime.format())
    return df

def read_misc(xlsx):
    df = xlsx.parse(sheet_name="misc", usecols="A:H")
    for v in ["Today", "T:start", "T:end", "H:start", "H:end"]:
        df[v] = pd.to_datetime(df[v], format=romz_datetime.format())
    return df

def read_links(xlsx):
    return xlsx.parse(sheet_name="links", usecols="A:B")

def read_invoicing_periods_bounds(xlsx):
    return xlsx.parse(sheet_name="invoicing periods bounds", usecols="A:D")

def df_diff(df1, df2):
    return df1.merge(df2, how='outer', indicator=True).query('_merge == "left_only"').drop(columns='_merge')

def adjust_start_days(data):
    today = data["misc"].at[0, "Today"]
    tomorrow = today + pd.Timedelta(days=1)

    # List of DataFrame keys and the column to update
    targets = [
        "tasks",
        "xbday",
        "xbsum",
        "ubday",
        "ubsum",
        "expert bounds",
        "invoicing periods",
    ]

    # Apply the adjustment to each target DataFrame
    for key in targets:
        col = "Start day"
        assert(col in data[key].columns)
        data[key].loc[data[key][col] < tomorrow, col] = tomorrow


def read(file_path):
    xlsx = pd.ExcelFile(file_path)
    data = dict()
    holidays = read_public_holidays(xlsx)
    data["public holidays"] = holidays
    data["misc"] = read_misc(xlsx)
    data["tasks"] = read_tasks(xlsx, holidays)
    data["xbday"] = read_xbday(xlsx)
    data["xbsum"] = read_xbsum(xlsx)
    data["ubday"] = read_ubday(xlsx)
    data["ubsum"] = read_ubsum(xlsx)
    data["invoicing periods"] = read_invoicing_periods(xlsx, holidays)
    data["experts"] = read_experts(xlsx)
    data["expert bounds"] = read_expert_bounds(xlsx)
    data["invoicing periods bounds"] = read_invoicing_periods_bounds(xlsx)
    data["links"] = read_links(xlsx)
    adjust_start_days(data)
    return data
