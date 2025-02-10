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
    df.insert(0, "Weekday", df.index.strftime('%a'))

    # df.replace(0, np.nan, inplace=True)

    # Define table styles as a list for clarity
    styles = [
        {'selector': 'tr:hover', 'props': [('background-color', '#555555')]},
        {'selector': 'td', 'props': 'text-align: right;'},
        {'selector': 'th:not(.index_name)', 'props': 'background-color: #000066; color: white;'}
    ]

    # # Apply styling to the DataFrame using method chaining with parentheses for better readability
    # styled_df = (
    #     df.style
    #     .format_index("{:%Y-%m-%d}", axis=0)
    #     #.format(lambda x: '{:.2f}'.format(x) if isinstance(x, (int, float)) and x > 0 else '') # Represent NaN as empty string!
    #     .format(func),
    #     # .apply(highlight_rows, axis=1)
    #     #.set_table_styles(styles, overwrite=True)
    #     #.map(lambda v: 'color:LightBlue', subset=['Weekday'])
    # )



    # Apply the custom function to each cell in the DataFrame
    styled_df = (
        df.style
        .format(format_score)
        .format_index("{:%Y-%m-%d}", axis=0)
        .apply(highlight_rows, axis=1)
        .set_table_styles(styles, overwrite=True)
        .map(lambda v: 'color:LightBlue', subset=['Weekday'])
    )


    if as_html:
        # Render the styled dataframe as HTML.
        st.markdown(styled_df.to_html(), unsafe_allow_html=True)
    else:
        # Display the dataframe as a Streamlit table.
        # Some of the formats may not be displayed correctly!
        st.dataframe(styled_df, use_container_width=False)

    df.drop(columns="Weekday", inplace=True)
