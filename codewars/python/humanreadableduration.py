'''
https://www.codewars.com/kata/52742f58faf5485cae000b9a/train/python
'''

LENMINUTE = 60
LENHOUR = 3600
LENDAY = 86400
LENYEAR = 31536000


def format_duration(seconds):
    if seconds is 0:
        return "now"

    lis = []
    years = int(seconds / LENYEAR)
    days = int((seconds % LENYEAR) / LENDAY)
    hours = int(((seconds % LENYEAR) % LENDAY) / LENHOUR)
    minutes = int((((seconds % LENYEAR) % LENDAY) % LENHOUR) / LENMINUTE)
    secleft = int((((seconds % LENYEAR) % LENDAY) % LENHOUR) % LENMINUTE)

    if years is not 0:
        if years is 1:
            lis.append("{} year".format(years))
        else:
            lis.append("{} years".format(years))
    if days is not 0:
        if days is 1:
            lis.append("{} day".format(days))
        else:
            lis.append("{} days".format(days))
    if hours is not 0:
        if hours is 1:
            lis.append("{} hour".format(hours))
        else:
            lis.append("{} hours".format(hours))
    if minutes is not 0:
        if minutes is 1:
            lis.append("{} minute".format(minutes))
        else:
            lis.append("{} minutes".format(minutes))
    if secleft is not 0:
        if secleft is 1:
            lis.append("{} second".format(secleft))
        else:
            lis.append("{} seconds".format(secleft))

    if len(lis) is 1:
        return lis[0]
    if len(lis) is 2:
        return "{} and {}".format(lis[0], lis[1])
    if len(lis) is 3:
        return "{}, {} and {}".format(lis[0], lis[1], lis[2])
    if len(lis) is 4:
        return "{}, {}, {} and {}".format(lis[0], lis[1], lis[2], lis[3])
    if len(lis) is 5:
        return "{}, {}, {}, {} and {}".format(lis[0], lis[1], lis[2], lis[3], lis[4])
    else:
        return "something has gone wrong in this massive mess.........."
