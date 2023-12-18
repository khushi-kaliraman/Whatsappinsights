import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
extract = URLExtract()

def omidf(df):
    temp = df[df['Message'] != '<Media omitted>\n']
    temp = temp[temp['User'] != 'group_notifications']
    temp = temp[~temp['Message'].str.contains('[0-9@#$%^&*()_+={}[\]:;<>,.?/\\|~-]')]
    return temp

def fetchdata(selecteduser, df):
    if selecteduser != 'Overall':
        df = df[df['User'] == selecteduser]

    num = df.shape[0]
    media = df[df['Message'] == '<Media omitted>\n'].shape[0]
    words = []
    links = []
    for message in df['Message']:
        words.extend(message.split())
    for message in df['Message']:
        links.extend(extract.find_urls(message))
    return num, len(words), media, len(links)
def mostbzy(df):
    x = df['User'].value_counts().head()
    ndf = round((df['User'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'Name', 'user': 'Percent'})
    return x, ndf

def actheat(selecteduser, df):
    if selecteduser != 'Overall':
        df = df[df['User'] == selecteduser]
    adf = df.pivot_table(index="Day", columns="Period", values="Message", aggfunc="count").fillna(0)
    return adf

def wordcloud(selecteduser, df):
    if selecteduser != 'Overall':
        df = df[df['User'] == selecteduser]
    f = open("stop_hinglish.txt", "r")
    stpwrds = f.read()
    temp = omidf(df)

    def remwords(msg):
        y =[]
        for word in msg.lower().split():
            if word not in stpwrds:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='Black')
    temp['Message'].apply(remwords)
    dfwc = wc.generate(temp['Message'].str.cat(sep=""))
    return dfwc
def mostwords(selecteduser, df):
    f = open("stop_hinglish.txt","r")
    stpwrds = f.read()
    if selecteduser != 'Overall':
        df = df[df['User'] == selecteduser]
    temp = omidf(df)
    words = []

    for msg in temp['Message']:
        for word in msg.lower().split():
            if word not in stpwrds:
                words.append(word)
    ndf = pd.DataFrame(Counter(words).most_common(25))
    wdf = ndf.rename(columns={0: 'Message', 1: 'Frequency'})
    return wdf

def poswords(selecteduser, df):
    f = open("stop_hinglish.txt", "r")
    stpwrds = f.read()
    if selecteduser != 'Overall':
        df = df[df['User'] == selecteduser]
    temp = omidf(df)
    temp = temp[temp["positive"]>0.8]

    words = []
    for msg in temp['Message']:
        for word in msg.lower().split():
            if word not in stpwrds:
                words.append(word)
    pdf = pd.DataFrame(Counter(words).most_common(25)).rename(columns={0: 'Word', 1: 'Frequency'})
    return pdf
def negwords(selecteduser, df):
    f = open("stop_hinglish.txt", "r")
    stpwrds = f.read()
    if selecteduser != 'Overall':
        df = df[df['User'] == selecteduser]
    temp = omidf(df)
    temp = temp[temp["negative"]>0.8]

    words = []
    for msg in temp['Message']:
        for word in msg.lower().split():
            if word not in stpwrds:
                words.append(word)
    ndf = pd.DataFrame(Counter(words).most_common(25)).rename(columns={0: 'Word', 1: 'Frequency'})
    return ndf

def mostpos(selecteduser, df):
    if selecteduser != 'Overall':
        df = df[df['User'] == selecteduser]
    temp = omidf(df)
    temp = temp[temp["positive"] > 0.8]
    x = temp['User'].value_counts().head()
    return x
def mostneg(selecteduser, df):
    if selecteduser != 'Overall':
        df = df[df['User'] == selecteduser]
    temp = omidf(df)
    temp = temp[temp["negative"] > 0.8]
    x = temp['User'].value_counts().head()
    return x
def monthlytime(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    timeline = df.groupby(['Year', 'month', 'Month']).count()['Message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + "-" + str(timeline['Year'][i]))
    timeline['Time'] = time
    return timeline

def dailytime(selecteduser,df):

    if selecteduser != 'Overall':
        df = df[df['User'] == selecteduser]
    dailytime = df.groupby('date').count()['Message'].reset_index()
    return dailytime
def dayweek(selectedu, df):
    if selectedu != 'Overall':
        df = df[df['User'] == selectedu]
    dayw = df['Day'].value_counts()
    return dayw
def monthy(selectedu, df):
    if selectedu != 'Overall':
        df = df[df['User'] == selectedu]
    my = df['Month'].value_counts()
    return my

def is_emoji(char):
    return 0x1F300 <= ord(char) <= 0x1F6FF or 0x2600 <= ord(char) <= 0x26FF or 0x2700 <= ord(char) <= 0x27BF
def emojianal(selecteduser, df):
    emojis = []
    for e in df['Message']:
        emojis.extend([c for c in e if is_emoji(c)])
        edf = pd.DataFrame(Counter(emojis).most_common(), columns=['Emoji', 'Count'], index=range(1, len(Counter(emojis)) + 1))
    return edf