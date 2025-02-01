import glb
import numpy as np
import pandas as pd
import streamlit as st

# Helper function to handle the date columns parsing
def parse_date_columns(df, date_columns):
    for column in date_columns:
        df[column] = pd.to_datetime(df[column], format=glb.format())
    return df


# Helper function to calculate Days and Workdays
def add_days_and_workdays(df, start, end):

    # Calculate total days (inclusive)
    df["Days"] = (df[end] - df[start]).dt.days + 1

    # Define dtype for datetime conversion
    dtype = "datetime64[D]"

    # Convert public holidays to numpy datetime64[D]
    holiday = st.session_state.mprob["holiday"]["Date"].to_numpy(dtype=dtype)

    # Calculate workdays using numpy's busday_count
    df["Workdays"] = np.busday_count(
        df[start].to_numpy(dtype=dtype),
        (df[end] + pd.Timedelta(days=1)).to_numpy(dtype=dtype),
        holidays=holiday
    )

    return df


def read_task(xlsx):
    df = xlsx.parse(sheet_name="task", usecols="A:D")
    df = parse_date_columns(df, ["Start", "End"])
    df = add_days_and_workdays(df, "Start", "End")
    df["Avg"] = df["Work"] / df["Workdays"]
    st.session_state.mprob["task"] = df


def read_period(xlsx):
    df = xlsx.parse(sheet_name="period", usecols="A:C")
    df = parse_date_columns(df, ["Start", "End"])
    df = add_days_and_workdays(df, "Start", "End")
    st.session_state.mprob["period"] =  df


def read_xbday(xlsx):
    df = xlsx.parse(sheet_name="xbday", usecols="A:F")
    df = parse_date_columns(df, ["Start", "End"])
    st.session_state.mprob["xbday"] = df


def read_ubday(xlsx):
    df = xlsx.parse(sheet_name="ubday", usecols="A:E")
    df = parse_date_columns(df, ["Start", "End"])
    st.session_state.mprob["ubday"] = df


def read_expert(xlsx):
    st.session_state.mprob["expert"] = xlsx.parse(sheet_name="expert", usecols="A:B")


def read_ebday(xlsx):
    df = xlsx.parse(sheet_name="ebday", usecols="A:E")
    df = parse_date_columns(df, ["Start", "End"])
    st.session_state.mprob["ebday"] = df


def read_holiday(xlsx):
    df = xlsx.parse(sheet_name="holiday", usecols="A:A")
    df = parse_date_columns(df, ["Date"])
    st.session_state.mprob["holiday"] = df


def read_misc(xlsx):
    df = xlsx.parse(sheet_name="misc", usecols="A:C")
    st.session_state.mprob["misc"] = df


def read_himg(xlsx):
    df = xlsx.parse(sheet_name="himg", usecols="B:I")
    df = parse_date_columns(df, ["Start", "End"])
    st.session_state.mprob["himg"] = df


def read_timg(xlsx):
    df = xlsx.parse(sheet_name="timg", usecols="B:I")
    df = parse_date_columns(df, ["Start", "End"])
    st.session_state.mprob["timg"] = df


def read_simg(xlsx):
    df = xlsx.parse(sheet_name="simg", usecols="B:G")
    df = parse_date_columns(df, ["Start", "End"])
    st.session_state.mprob["simg"] = df


def read_gimg(xlsx):
    df = xlsx.parse(sheet_name="gimg", usecols="B:G")
    st.session_state.mprob["gimg"] = df


def read_wimg(xlsx):
    df = xlsx.parse(sheet_name="wimg", usecols="B:G")
    st.session_state.mprob["wimg"] = df


def read_bimg(xlsx):
    df = xlsx.parse(sheet_name="bimg", usecols="B:J")
    st.session_state.mprob["bimg"] = df


def read_eimg(xlsx):
    st.session_state.mprob["eimg"] = xlsx.parse(sheet_name="eimg", usecols="B:E")


def read_assign(xlsx):
    st.session_state.mprob["assign"] = xlsx.parse(sheet_name="assign", usecols="A:B")


def read_pbsum(xlsx):
    st.session_state.mprob["pbsum"] = xlsx.parse(sheet_name="pbsum", usecols="A:D")


def adjust_start_days():
    # List of DataFrame keys and the column to update
    targets = [
        "task",
        "xbday",
        "ubday",
        "ebday",
        "period",
    ]

    tomorrow = pd.to_datetime(glb.tomorrow(), format=glb.format())

    # Apply the adjustment to each target DataFrame
    for key in targets:
        col = "Start"
        assert(col in st.session_state.mprob[key].columns)
        st.session_state.mprob[key].loc[st.session_state.mprob[key][col] < tomorrow, col] = tomorrow


def read(file_path):
    xlsx = pd.ExcelFile(file_path)
    read_holiday(xlsx)
    read_misc(xlsx)
    read_task(xlsx)
    read_xbday(xlsx)
    read_ubday(xlsx)
    read_period(xlsx)
    read_expert(xlsx)
    read_ebday(xlsx)
    read_pbsum(xlsx)
    read_assign(xlsx)
    read_himg(xlsx)
    read_timg(xlsx)
    read_simg(xlsx)
    read_gimg(xlsx)
    read_wimg(xlsx)
    read_bimg(xlsx)
    read_eimg(xlsx)
    adjust_start_days()

