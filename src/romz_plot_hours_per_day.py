import pandas as pd
import romz_plot_per_day

def plot(df, start_day, end_day, dpi):
    if end_day < start_day:
        end_day = start_day
    days = pd.period_range(start=start_day, end=end_day, freq="D").astype("str")
    hours_per_day = df[days].sum()
    romz_plot_per_day.plot(df, days, hours_per_day, 'Hours per day', 'C2', '/', dpi)
