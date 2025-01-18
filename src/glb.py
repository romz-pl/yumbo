import datetime

data = dict()

def hours_per_day():
    return data["misc"].iloc[0]["Hours per day"]

def today():
    return data["misc"].iloc[0]["Today"]
    # return data["misc"].at[0, "Today"]

def tomorrow():
    return (today() + datetime.timedelta(days=1)).date()

def dpi():
    return int(data["misc"].iloc[0]["dpi"])

def last_day():
    return (today() + datetime.timedelta(days=int(data["DAY_NO"]))).date()

def tstart():
    return data["misc"].iloc[0]["T:start"]

def tend():
    return data["misc"].iloc[0]["T:end"]

def hstart():
    return data["misc"].iloc[0]["H:start"]

def hend():
    return data["misc"].iloc[0]["H:end"]
