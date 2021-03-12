import datetime
import json
from datetime import date 


def time_date_slots():
    times = ["7:00 AM - 9:00 AM","9:00 AM - 11:00 AM","11:00 AM - 1:00 PM","1:00 PM - 3:00 PM","3:00 PM - 5:00 PM","5:00 PM - 7:00 PM","7:00 PM - 10:00 AM"]

    todays_date = date.today() 

    numdays = 1000
    dateList = []

    for x in range (0, numdays):
        dateList.append(todays_date + datetime.timedelta(days = x))

    a_dict = {}

    for a in times:
        if "Court 1" in a_dict:
            a_dict["Court 1"].append(a)
        else:
            a_dict["Court 1"] = [a]

    for a in times:
        if "Court 2" in a_dict:
            a_dict["Court 2"].append(a)
        else:
            a_dict["Court 2"] = [a]

    for a in times:
        if "Court 3" in a_dict:
            a_dict["Court 3"].append(a)
        else:
            a_dict["Court 3"] = [a]


    nl = []

    for a in dateList:
        #nl.append(str(a))
        nl.append(a)
        

    d = dict.fromkeys(nl, a_dict)
    return d