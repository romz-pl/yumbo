import numpy as np
import streamlit as st

import glb


def highlight_rows(row):
    if row['Weekday'] in ['Sat', 'Sun']:
        return ['background-color: rgba(144,238,144, 0.2)'] * len(row)
    else:
        return [''] * len(row)



# Define a custom function to format each cell
def format_score(value):
    if isinstance(value, float):  # Apply formatting only to float values
        if value < 0.0001:
            return ""
        return f"{value:.2f}"  # Round to 1 decimal place
    return value  # Return non-float values unchanged


def show(df, as_html):
    # Define table styles as a list for clarity
    styles = [
        {'selector': 'tr:hover', 'props': [('background-color', '#555555')]},
        {'selector': 'td', 'props': 'text-align: right;'},
        {'selector': 'th:not(.index_name)', 'props': 'background-color: #000066; color: white;'}
    ]

    # Temporary column for Weekday
    df.insert(0, "Weekday", df.index.strftime('%a'))

    if as_html:
        # Render the styled DataFrame as HTML
        styled_df = (
            df.style
            .format(format_score)
            .format_index("{:%Y-%m-%d}", axis=0)
            .apply(highlight_rows, axis=1)
            .set_table_styles(styles, overwrite=True)
            .map(lambda _: 'color:LightBlue', subset=['Weekday'])
        )
        st.markdown(styled_df.to_html(), unsafe_allow_html=True)
    else:
        #
        # The "format_index" does not work with st.dataframe in Streamlit version 1.42.0!
        # So, a temporray column "Date" has been added and the index has been hidden.
        #

        # Temporary column for Date
        df.insert(0, "Date", df.index.strftime("%Y-%m-%d"))

        styled_df = (
            df.style
            .format(format_score)
            # .format_index("{:%Y-%m-%d}", axis=0) It does not work!
            .apply(highlight_rows, axis=1)
            .set_table_styles(styles, overwrite=True)
            .map(lambda _: 'color:LightBlue', subset=['Date', 'Weekday'])
        )
        st.dataframe(styled_df, hide_index=True)

        # Drop the temporary Date column
        df.drop(columns="Date", inplace=True)

    # Drop the temporary Weekday column
    df.drop(columns="Weekday", inplace=True)

