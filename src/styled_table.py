import streamlit as st
import time
import uuid

import glb

def highlight_rows(row):
    if row['Weekday'] in ['Sat', 'Sun']:
        return ['background-color: rgba(144,238,144, 0.2)'] * len(row)
    else:
        return [''] * len(row)


def format_cell(value):
    if isinstance(value, float):  # Apply formatting only to float values
        if value < 0.0001:
            return ""
        return f"{value:.2f}"  # Round to 2 decimal place
    return value  # Return non-float values unchanged



@st.cache_resource(max_entries=1000)
def create_stable(df, df_name):
    """
    The index is hidden due to Streamlit version 1.42.0 limitations.
    df_name is required for correct caching!
    """

    # Create a temporary DataFrame with additional columns (avoid modifying original df)
    temp_df = df.copy()
    temp_df.insert(0, "Weekday", temp_df.index.strftime('%a'))
    temp_df.insert(0, "Date", temp_df.index.strftime(glb.format()))

    # Apply styling
    styled_df = (
        temp_df.style
        .format(format_cell)
        # .format_index("{:%Y-%m-%d}", axis=0) It does not work!
        .apply(highlight_rows, axis=1)
        .map(lambda _: 'color:LightBlue', subset=['Date', 'Weekday'])
    )

    csv = temp_df.to_csv(index=False).encode("utf-8")
    size_in_Kib = len(csv) / 1024
    file_name = f"{uuid.uuid4().hex}.csv"

    return styled_df, csv, size_in_Kib, file_name


def show_stable(df):
    time_start = time.perf_counter()

    styled_df, csv, size_in_Kib, file_name = create_stable(df, df.name)

    time_end = time.perf_counter()
    st.session_state.stats["S:Table:cnt"] += 1
    st.session_state.stats["S:Table:ttime"] += time_end - time_start
    st.session_state.stats["S:Table:nbytes"] += df.memory_usage(deep=True).sum()

    # Render DataFrame in Streamlit
    st.dataframe(styled_df, hide_index=True)

    st.download_button(
        label=f"Download schedule :green[{file_name}] -> {size_in_Kib:,.1f} KiB",
        key=file_name,
        data=csv,
        file_name=file_name,
        mime="text/csv",
        icon=":material/download:",
    )


@st.cache_resource(max_entries=1000)
def create_htable(df, df_name):
    """
    df_name is required for correct caching!
    """

    # Define table styles
    styles = [
        {"selector": "tr:hover", "props": [("background-color", "#555555")]},
        {"selector": "td", "props": [("text-align", "right")]},
        {"selector": "th:not(.index_name)", "props": [("background-color", "#000066"), ("color", "white")]}
    ]

    # Create a temporary DataFrame with additional columns (avoid modifying original df)
    temp_df = df.copy()
    temp_df.insert(0, "Weekday", temp_df.index.strftime('%a'))

    # Apply styling
    styled_df = (
        temp_df.style
        .format(format_cell)
        .format_index("{:%Y-%m-%d}", axis=0)
        .apply(highlight_rows, axis=1)
        .set_table_styles(styles, overwrite=True)
        .map(lambda _: "color:LightBlue", subset=["Weekday"])
    )

    return styled_df


def show_htable(df):
    time_start = time.perf_counter()

    styled_df = create_htable(df, df.name)

    time_end = time.perf_counter()
    st.session_state.stats["H:Table:cnt"] += 1
    st.session_state.stats["H:Table:ttime"] += time_end - time_start
    st.session_state.stats["H:Table:nbytes"] += df.memory_usage(deep=True).sum()

    # Render the styled DataFrame as HTML
    st.write(styled_df.to_html(), unsafe_allow_html=True)


def show(df, as_html):
    if as_html:
        show_htable(df)
    else:
        show_stable(df)
