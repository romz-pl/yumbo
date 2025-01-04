import pandas as pd
import romz_plot_per_day

def plot(df, start_day, end_day, dpi):
    # Ensure end_day is not before start_day
    end_day = max(end_day, start_day)

    # Generate the date range as string
    days = pd.period_range(start=start_day, end=end_day, freq="D").astype(str)

    # Sum the hours for each day
    hours_per_day = df[days].sum()

    # Plot the data
    romz_plot_per_day.plot(df, days, hours_per_day, "Hours per day", "C2", "/", dpi)

