import pandas as pd
import romz_plot_per_day

def plot(df, start_day, end_day, dpi):
    # Ensure the end day is not earlier than the start day
    end_day = max(end_day, start_day)

    # Generate date range as strings
    days = pd.period_range(start=start_day, end=end_day, freq="D").astype(str)

    # Count the number of tasks per day
    tasks_per_day = (df[days] > 0).sum()

    # Use the plotting function to visualize the data
    romz_plot_per_day.plot(df, days, tasks_per_day, "Tasks per day", "C3", "\\", dpi)
