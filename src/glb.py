data = dict()

def hours_per_day():
    return data["misc"].iloc[0]["Hours per day"]

def today():
    return data["misc"].iloc[0]["Today"]

def dpi():
    return int(data["misc"].iloc[0]["dpi"])
