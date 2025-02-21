import numpy as np
import pandas as pd
import streamlit as st
import tempfile
import time

import glb


import pandas as pd
import os
from typing import Union, List, Tuple

def validate_excel_file(file_path):
    """
    Validates an Excel file by checking:
        1. If the file exists and is readable
        2. If it has a valid file extension
        3. If required columns are present (optional)
        4. If required sheets are present (optional)

    Args:
        file_path: Path to the Excel file
    """

    sheets_and_columns = {
        "expert" :["Name", "Comment"],
        "task": ["Name", "Start", "End", "Work"],
        "assign": ["Expert", "Task"],
        "xbday": ["Expert", "Task", "Start", "End", "Lower", "Upper"],
        "ubday": ["Expert", "Start", "End", "Lower", "Upper"],
        "ebday": ["Expert", "Start", "End", "Lower", "Upper"],
        "period": ["Name", "Start", "End"],
        "pbsum": ["Expert", "Period", "Lower", "Upper"],
        "holiday": ["Date"],
        "misc": ["Today", "Hours per day", "Solver", "AMPL model"],
        "img": ["Width", "Height", "Dpi", "End", "Start"],
        "imgh": ["Bar:color", "Bar:hatch", "Bar:alpha"],
        "imgt": ["Bar:color", "Bar:hatch", "Bar:alpha"],
        "imgs": ["Bar:alpha"],
        "imgg": ["Barh:color", "Barh:height", "Barh:alpha"],
        "imgw": ["Bar:color", "Bar:ecolor", "Bar:capsize"],
        "imgb": ["Fill:color", "Fill:hatch", "Fill:alpha", "Plot:format", "Plot:markeredgewidth", "Step:linewidth"],
        "imge": ["Bar:alpha"],
    }

    # Check if file exists
    if not os.path.exists(file_path):
        raise Exception(f"File not found: {file_path}")

    # Check file extension
    if not file_path.endswith(('.xlsx', '.xls', '.xlsm')):
        raise Exception("File is not an Excel file (must end with .xlsx, .xls, or .xlsm)")

    # Try to read the file with pandas. Read Excel info without loading data.
    excel_info = pd.ExcelFile(file_path)

    # Check for required sheets
    missing_sheets = set(sheets_and_columns.keys()) - set(excel_info.sheet_names)
    if missing_sheets:
        raise Exception(f"In Excel file: Missing required sheets: {', '.join(missing_sheets)}")


    # For each sheet, check the required columns.
    for sheet, columns in sheets_and_columns.items():
        df = pd.read_excel(file_path, sheet_name=sheet)
        missing_cols = set(columns) - set(df.columns)
        if missing_cols:
            raise Exception(f"In Excel file: Sheet '{sheet}' is missing required columns: {', '.join(missing_cols)}")



# Helper function to handle the date columns parsing
def parse_date_columns(df, date_columns):
    for column in date_columns:
        df[column] = pd.to_datetime(df[column], format=glb.format())
    return df


# Helper function to calculate Days and Workdays
def add_days_and_workdays(df, start, end, mprob):

    # Calculate total days (inclusive)
    df["Days"] = (df[end] - df[start]).dt.days + 1

    # Define dtype for datetime conversion
    dtype = "datetime64[D]"

    # Convert public holidays to numpy datetime64[D]
    holiday = mprob["holiday"]["Date"].to_numpy(dtype=dtype)

    # Calculate workdays using numpy's busday_count
    df["Workdays"] = np.busday_count(
        df[start].to_numpy(dtype=dtype),
        (df[end] + pd.Timedelta(days=1)).to_numpy(dtype=dtype),
        holidays=holiday
    )

    return df


def get_today(mprob):
    today = mprob["misc"].at[0, "Today"]
    return pd.to_datetime(today, format=glb.format())


def check_task(df, mprob):
    invalid = df["Start"] > df["End"]
    if invalid.any():
        invalid_rows = df[invalid]
        raise Exception(f"Found {len(invalid_rows)} task's Start date after End!")

    invalid = df["End"] <= get_today(mprob)
    if invalid.any():
        invalid_rows = df[invalid]
        raise Exception(f"Found {len(invalid_rows)} task's End date before Today!")


def read_task(xlsx, mprob):
    df = xlsx.parse(sheet_name="task", usecols="A:D").sort_values("Name")
    df = parse_date_columns(df, ["Start", "End"])
    df = add_days_and_workdays(df, "Start", "End", mprob)
    df["Avg"] = df["Work"] / df["Workdays"]
    df.set_index("Name", drop=False, inplace=True, verify_integrity=True)
    df.index.name = "Nindex"
    check_task(df, mprob)
    mprob["task"] = df
    return mprob


def read_expert(xlsx, mprob):
    df = xlsx.parse(sheet_name="expert", usecols="A:B").sort_values("Name")
    df.set_index("Name", drop=False, inplace=True, verify_integrity=True)
    df.index.name = "Nindex"
    mprob["expert"] = df
    return mprob


def check_assign(df, mprob):
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        raise Exception(f"Found {duplicates} in assigments!")


    delta = set(df["Expert"]) - set(mprob["expert"]["Name"])
    if len(delta) > 0:
        raise Exception(f"Found at least {len(delta)} assigment(s) to unknown expert(s)!")


    delta = set(mprob["expert"]["Name"]) - set(df["Expert"])
    if len(delta) > 0:
        raise Exception(f"Found {len(delta)} expert(s) without an assigned task!")


    delta = set(df["Task"]) - set(mprob["task"]["Name"])
    if len(delta) > 0:
        raise Exception(f"Found at least {len(delta)} assigment(s) to unknown task(s)!")


    delta = set(mprob["task"]["Name"]) - set(df["Task"])
    if len(delta) > 0:
        raise Exception(f"Found {len(delta)} task(s) without an assigned expert!")


def read_assign(xlsx, mprob):
    df = xlsx.parse(sheet_name="assign", usecols="A:B").sort_values(["Expert", "Task"])
    df.set_index(["Expert", "Task"], drop=False, inplace=True, verify_integrity=True)
    df.index.names = ["Elevel", "Tlevel"]
    check_assign(df, mprob)
    mprob["assign"] = df
    return mprob


def check_xbday(df, mprob):
    delta = set(df["Expert"]) - set(mprob["expert"]["Name"])
    if len(delta) > 0:
        raise Exception(f"Found {len(delta)} unknown expert(s) in XBDAY!")

    delta = set(df["Task"]) - set(mprob["task"]["Name"])
    if len(delta) > 0:
        raise Exception(f"Found {len(delta)} unknown task(s) in XBDAY!")

    invalid = df["Start"] > df["End"]
    if invalid.any():
        invalid_rows = df[invalid]
        raise Exception(f"Found {len(invalid_rows)} Start date after End in XBDAY!")



def read_xbday(xlsx, mprob):
    df = xlsx.parse(sheet_name="xbday", usecols="A:F").sort_values(["Expert", "Task"])
    df = parse_date_columns(df, ["Start", "End"])
    mprob["xbday"] = df
    check_xbday(df, mprob)
    return mprob


def check_ubday(df, mprob):
    delta = set(df["Expert"]) - set(mprob["expert"]["Name"])
    if len(delta) > 0:
        raise Exception(f"Found {len(delta)} unknown expert(s) in UBDAY!")

    invalid = df["Start"] > df["End"]
    if invalid.any():
        invalid_rows = df[invalid]
        raise Exception(f"Found {len(invalid_rows)} Start date after End in UBDAY!")


def read_ubday(xlsx, mprob):
    df = xlsx.parse(sheet_name="ubday", usecols="A:E").sort_values("Expert")
    df = parse_date_columns(df, ["Start", "End"])
    check_ubday(df, mprob)
    mprob["ubday"] = df
    return mprob


def check_ebday(df, mprob):
    delta = set(df["Expert"]) - set(mprob["expert"]["Name"])
    if len(delta) > 0:
        raise Exception(f"Found {len(delta)} unknown expert(s) in EBDAY!")

    invalid = df["Start"] > df["End"]
    if invalid.any():
        invalid_rows = df[invalid]
        raise Exception(f"Found {len(invalid_rows)} Start date after End in EBDAY!")


def read_ebday(xlsx, mprob):
    df = xlsx.parse(sheet_name="ebday", usecols="A:E").sort_values("Expert")
    df = parse_date_columns(df, ["Start", "End"])
    mprob["ebday"] = df
    check_ebday(df, mprob)
    return mprob


def read_period(xlsx, mprob):
    df = xlsx.parse(sheet_name="period", usecols="A:C")
    df = parse_date_columns(df, ["Start", "End"])
    df.sort_values("Start", inplace=True)
    df = add_days_and_workdays(df, "Start", "End", mprob)
    df.set_index("Name", drop=False, inplace=True, verify_integrity=True)
    df.index.name = "Pindex"
    mprob["period"] =  df
    return mprob


def read_pbsum(xlsx, mprob):
    df = xlsx.parse(sheet_name="pbsum", usecols="A:D").sort_values(["Expert", "Period"])
    df.set_index(["Expert", "Period"], drop=False, inplace=True, verify_integrity=True)
    df.index.names = ["Elevel", "Plevel"]
    mprob["pbsum"] = df
    return mprob



def check_holiday(df, mprob):
    invalid = df["Date"] <= get_today(mprob)
    if invalid.any():
        invalid_rows = df[invalid]
        raise Exception(f"Found {len(invalid_rows)} holiday dates before Today!")


def read_holiday(xlsx, mprob):
    df = xlsx.parse(sheet_name="holiday", usecols="A:A")
    df = parse_date_columns(df, ["Date"])
    df.sort_values("Date", inplace=True)
    check_holiday(df, mprob)
    mprob["holiday"] = df
    return mprob


def read_misc(xlsx, mprob):
    df = xlsx.parse(sheet_name="misc", usecols="A:D")
    mprob["misc"] = df
    return mprob


def read_img(xlsx, mprob):
    df = xlsx.parse(sheet_name="img", usecols="B:F")
    df = parse_date_columns(df, ["Start", "End"])
    mprob["img"] = df
    mprob["img_init"] = df.copy()
    return mprob

def read_imgh(xlsx, mprob):
    df = xlsx.parse(sheet_name="imgh", usecols="B:D")
    mprob["imgh"] = df
    mprob["imgh_init"] = df.copy()
    return mprob


def read_imgt(xlsx, mprob):
    df = xlsx.parse(sheet_name="imgt", usecols="B:D")
    mprob["imgt"] = df
    mprob["imgt_init"] = df.copy()
    return mprob


def read_imgs(xlsx, mprob):
    df = xlsx.parse(sheet_name="imgs", usecols="B:B")
    mprob["imgs"] = df
    mprob["imgs_init"] = df.copy()
    return mprob


def read_imgg(xlsx, mprob):
    df = xlsx.parse(sheet_name="imgg", usecols="B:D")
    mprob["imgg"] = df
    mprob["imgg_init"] = df.copy()
    return mprob


def read_imgw(xlsx, mprob):
    df = xlsx.parse(sheet_name="imgw", usecols="B:D")
    mprob["imgw"] = df
    mprob["imgw_init"] = df.copy()
    return mprob


def read_imgb(xlsx, mprob):
    df = xlsx.parse(sheet_name="imgb", usecols="B:G")
    mprob["imgb"] = df
    mprob["imgb_init"] = df.copy()
    return mprob


def read_imge(xlsx, mprob):
    df = xlsx.parse(sheet_name="imge", usecols="B:B")
    mprob["imge"] = df
    mprob["imge_init"] = df.copy()
    return mprob


def adjust_start_days(mprob):
    # List of DataFrame keys and the column to update
    targets = [
        "task",
        "xbday",
        "ubday",
        "ebday",
        "period",
    ]

    today = mprob["misc"].iloc[0]["Today"]
    tomorrow = today + pd.Timedelta(1, unit="D")

    # Apply the adjustment to each target DataFrame
    for key in targets:
        col = "Start"
        assert(col in mprob[key].columns)
        mprob[key].loc[mprob[key][col] < tomorrow, col] = tomorrow

    return mprob


@st.cache_resource(max_entries=99)
def read_excel_file(file_data, git_hash):
    with tempfile.NamedTemporaryFile(prefix="yumbo", suffix=".xlsx") as f:
        f.write(file_data)
        f.flush()

        validate_excel_file(f.name)

        mprob = dict()
        xlsx = pd.ExcelFile(f)
        mprob = read_misc(xlsx, mprob)
        mprob = read_holiday(xlsx, mprob)
        mprob = read_expert(xlsx, mprob)
        mprob = read_task(xlsx, mprob)
        mprob = read_xbday(xlsx, mprob)
        mprob = read_ubday(xlsx, mprob)
        mprob = read_period(xlsx, mprob)
        mprob = read_ebday(xlsx, mprob)
        mprob = read_pbsum(xlsx, mprob)
        mprob = read_assign(xlsx, mprob)
        mprob = read_img(xlsx, mprob)
        mprob = read_imgh(xlsx, mprob)
        mprob = read_imgt(xlsx, mprob)
        mprob = read_imgs(xlsx, mprob)
        mprob = read_imgg(xlsx, mprob)
        mprob = read_imgw(xlsx, mprob)
        mprob = read_imgb(xlsx, mprob)
        mprob = read_imge(xlsx, mprob)
        mprob = adjust_start_days(mprob)

        return mprob


def load(uploaded_file):
    time_start = time.perf_counter()

    git_hash = st.session_state.git_hash
    st.session_state.mprob = read_excel_file(uploaded_file.getvalue(), git_hash)

    time_end = time.perf_counter()
    st.session_state.stats["excel:ttime"] += time_end - time_start
