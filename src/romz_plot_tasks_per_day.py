import pandas as pd
import romz_plot_per_day

def plot(df, start_day, end_day, dpi):
    if end_day < start_day:
        end_day = start_day

    days = pd.period_range(start=start_day, end=end_day, freq="D").astype("str")
    tasks_per_day = (df[days] > 0).sum()
    romz_plot_per_day.plot(df, days, tasks_per_day, 'Tasks per day', 'C3', '\\', dpi)
