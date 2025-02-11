import os
import streamlit as st
import tempfile
import time
import uuid
import zipfile

import glb
import imggsum
import imghsum
import imgtsum
import styled_table


def show_charts():
    show = st.session_state.show

    b_list = [
        show["summary_tasks_gantt_chart"],
        show["summary_tasks_per_day"],
        show["summary_hours_per_day"],
    ]

    if not any(b_list):
        return

    days_off = show["days_off"]
    func_list = [imggsum.plot, imgtsum.plot, imghsum.plot]

    if show["summary_charts_in_one_column"]:
        # Loop through and plot charts in one column
        for func, show_chart in zip(func_list, b_list):
            if show_chart:
                func(days_off)
    else:
        # Create columns only for the charts that need to be shown
        col_list = st.columns(sum(b_list))
        col_index = 0

        for func, show_chart in zip(func_list, b_list):
            if show_chart:
                with col_list[col_index]:
                    func(days_off)
                col_index += 1


def show_overflow():
    task_overflows = st.session_state.show["summary_task_overflows"]

    if glb.is_ampl_model_overflow() and task_overflows:
        overflow = st.session_state.overflow
        if overflow.sum() > 0:
            st.subheader(":red[There are task overflows!]", divider="red")
            df = overflow[ overflow > 0]
            st.write(df)
        else:
            st.subheader(":green[There in no overflows]", divider="green")


@st.fragment()
def download_full_schedule(df):
    csv = glb.convert_df_to_csv(df)

    file_name = f"{uuid.uuid4().hex}.csv"

    st.download_button(
        label=f"Download full schedule as :green[{file_name}]",
        data=csv,
        file_name=file_name,
        mime="text/csv",
    )


@st.cache_resource(max_entries=1000)
def save_to_compressed_file(df, compression):
    f_tmp = tempfile.NamedTemporaryFile(
        mode='w+',
        prefix="yumbo-",
        delete=False,
        delete_on_close=False,
    )

    csv = df.to_csv(index=False).encode("utf-8")
    ampl_data_file = st.session_state.mprob["ampl_data_file"]
    solver_log = st.session_state.stats["solver_log"]

    ampl_model_file = glb.get_ampl_model_file()
    with open(ampl_model_file, "r") as f:
        ampl_model = f.read()

    with open(ampl_model_file + ".run", "r") as f:
        ampl_model_run = f.read()

    with zipfile.ZipFile(f_tmp.name, 'w', compression=compression, compresslevel=9) as zf:
        zf.writestr("full_schedule.csv", csv)
        zf.writestr("ampl_data_file.dat", ampl_data_file)
        zf.writestr("solver_log.txt", solver_log)
        zf.writestr("model.ampl", ampl_model)
        zf.writestr("model.ampl.run", ampl_model_run)

    f_tmp.close()
    return f_tmp



def download_complete_set(df, compression, ext):
    f_tmp = save_to_compressed_file(df, compression)
    with open(f_tmp.name, 'rb') as f:
        file_name = f"{uuid.uuid4().hex}.{ext}"
        st.download_button(
            label=f"Download the complete set as :green[{file_name}]",
            data=f,
            file_name=file_name,
        )
    os.unlink(f.name)


@st.fragment()
def download_complete_set_zip(df):
    download_complete_set(df, zipfile.ZIP_DEFLATED, "zip")


@st.fragment()
def download_complete_set_bz2(df):
    download_complete_set(df, zipfile.ZIP_BZIP2, "bz2")


def show_full_schedule(as_html):
    if not st.session_state.show["summary_full_schedule"]:
        return

    st.subheader(":green[Full schedule]", divider="green")

    df = st.session_state.schedule

    # .strftime('%a') Returns 'Mon', 'Tue', etc.
    # .strftime('%A') Returns 'Monday', 'Tuesday', etc.
    df.insert(0, "Weekday", df.index.strftime('%a'))
    df.insert(0, "Date", df.index.strftime("%Y-%m-%d"))

    #
    # streamlit.errors.StreamlitAPIException:
    # The dataframe has 309748 cells, but the maximum number of cells allowed to be rendered by Pandas Styler is configured to 262144.
    # To allow more cells to be styled, you can change the "styler.render.max_elements" config.
    # For example: pd.set_option("styler.render.max_elements", 309748)
    #
    # Always display the dataframe as a Streamlit table without styles to avoid the above error.
    st.dataframe(df, use_container_width=False, hide_index=True)

    download_full_schedule(df)
    download_complete_set_zip(df)
    download_complete_set_bz2(df)

    df.drop(columns="Date", inplace=True)
    df.drop(columns="Weekday", inplace=True)


def show_report():
    show = st.session_state.show

    # Extract relevant values from the session state
    b_list = [
        show["summary_tasks_gantt_chart"],
        show["summary_tasks_per_day"],
        show["summary_hours_per_day"],
        show["summary_task_overflows"],
        show["summary_full_schedule"],
    ]

    # Return early if no charts are to be shown
    if not any(b_list):
        return

    st.divider()
    st.header(":blue[Summary]", divider="blue")

    show_charts()
    show_overflow()
    show_full_schedule(False)


def show():
    time_start = time.perf_counter()
    show_report()
    time_end = time.perf_counter()
    st.session_state.stats["report_summary:ttime"] += time_end - time_start
