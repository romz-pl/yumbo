import numpy as np

import glb

#import streamlit as st

def highlight_rows(row):
    # if row['Weekdays'] in ['Saturday', 'Sunday']:
    #     return ['background-color: rgba(144,238,144, 0.2)'] * len(row)
    # else:
    #     return [''] * len(row)

    return [''] * len(row)


def create(df, as_html):
    if as_html:
        df.replace(0, np.nan, inplace=True)

    #
    # streamlit.errors.StreamlitAPIException:
    # The dataframe has 309748 cells, but the maximum number of cells allowed to be rendered by Pandas Styler is configured to 262144.
    # To allow more cells to be styled, you can change the "styler.render.max_elements" config.
    # For example: pd.set_option("styler.render.max_elements", 309748)
    #
    # In order to avoid the error that is listed above.
    if df.shape[0] * df.shape[1] > 100 * 1000:
        return df

    # Define table styles as a list for clarity
    styles = [
        {'selector': 'tr:hover', 'props': [('background-color', '#555555')]},
        {'selector': 'td', 'props': 'text-align: right;'},
        {'selector': 'th:not(.index_name)', 'props': 'background-color: #000066; color: white;'}
    ]

    # Apply styling to the DataFrame using method chaining with parentheses for better readability
    styled_df = (
        df.style
        .format(na_rep='', precision=2) # Represent NaN as empty
        .apply(highlight_rows, axis=1)
        .set_table_styles(styles, overwrite=True)
        # .map(lambda v: 'color:LightBlue', subset=['Weekdays'])
    )

    return styled_df

