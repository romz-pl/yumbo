import datetime

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


def plus_delta(dd, delta):
    return to_string(dd + datetime.timedelta(days=delta))
