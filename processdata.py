import re
import nltk
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
def process(data):
    device = ''
    frstchar = data[0]
    if frstchar == '[':
        device = 'ios'
    else:
        device = 'android'

    if device == 'ios':
        pattern = r'\[(\d{2}/\d{2}/\d{2}, \d{2}:\d{2}:\d{2})\] (\w+\s\w+): (.+?)$'
        matches = re.findall(pattern, data, re.MULTILINE)
        dates = [match[0] for match in matches]
        senders = [match[1] for match in matches]
        messages = [(match[2]) for match in matches]
        df = pd.DataFrame({'gdate': dates, 'User': senders, 'Message': messages})
        yc = df['gdate'].str.extract(r'/((\d{2})/(\d{2,4}))')[2]
        mc = df['gdate'].str.extract(r'/((\d{2})/(\d{2,4}))')[1]
        for x in mc:
            flag = 0
        if (int(x) > 12):
            flag = 1
        if flag == 1:
            if (len(yc[0]) == 4):
                formatt = '%d/%m/%y, %I:%M:%S'
            else:
                formatt = '%d/%m/%y, %I:%M:%S'
        else:
            if (len(yc[0]) == 4):
                formatt = '%d/%m/%y, %I:%M:%S'
            else:
                formatt = '%d/%m/%y, %I:%M:%S'
        df["Date"] = pd.to_datetime(df['gdate'], format=formatt, errors='coerce')
        df.drop(columns=['gdate'], inplace=True)
    else:
        pattern = '\d{2}/\d{2}/(?:\d{2}|\d{4}),\s\d{1,2}:\d{2}\s(?:AM|PM|am|pm)\s-\s'
        msg = re.split(pattern, data)[3:]
        dates = re.findall(pattern, data)[2:]
        df = pd.DataFrame({'User_message': msg, 'gdate': dates})
        df['gdate'] = df['gdate'].str.replace('\u202f', ' ')
        yc = df['gdate'].str.extract(r'/((\d{2})/(\d{2,4}))')[2]
        mc = df['gdate'].str.extract(r'/((\d{2})/(\d{2,4}))')[1]
        for x in mc:
            flag = 0
            if (int(x) > 12):
                flag = 1
        if flag == 1:
            if (len(yc[0]) == 4):
                formatt = '%m/%d/%Y, %I:%M %p - '
            else:
                formatt = '%m/%d/%y, %I:%M %p - '
        else:
            if (len(yc[0]) == 4):
                formatt = '%d/%m/%Y, %I:%M %p - '
            else:
                formatt = '%d/%m/%y, %I:%M %p - '
        df["Date"] = pd.to_datetime(df['gdate'], format=formatt, errors='coerce')
        df.drop(columns=['gdate'], inplace=True)

        user = []
        messages = []

        for message in df['User_message']:
            entry = re.split('([\w\W]+?):\s', message)
            if entry[1:]:
                user.append(entry[1])
                messages.append(entry[2])
            else:
                user.append('group_notification')
                messages.append(entry[0])

        df["User"] = user
        df["Message"] = messages

        df.drop(columns=['User_message'], inplace=True)
        df = df[df['User'] != 'group_notification']
        df.reset_index(drop=True, inplace=True)

    df["Year"] = df["Date"].dt.year
    df["month"] = df["Date"].dt.month
    df["date"] = df["Date"].dt.date
    df["Month"] = df["Date"].dt.month_name()
    df["Day"] = df['Date'].dt.day_name()
    df["Datee"] = df["Date"].dt.day
    df["Hour"] = df["Date"].dt.hour
    df["Minute"] = df["Date"].dt.minute

    sentiments = SentimentIntensityAnalyzer()
    df["positive"] = [sentiments.polarity_scores(i)["pos"] for i in df["Message"]]
    df["negative"] = [sentiments.polarity_scores(i)["neg"] for i in df["Message"]]
    df["neutral"] = [sentiments.polarity_scores(i)["neu"] for i in df["Message"]]

    period = []
    for hour in df[['Day', 'Hour']]['Hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['Period'] = period

    return df
