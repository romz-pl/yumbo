import datetime

def format():
    return "%Y-%m-%d"


#def string_to_date(d):
#    return datetime.datetime.strptime(d, format()).date()



def from_string(d):
    return datetime.datetime.strptime(d, format())


def to_string(d):
    return d.strftime(format())
