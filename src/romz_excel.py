import numpy as np
import pandas as pd
import streamlit as st
import tempfile
import time

import glb


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



def read_task(xlsx, mprob):
    df = xlsx.parse(sheet_name="task", usecols="A:D").sort_values("Name")
    df = parse_date_columns(df, ["Start", "End"])
    df = add_days_and_workdays(df, "Start", "End", mprob)
    df["Avg"] = df["Work"] / df["Workdays"]
    df.set_index("Name", drop=False, inplace=True, verify_integrity=True)
    df.index.name = "Nindex"
    mprob["task"] = df
    return mprob


def read_expert(xlsx, mprob):
    df = xlsx.parse(sheet_name="expert", usecols="A:B").sort_values("Name")
    df.set_index("Name", drop=False, inplace=True, verify_integrity=True)
    df.index.name = "Nindex"
    mprob["expert"] = df
    return mprob


def read_assign(xlsx, mprob):
    df = xlsx.parse(sheet_name="assign", usecols="A:B").sort_values(["Expert", "Task"])
    df.set_index(["Expert", "Task"], drop=False, inplace=True, verify_integrity=True)
    df.index.names = ["Elevel", "Tlevel"]
    mprob["assign"] = df
    return mprob


def read_xbday(xlsx, mprob):
    df = xlsx.parse(sheet_name="xbday", usecols="A:F").sort_values(["Expert", "Task"])
    df = parse_date_columns(df, ["Start", "End"])
    mprob["xbday"] = df
    return mprob


def read_ubday(xlsx, mprob):
    df = xlsx.parse(sheet_name="ubday", usecols="A:E").sort_values("Expert")
    df = parse_date_columns(df, ["Start", "End"])
    mprob["ubday"] = df
    return mprob


def read_ebday(xlsx, mprob):
    df = xlsx.parse(sheet_name="ebday", usecols="A:E").sort_values("Expert")
    df = parse_date_columns(df, ["Start", "End"])
    mprob["ebday"] = df
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


def read_holiday(xlsx, mprob):
    df = xlsx.parse(sheet_name="holiday", usecols="A:A")
    df = parse_date_columns(df, ["Date"])
    df.sort_values("Date", inplace=True)
    mprob["holiday"] = df
    return mprob


def read_misc(xlsx, mprob):
    df = xlsx.parse(sheet_name="misc", usecols="A:D")
    mprob["misc"] = df
    return mprob


def read_img(xlsx, mprob):
    df = xlsx.parse(sheet_name="img", usecols="B:F")
    df = parse_date_columns(df, ["Start", "End"])
    df["Width_init"] = df["Width"]
    df["Height_init"] = df["Height"]
    df["Dpi_init"] = df["Dpi"]
    df["Start_init"] = df["Start"]
    df["End_init"] = df["End"]
    mprob["img"] = df
    return mprob

def read_imgh(xlsx, mprob):
    df = xlsx.parse(sheet_name="imgh", usecols="B:D")
    mprob["imgh"] = df
    return mprob


def read_imgt(xlsx, mprob):
    df = xlsx.parse(sheet_name="imgt", usecols="B:D")
    mprob["imgt"] = df
    return mprob


def read_imgs(xlsx, mprob):
    df = xlsx.parse(sheet_name="imgs", usecols="B:B")
    mprob["imgs"] = df
    return mprob


def read_imgg(xlsx, mprob):
    df = xlsx.parse(sheet_name="imgg", usecols="B:D")
    mprob["imgg"] = df
    return mprob


def read_imgw(xlsx, mprob):
    df = xlsx.parse(sheet_name="imgw", usecols="B:D")
    mprob["imgw"] = df
    return mprob


def read_imgb(xlsx, mprob):
    df = xlsx.parse(sheet_name="imgb", usecols="B:G")
    mprob["imgb"] = df
    return mprob


def read_imge(xlsx, mprob):
    mprob["imge"] = xlsx.parse(sheet_name="imge", usecols="B:B")
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

        mprob = dict()
        xlsx = pd.ExcelFile(f)
        mprob = read_holiday(xlsx, mprob)
        mprob = read_misc(xlsx, mprob)
        mprob = read_task(xlsx, mprob)
        mprob = read_xbday(xlsx, mprob)
        mprob = read_ubday(xlsx, mprob)
        mprob = read_period(xlsx, mprob)
        mprob = read_expert(xlsx, mprob)
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
