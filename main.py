import re
import pandas as pd
import datetime
from datetime import *

def preprocess(data):
    pattern = "\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{2}\s\w{2}\s-\s"

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_messages': messages, 'messages_date': dates})
    df['messages_date'] = df['messages_date'].str.replace("-", "")
    ##df['messages_date'] = pd.to_datetime(df['messages_date'],format="%m/%d/%y, %H:%M -")
    df["timestamp"] = df['messages_date'].str[-10:-1]
    df.rename(columns={"messages_date": "date"}, inplace=True)

    users = []
    messages = []
    for message in df["user_messages"]:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2:])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['users'] = users
    df['message'] = messages

    p = '(\d{1,2}/\d{1,2}/\d{2}),\s'
    dates = []
    for i in df["date"]:
        entry = re.split(p, i)
        if entry[1:]:
            dates.append(entry[1])
    df["date_new"] = dates

    df["date_new"] = pd.to_datetime(df['date_new'], format="%m/%d/%y")
    df["year"] = df["date_new"].dt.year
    df["month"] = df["date_new"].dt.month_name()
    df["day"] = df["date_new"].dt.day
    df["day_name"] = df["date_new"].dt.day_name()
    df["timestamp_new"] = pd.to_datetime(df['timestamp'], errors='coerce').dt.time
    df["message"] = df["message"].astype(str)

    df["message"] = df["message"].str.replace("[", "")
    df["message"] = df["message"].str.replace("]", "")
    df["message"] = df["message"].str.replace("[\n]", "")
    df["message"].replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=["", ""], regex=True, inplace=True)
    df["message"] = df["message"].str.replace("'", "")
    df["month_num"] = df["date_new"].dt.month
    df = df[["users", "date", "date_new", "timestamp", "timestamp_new", "message", "year", "month", "day","month_num", "day_name"]]
    return df

