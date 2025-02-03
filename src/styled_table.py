import numpy as np

import glb

def highlight_rows(row):
    if row['Weekdays'] in ['Saturday', 'Sunday']:
        return ['background-color: rgba(144,238,144, 0.2)'] * len(row)
    else:
        return [''] * len(row)


def create(df, days):

    # df.index = days.astype(str)
    df.index = df.index.strftime(glb.format())
    df.replace(0, np.nan, inplace=True)

    # Insert the "Weekdays" column at the beginning
    df.insert(0, "Weekdays", days.day_name())

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
        .map(lambda v: 'color:LightBlue', subset=['Weekdays'])
    )

    return styled_df

