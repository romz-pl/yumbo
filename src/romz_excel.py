import pandas as pd
import romz_datetime
import glb

# Helper function to handle the date columns parsing
def parse_date_columns(df, date_columns, date_format):
    for column in date_columns:
        df[column] = pd.to_datetime(df[column], format=date_format)
    return df

# Helper function to calculate Days and Workdays
def add_days_and_workdays(df, date_columns):
    df["Days"] = [pd.bdate_range(start=df.loc[j, date_columns[0]],
                                 end=df.loc[j, date_columns[1]],
                                 freq='D').size for j in df.index]


    df["Workdays"] = [pd.bdate_range(start=df.loc[j, date_columns[0]],
                                     end=df.loc[j, date_columns[1]],
                                     freq='C',
                                     holidays=glb.data["public holidays"]["Date"]).size for j in df.index]
    return df

def read_tasks(xlsx):
    df = xlsx.parse(sheet_name="tasks", usecols="A:D")
    df = parse_date_columns(df, ["Start day", "End day"], romz_datetime.format())
    df = add_days_and_workdays(df, ["Start day", "End day"])
    df["Avg"] = df["Work"] / df["Workdays"]
    glb.data["tasks"] = df

def read_invoicing_periods(xlsx):
    df = xlsx.parse(sheet_name="invoicing periods", usecols="A:C")
    df = parse_date_columns(df, ["Start day", "End day"], romz_datetime.format())
    df = add_days_and_workdays(df, ["Start day", "End day"])
    glb.data["invoicing periods"] =  df

def read_xbday(xlsx):
    df = xlsx.parse(sheet_name="xbday", usecols="A:F")
    df = parse_date_columns(df, ["Start day", "End day"], romz_datetime.format())
    glb.data["xbday"] = df

def read_xbsum(xlsx):
    df = xlsx.parse(sheet_name="xbsum", usecols="A:F")
    df = parse_date_columns(df, ["Start day", "End day"], romz_datetime.format())
    glb.data["xbsum"] = df

def read_ubday(xlsx):
    df = xlsx.parse(sheet_name="ubday", usecols="A:E")
    df = parse_date_columns(df, ["Start day", "End day"], romz_datetime.format())
    glb.data["ubday"] = df

def read_ubsum(xlsx):
    df = xlsx.parse(sheet_name="ubsum", usecols="A:F")
    df = parse_date_columns(df, ["Start day", "End day"], romz_datetime.format())
    glb.data["ubsum"] = df

def read_experts(xlsx):
    glb.data["experts"] = xlsx.parse(sheet_name="experts", usecols="A:B")

def read_expert_bounds(xlsx):
    df = xlsx.parse(sheet_name="expert bounds", usecols="A:E")
    df = parse_date_columns(df, ["Start day", "End day"], romz_datetime.format())
    glb.data["expert bounds"] = df

def read_public_holidays(xlsx):
    df = xlsx.parse(sheet_name="public holidays", usecols="A:A")
    df = parse_date_columns(df, ["Date"], romz_datetime.format())
    glb.data["public holidays"] = df


def read_misc(xlsx):
    df = xlsx.parse(sheet_name="misc", usecols="A:H")
    for v in ["Today", "T:start", "T:end", "H:start", "H:end"]:
        df[v] = pd.to_datetime(df[v], format=romz_datetime.format())
    glb.data["misc"] = df

def read_links(xlsx):
    glb.data["links"] = xlsx.parse(sheet_name="links", usecols="A:B")

def read_invoicing_periods_bounds(xlsx):
    glb.data["invoicing periods bounds"] = xlsx.parse(sheet_name="invoicing periods bounds", usecols="A:D")

def df_diff(df1, df2):
    return df1.merge(df2, how='outer', indicator=True).query('_merge == "left_only"').drop(columns='_merge')

def adjust_start_days():
    tomorrow = glb.today() + pd.Timedelta(days=1)

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
        assert(col in glb.data[key].columns)
        glb.data[key].loc[glb.data[key][col] < tomorrow, col] = tomorrow


def read(file_path):
    xlsx = pd.ExcelFile(file_path)
    read_public_holidays(xlsx)
    read_misc(xlsx)
    read_tasks(xlsx)
    read_xbday(xlsx)
    read_xbsum(xlsx)
    read_ubday(xlsx)
    read_ubsum(xlsx)
    read_invoicing_periods(xlsx)
    read_experts(xlsx)
    read_expert_bounds(xlsx)
    read_invoicing_periods_bounds(xlsx)
    read_links(xlsx)
    adjust_start_days()
