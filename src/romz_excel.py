import pandas as pd
import romz_datetime


def read_tasks(xlsx, holidays):
    df = xlsx.parse(sheet_name = "tasks")
    df["Start day"] = pd.to_datetime(df["Start day"], format=romz_datetime.format())
    df["End day"] = pd.to_datetime(df["End day"], format=romz_datetime.format())
    df["Days"] = [romz_datetime.length(df.loc[j, "Start day"], df.loc[j, "End day"]) for j in df.index]
    df["Workdays"] = [romz_datetime.length_workdays(df.loc[j, "Start day"], df.loc[j, "End day"], holidays.to_numpy()) for j in df.index]
    df["Avg"] = df["Work"] / df["Workdays"]
    return df


def read_invoicing_periods(xlsx, holidays):
    df = xlsx.parse(sheet_name = "invoicing periods")
    df["Start day"] = pd.to_datetime(df["Start day"], format=romz_datetime.format())
    df["End day"] = pd.to_datetime(df["End day"], format=romz_datetime.format())
    df["Days"] = [romz_datetime.length(df.loc[j, "Start day"], df.loc[j, "End day"]) for j in df.index]
    df["Workdays"] = [romz_datetime.length_workdays(df.loc[j, "Start day"], df.loc[j, "End day"], holidays.to_numpy()) for j in df.index]
    return df


def read_xbday(xlsx):
    df = xlsx.parse(sheet_name = "xbday")
    df["Start day"] = pd.to_datetime(df["Start day"], format=romz_datetime.format())
    df["End day"] = pd.to_datetime(df["End day"], format=romz_datetime.format())
    return df


def read_xbsum(xlsx):
    df = xlsx.parse(sheet_name = "xbsum")
    df["Start day"] = pd.to_datetime(df["Start day"], format=romz_datetime.format())
    df["End day"] = pd.to_datetime(df["End day"], format=romz_datetime.format())
    return df


def read_ubday(xlsx):
    df = xlsx.parse(sheet_name = "ubday")
    df["Start day"] = pd.to_datetime(df["Start day"], format=romz_datetime.format())
    df["End day"] = pd.to_datetime(df["End day"], format=romz_datetime.format())
    return df


def read_ubsum(xlsx):
    df = xlsx.parse(sheet_name = "ubsum")
    df["Start day"] = pd.to_datetime(df["Start day"], format=romz_datetime.format())
    df["End day"] = pd.to_datetime(df["End day"], format=romz_datetime.format())
    return df


def read_experts(xlsx):
    df = xlsx.parse(sheet_name = "experts")
    return df


def read_expert_bounds(xlsx):
    df = xlsx.parse(sheet_name = "expert bounds")
    df["Start day"] = pd.to_datetime(df["Start day"], format=romz_datetime.format())
    df["End day"] = pd.to_datetime(df["End day"], format=romz_datetime.format())
    return df


def read_public_holidays(xlsx):
    df = xlsx.parse(sheet_name = "public holidays")
    df["Date"] = pd.to_datetime(df["Date"], format=romz_datetime.format())
    return df


def read_misc(xlsx):
    df = xlsx.parse(sheet_name = "misc")
    for v in ["Today", "T:start", "T:end", "H:start", "H:end"]:
        df[v] = pd.to_datetime(df[v], format=romz_datetime.format())
    return df


def read_links(xlsx):
    df = xlsx.parse(sheet_name = "links")
    return df


def read_invoicing_periods_bounds(xlsx):
    df = xlsx.parse(sheet_name = "invoicing periods bounds")
    return df


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
    return data
