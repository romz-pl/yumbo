import datetime
import pandas as pd
import numpy as np


def format():
    return "%Y-%m-%d"


#def string_to_date(d):
#    return datetime.datetime.strptime(d, format()).date()



def from_string(d):
    return datetime.datetime.strptime(d, format())


def to_string(d):
    return d.strftime(format())


def diff(d1, d2):
    return (d2 - d1).days


def length(d1, d2):
    return diff(d1, d2) + 1


def length_workdays(d1, d2, holidays):
    # Generate a date range between d1 and d2
    # 'B' frequency means business days (weekdays)
    date_range = pd.date_range(start=d1, end=d2, freq='B')

    # Convert holidays to a set for faster lookup
    holidays_set = set(holidays)

    # Filter the business days that are not in holidays
    workdays = np.setdiff1d(date_range, holidays_set)

    return len(workdays)



def plus_delta(dd, delta):
    return to_string(dd + datetime.timedelta(days=delta))
