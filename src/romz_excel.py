import numpy as np
import pandas as pd
import romz_datetime
import glb

# Helper function to handle the date columns parsing
def parse_date_columns(df, date_columns):
    for column in date_columns:
        df[column] = pd.to_datetime(df[column], format=romz_datetime.format())
    return df


# Helper function to calculate Days and Workdays
def add_days_and_workdays(df, start, end):

    # Calculate total days (inclusive)
    df["Days"] = (df[end] - df[start]).dt.days + 1

    # Define dtype for datetime conversion
    dtype = "datetime64[D]"

    # Convert public holidays to numpy datetime64[D]
    holidays = glb.data["public holidays"]["Date"].to_numpy(dtype=dtype)

    # Calculate workdays using numpy's busday_count
    df["Workdays"] = np.busday_count(
        df[start].to_numpy(dtype=dtype),
        (df[end] + pd.Timedelta(days=1)).to_numpy(dtype=dtype),
        holidays=holidays
    )

    return df


def read_tasks(xlsx):
    df = xlsx.parse(sheet_name="tasks", usecols="A:D")
    df = parse_date_columns(df, ["Start", "End"])
    df = add_days_and_workdays(df, "Start", "End")
    df["Avg"] = df["Work"] / df["Workdays"]
    glb.data["tasks"] = df


def read_invoicing_periods(xlsx):
    df = xlsx.parse(sheet_name="invoicing periods", usecols="A:C")
    df = parse_date_columns(df, ["Start", "End"])
    df = add_days_and_workdays(df, "Start", "End")
    glb.data["invoicing periods"] =  df


def read_xbday(xlsx):
    df = xlsx.parse(sheet_name="xbday", usecols="A:F")
    df = parse_date_columns(df, ["Start", "End"])
    glb.data["xbday"] = df


def read_xbsum(xlsx):
    df = xlsx.parse(sheet_name="xbsum", usecols="A:F")
    df = parse_date_columns(df, ["Start", "End"])
    glb.data["xbsum"] = df


def read_ubday(xlsx):
    df = xlsx.parse(sheet_name="ubday", usecols="A:E")
    df = parse_date_columns(df, ["Start", "End"])
    glb.data["ubday"] = df


def read_ubsum(xlsx):
    df = xlsx.parse(sheet_name="ubsum", usecols="A:F")
    df = parse_date_columns(df, ["Start", "End"])
    glb.data["ubsum"] = df


def read_experts(xlsx):
    glb.data["experts"] = xlsx.parse(sheet_name="experts", usecols="A:B")


def read_expert_bounds(xlsx):
    df = xlsx.parse(sheet_name="expert bounds", usecols="A:E")
    df = parse_date_columns(df, ["Start", "End"])
    glb.data["expert bounds"] = df


def read_public_holidays(xlsx):
    df = xlsx.parse(sheet_name="public holidays", usecols="A:A")
    df = parse_date_columns(df, ["Date"])
    glb.data["public holidays"] = df


def read_misc(xlsx):
    df = xlsx.parse(sheet_name="misc", usecols="A:C")
    glb.data["misc"] = df


def read_himg(xlsx):
    df = xlsx.parse(sheet_name="himg", usecols="B:I")
    df = parse_date_columns(df, ["Start", "End"])
    glb.data["himg"] = df


def read_timg(xlsx):
    df = xlsx.parse(sheet_name="timg", usecols="B:I")
    df = parse_date_columns(df, ["Start", "End"])
    glb.data["timg"] = df


def read_simg(xlsx):
    df = xlsx.parse(sheet_name="simg", usecols="B:G")
    df = parse_date_columns(df, ["Start", "End"])
    glb.data["simg"] = df


def read_gimg(xlsx):
    df = xlsx.parse(sheet_name="gimg", usecols="B:I")
    df = parse_date_columns(df, ["Start", "End"])
    glb.data["gimg"] = df


def read_wimg(xlsx):
    df = xlsx.parse(sheet_name="wimg", usecols="B:G")
    glb.data["wimg"] = df


def read_bimg(xlsx):
    df = xlsx.parse(sheet_name="bimg", usecols="B:J")
    glb.data["bimg"] = df


def read_links(xlsx):
    glb.data["links"] = xlsx.parse(sheet_name="links", usecols="A:B")


def read_invoicing_periods_bounds(xlsx):
    glb.data["invoicing periods bounds"] = xlsx.parse(sheet_name="invoicing periods bounds", usecols="A:D")


def adjust_start_days():
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

    tomorrow = pd.to_datetime(glb.tomorrow(), format=romz_datetime.format())

    # Apply the adjustment to each target DataFrame
    for key in targets:
        col = "Start"
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
    read_himg(xlsx)
    read_timg(xlsx)
    read_simg(xlsx)
    read_gimg(xlsx)
    read_wimg(xlsx)
    read_bimg(xlsx)
    adjust_start_days()

