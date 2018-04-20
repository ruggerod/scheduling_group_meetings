from datetime import datetime, timedelta
import pandas as pd
from copy import deepcopy


def load_initial_schedule():
    schedule = pd.DataFrame(columns=('Date', 'Topic', 'Speaker'))
    with open("initial_schedule.dat", "r") as f:
        for n, line in enumerate(f):
            entries = filter(bool, line.split("  "))
            if entries[1][0] == ' ':
                date = entries[1][1:]
            else:
                date = entries[1]
            schedule.loc[n] = ([datetime.strptime(date, '%Y-%m-%d'),
                                entries[2],
                                entries[3].replace("\n", "")])
    return schedule


def save_schedule(schedule, from_date=pd.Timestamp('today')):
    """
    Overwrite schedule on file 'updated_schedule.dat'.

    Parameters
    ----------
        schedule, pd.DataFrame
            Represents the updated group meeting's schedule
        from_date, pd.Timestamp (optional)
            Specifies the initial date of the schedule
    """
    with open("updated_schedule.dat", "w") as f:
        print >>f, schedule[schedule["Date"] >= from_date]


def shift_meetings(original_schedule, date):
    """
    Shifts the meeting scheduled for date
    (and the following meetings) by 1 week.

    Parameters
    ----------
        original_schedule, pd.DataFrame
            Represents the up-to-date group meeting's schedule
        date, str
            Date to erase. Use format "dd-mm-yyyy"

    Returns
    -------
        schedule, pd.Dataframe
            Represents the modified version of the group meeting
    """
    schedule = deepcopy(original_schedule)  # copy for this function
    date_to_del = pd.Timestamp(date[6:10] + "-" + date[3:5] + "-" + date[0:2])
    if not any(date_to_del == schedule['Date']):
        raise ValueError("Invalid date!")

    indx = schedule.index[date_to_del == schedule['Date']][0]
    schedule.loc[indx:, 'Date'] = schedule['Date'][indx:] + timedelta(7)
    return schedule


def switch_speakers(original_schedule, d1, d2):
    """
    Switch dates for two speakers

    Parameters
    ----------
        original_schedule, pd.DataFrame
            Represents the up-to-date group meeting's schedule
        date, str
            Date to erase. Use format "dd-mm-yyyy"

    Returns
    -------
        schedule, pd.Dataframe
            Represents the modified version of the group meeting
    """
    schedule = deepcopy(original_schedule)  # copy for this function
    d1_to_sw = pd.Timestamp(d1[6:10] + "-" + d1[3:5] + "-" + d1[0:2])
    d2_to_sw = pd.Timestamp(d2[6:10] + "-" + d2[3:5] + "-" + d2[0:2])
    if not any(d1_to_sw == schedule['Date']):
        raise ValueError("Invalid first date!")
    if not any(d2_to_sw == schedule['Date']):
        raise ValueError("Invalid second date!")

    indx1 = schedule.index[d1_to_sw == schedule['Date']][0]
    indx2 = schedule.index[d2_to_sw == schedule['Date']][0]
    # switch
    temp = schedule['Speaker'][indx1]
    schedule.loc[indx1, 'Speaker'] = schedule['Speaker'][indx2]
    schedule.loc[indx2, 'Speaker'] = temp
    return schedule
