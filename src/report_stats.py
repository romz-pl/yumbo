import pandas as pd
import streamlit as st


def show_stats_chart_table():
    st.subheader(":green[Statistics on chart and table creation]", divider="green")

    chart_data = [
        ("Plot task with its constrains", "imgb"),
        ("Task's Gantt Chart", "imgg"),
        ("Task's Gantt Chart (Summary)", "imggsum"),
        ("Hours per day", "imgh"),
        ("Hours per day  (Summary)", "imghsum"),
        ("Hours per day stacked", "imgs"),
        ("Tasks per day", "imgt"),
        ("Tasks per day (Summary)", "imgtsum"),
        ("Invoicing Periods Workload", "imgw"),
        ("Experts per day stacked", "imge"),
        ("A HTML table", "H:Table"),
        ("A Simple table", "S:Table"),
    ]

    # Column names
    time_total_col = "Total time [s]"
    time_avg_col = "Average time [s]"
    nbytes_total_col = "Total nbytes [KiB]"
    nbytes_avg_col = "Average nbytes [B]"

    # Extract relevant data in a single pass
    chart_titles = []
    short_names = []
    num_calls = []
    time_total = []
    time_avg = []
    nbytes_total = []
    nbytes_avg = []

    for title, short_name in chart_data:
        chart_titles.append(title)
        short_names.append(short_name)

        cnt = st.session_state.stats[f"{short_name}:cnt"]
        num_calls.append(cnt)

        ttime = st.session_state.stats[f"{short_name}:ttime"]
        time_total.append(ttime)
        time_avg.append(ttime / cnt if cnt != 0 else 0)

        nbytes = st.session_state.stats[f"{short_name}:nbytes"]
        nbytes_total.append(nbytes / 1024)
        nbytes_avg.append(nbytes / cnt if cnt != 0 else 0)

    # Create a DataFrame to organize the data
    data = pd.DataFrame({
        "Chart title": chart_titles,
        "Chart short name": short_names,
        "Number of calls": num_calls,
        time_total_col: time_total,
        time_avg_col: time_avg,
        nbytes_total_col: nbytes_total,
        nbytes_avg_col: nbytes_avg,
    })

    # Create DataFrame and format it
    format_spec = {
        time_total_col: "{:,.3f}",
        time_avg_col: "{:,.3f}",
        nbytes_total_col: "{:,.0f}",
        nbytes_avg_col: "{:,.0f}",
    }

    df = pd.DataFrame(data)
    df_styled = (
        df
        .sort_values(by="Chart title", ascending=False)
        .style.format(format_spec)
    )

    # Display DataFrame
    st.dataframe(df_styled, hide_index=True, use_container_width=False)

    mb = df[nbytes_total_col].sum()  / 1024
    st.markdown("**For all figures, the total number of data downloaded is: :green[{:,.3f} MiB]**".format(mb))


def show_stats_execution():
    st.subheader(":green[Statistics on Yumbo execution]", divider="green")

    stats = st.session_state.stats
    messages = [
        ("Solution time of AMPL model", "ampl:ttime"),
        ("Load time from Excel file", "excel:ttime"),
        ("Time taken to report on experts", "report_experts:ttime"),
        ("Time taken to report on tasks", "report_tasks:ttime"),
        ("Time taken to report on summary", "report_summary:ttime"),
    ]

    for label, key in messages:
        st.markdown(f"**{label}: :green[{stats[key]:.3f} [s]]**")


def show():
    stats_chart_table = st.session_state.show["stats_chart_table"]
    stats_execution = st.session_state.show["stats_execution"]

    if not (stats_chart_table or stats_execution):
        return

    st.divider()
    st.header(":blue[Statistics]", divider="blue")

    if stats_chart_table:
        show_stats_chart_table()

    if stats_execution:
        show_stats_execution()
