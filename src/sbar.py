import numpy as np
import os
import pandas as pd
import streamlit as st

import glb

def get_uploaded_file():
    st.subheader(":material/database: :blue[Load Excel data file]", divider="blue")

    uploaded_file = st.file_uploader("Excel file required in format 'xlsx'", label_visibility="collapsed")
    if uploaded_file == None:
        st.subheader(":red[Select Excel data file for scheduling investigation!]")
        dd = os.path.dirname(__file__)
        st.image(f"{dd}/../doc/logo/python-logo.png")
        st.image(f"{dd}/../doc/logo/python-logo-large.png")
        st.image(f"{dd}/../doc/logo/python-package-logo-large.svg")

    # st.markdown("See the [Yumbo](https://github.com/romz-pl/yambo/tree/main/ampl-data-input-excel) GitHub repository for sample Excel input files.")
    return uploaded_file


def customise_expert_report_layout():
    st.subheader(":material/dashboard: :blue[Appearance]", divider="blue")

    max_col_no = 5
    report_column_no = st.number_input("Number of charts", min_value=1, max_value=max_col_no, value=max_col_no)

    for ii in range(1, max_col_no + 1):
        st.session_state.show[f"expert_column_{ii}"] = st.selectbox(
            f"Col {ii}",
            ("Task's Gantt chart", "Tasks per day", "Hours per day stacked", "Hours per day", "Invoice period workload"),
            disabled = (ii > report_column_no),
            index = (ii - 1),
            label_visibility = "collapsed",
        )
    st.session_state.show["expert_column_no"] = report_column_no

def customise_expert_orientation():
    st.subheader(":material/flip_camera_android: :blue[Orientation]", divider="blue")
    label = "Charts in one column"
    st.session_state.show["expert_charts_in_one_column"] = st.checkbox(label, key="experts" + label)


def customise_expert_show():
    st.subheader(":material/group: :blue[Layout]", divider="blue")
    experts_init = st.session_state.show["experts_init"]

    df = st.data_editor(
        experts_init,
        hide_index=False,
        use_container_width=True,
        column_config={
            "Expert": st.column_config.TextColumn(disabled=True, pinned=True),
            **{col: st.column_config.CheckboxColumn() for col in experts_init.columns},
        },
    )

    label = "All charts"
    if st.checkbox(label, key="experts" + label):
        df["Chart"] = True

    label = "All H:Tables"
    if st.checkbox(label, key="experts" + label):
        df["H:Table"] = True

    label = "All S:Tables"
    if st.checkbox(label, key="experts" + label):
        df["S:Table"] = True

    label = "All xbdays"
    if st.checkbox(label, key="experts" + label):
        df["xbday"] = True

    label = "None"
    if st.checkbox(label, key="experts" + label):
        df.loc[:, :] = False

    st.session_state.show["experts"] = df


def customise_show_tasks():
    st.subheader(":material/receipt_long: :blue[Layout]", divider="blue")

    tasks_init = st.session_state.show["tasks_init"]

    df = st.data_editor(
        tasks_init,
        hide_index=False,
        use_container_width=True,
        column_config={
            "Task": st.column_config.TextColumn(disabled=True, pinned=True),
            **{col: st.column_config.CheckboxColumn() for col in tasks_init.columns},
        },
    )

    label = "All charts"
    if st.checkbox(label, key="tasks" + label):
        df["Chart"] = True

    label = "All H:Tables"
    if st.checkbox(label, key="tasks" + label):
        df["H:Table"] = True

    label = "All S:Tables"
    if st.checkbox(label, key="tasks" + label):
        df["S:Table"] = True

    label = "None"
    if st.checkbox(label, key="tasks" + label):
        df.loc[:, :] = False

    st.session_state.show["tasks"] = df


def customise_date_range():
    st.subheader(":material/date_range: :blue[Date ranges]", divider="blue")

    mprob = st.session_state.mprob
    row = st.columns(2)

    start = row[0].date_input(
        "Start date",
        format="YYYY-MM-DD",
        min_value=glb.tomorrow(),
        max_value=glb.last_day(),
        value=mprob["img_init"].loc[0, "Start"],
    )

    mprob["img"].loc[0, "Start"] = pd.to_datetime(start)

    end = row[1].date_input(
        "End date",
        format="YYYY-MM-DD",
        min_value=glb.tomorrow(),
        max_value=glb.last_day(),
        value=mprob["img_init"].loc[0, "End"],
    )

    mprob["img"].loc[0, "End"] = pd.to_datetime(end)


def customise_chart_colours():
    st.subheader(":material/palette: :blue[Colors]", divider="blue")

    # Mapping data keys to labels
    sections = [
        ("imgt", "Tasks per day", "Bar:color"),
        ("imgh", "Hours per day", "Bar:color"),
        ("imgg", "Task's Gantt Chart", "Barh:color"),
        ("imgw", "Invoicing Periods Workload", "Bar:color"),
    ]

    mprob = st.session_state.mprob
    for key, label, col in sections:
        row = st.columns(2)
        row[0].write(label)

        new_color = row[1].color_picker(
            f"{key}:Color",
            key=f"{key}:Color",
            label_visibility="collapsed",
            value=mprob[f"{key}_init"].loc[0, col],

        )
        mprob[key].loc[0, col] = new_color


def customise_ampl():
    st.subheader(":material/calculate: :blue[Layout]", divider="blue")

    show = st.session_state.show
    show["ampl_solver_log"] = st.checkbox("Solver log", value=False)
    show["ampl_data_file"] = st.checkbox("AMPL data file", value=False)
    show["ampl_model_file"] = st.checkbox("AMPL model file", value=False)


def customise_expert():
    customise_expert_orientation()
    customise_expert_report_layout()
    customise_expert_show()


def customise_task():
    customise_show_tasks()


def show_planing_horizon():
    st.subheader(f":material/timeline: :blue[Planing horizon]", divider="blue")
    st.markdown(f"Today: :green[{glb.today().date()}]")
    st.markdown(f"Tomorrow: :green[{glb.tomorrow().date()}]")
    st.markdown(f"Last day: :green[{glb.last_day().date()}]")
    st.markdown(f"Number of days: :green[{(glb.last_day() - glb.today()).days}]")


def customise_summary_orientation():
    st.subheader(":material/flip_camera_android: :blue[Orientation]", divider="blue")
    label = "Charts in one column"
    show = st.session_state.show
    show["summary_charts_in_one_column"] = st.checkbox(label, key="summary" + label)


def customise_summary_show():
    st.subheader(":material/summarize: :blue[Layout]", divider="blue")

    show = st.session_state.show
    show["summary_tasks_gantt_chart"] = st.checkbox("Task's Gantt Chart", value=True)
    show["summary_tasks_per_day"] = st.checkbox("Tasks per day", value=True)
    show["summary_hours_per_day"] = st.checkbox("Hours per day", value=True)
    show["summary_full_schedule"] = st.checkbox("Full schedule", value=False)

    if glb.is_ampl_model_overflow():
        show["summary_task_overflows"] = st.checkbox("Task overflows", value=True)
    else:
        show["summary_task_overflows"] = False


def customise_summary():
    customise_summary_orientation()
    customise_summary_show()

def customise_problem():
    st.subheader(":material/database: :blue[Layout]", divider="blue")

    show = st.session_state.show
    show["problem"] = st.checkbox("Problem definition", value=False)
    show["days_off"] = st.checkbox(f"Show days off", value=False)


def customise_stats():
    st.subheader(":material/analytics: :blue[Layout]", divider="blue")

    show = st.session_state.show
    show["stats_chart_table"] = st.checkbox("Statistics on chart and table creation", value=True)
    show["stats_execution"] = st.checkbox("Statistics on Yumbo execution", value=True)


def max_imag_sizes():
    max_width = 12.0
    max_height = 12.0
    return max_width, max_height


def image_zoom_in():
    max_width, max_height = max_imag_sizes()

    st.session_state.image_width = min(max_width, 1.1 * st.session_state.image_width)
    st.session_state.image_height = min(max_height, 1.1 * st.session_state.image_height)


def image_zoom_out():
    max_width, max_height = max_imag_sizes()

    st.session_state.image_width = min(max_width, st.session_state.image_width / 1.1)
    st.session_state.image_height = min(max_height, st.session_state.image_height / 1.1)



def customise_size_and_dpi():
    st.subheader(":material/aspect_ratio: :blue[Size and DPI]", divider="blue")

    max_width, max_height = max_imag_sizes()

    mprob = st.session_state.mprob
    st.button(":material/zoom_in: Zoom In 10%", on_click=image_zoom_in)
    st.button(":material/zoom_out: Zoom Out 10%", on_click=image_zoom_out)

    if "image_width" not in st.session_state:
        st.session_state.image_width = mprob["img_init"].loc[0, "Width"]

    if "image_height" not in st.session_state:
        st.session_state.image_height = mprob["img_init"].loc[0, "Height"]

    with st.form("my_form"):
        width = st.slider("Width", key="image_width", min_value=1.0, max_value=max_width, step=0.1, format="%.1f")
        height = st.slider("Height", key="image_height", min_value=1.0, max_value=max_height, step=0.1, format="%.1f")

        dpi_init = int(mprob["img_init"].loc[0, "Dpi"])
        dpi = st.slider("Dpi", min_value=10, max_value=600, value=dpi_init, step=1)

        submitted = st.form_submit_button("Set sizes and DPI")


    if submitted:
        mprob["img"].loc[0, "Width"] = width
        mprob["img"].loc[0, "Height"] = height
        mprob["img"].loc[0, "Dpi"] = dpi
        st.rerun()


def customise_chart():
    customise_chart_colours()
    customise_date_range()
    customise_size_and_dpi()



def show():

    # st.divider()

    tab = st.tabs(["**Expert**", "**Task**", "**Summary**", "**AMPL**", "**Problem**", "**Stats**", "**Chart**", "**Horizon**"])
    with tab[0]:
        customise_expert()
    with tab[1]:
        customise_task()
    with tab[2]:
        customise_summary()
    with tab[3]:
        customise_ampl()
    with tab[4]:
        customise_problem()
    with tab[5]:
        customise_stats()
    with tab[6]:
        customise_chart()
    with tab[7]:
        show_planing_horizon()

