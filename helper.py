from urlextract import URLExtract
from wordcloud import wordcloud, WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()
def fetch_stats(choice,df):
    if choice != 'Overall':
        df = df[df['name'] == choice]
    # 1.number of messages
    num_messages = df.shape[0]
    # 2.number of words
    words = []
    for i in df['msg']:
        words.extend(i.split())
    #3.number of media messages
    num_media_messages=df[df['msg'] == '<Media omitted>'].shape[0]
    #4.numbers of links
    links=[]
    for i in df['msg']:
        links.extend(extract.find_urls(i))
    return num_messages, len(words) ,num_media_messages, len(links)

def most_active_users(df):
    x = df['name'].value_counts().head()
    df = round((df['name'].value_counts() / df.shape[0]) * 100,2).reset_index().rename(columns={'index':'names','name':'percent'})
    return x,df
def filter_msg(df):
    temp = df[df['msg'] != '<Media omitted>']
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    words = []

    for i in temp['msg']:
        for j in i.lower().split():
            if j not in stop_words:
                if not j.startswith('https://') and '"' not in j:
                    words.append(j)
    return words
def create_wordcloud(choice,df):
    if choice != 'Overall':
        df = df[df['name'] == choice]

    words = filter_msg(df)
    text = ' '.join(words)

    wc =WordCloud(width=500,height=500,min_font_size = 10,background_color='white')
    df_wc = wc.generate(text)

    return df_wc
def most_common_words(choice,df):

    if choice != 'Overall':
        df = df[df['name'] == choice]

    words = filter_msg(df)
    most_common_df = pd.DataFrame(Counter(words).most_common(20),columns=['Words','Count'])

    return most_common_df
def emoji_counter(choice,df):
    if choice != 'Overall':
        df = df[df['name'] == choice]
    emojis = []

    for msg in df['msg']:
        emojis.extend([i for i in msg if i in emoji.EMOJI_DATA])

    emoji_counts = Counter(emojis)
    emoji_df = pd.DataFrame(emoji_counts.most_common(10), columns=['Emoji', 'Count'])

    return emoji_df

def monthly_timeline(choice,df):
    if choice != 'Overall':
        df = df[df['name'] == choice]

    timeline = df.groupby(['Year','Month_num','Month']).count()['msg'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i]+'-'+str(timeline['Year'][i]))
    timeline['Time'] = time
    return timeline

def week_activity_map(choice,df):
    if choice != 'Overall':
        df = df[df['name'] == choice]
    return df['Day_name'].value_counts()

def month_activity_map(choice,df):
    if choice != 'Overall':
        df = df[df['name'] == choice]
    return df['Month'].value_counts()

def activity_heatmap(choice,df):
    if choice != 'Overall':
        df = df[df['name'] == choice]

    heatmap=df.pivot_table(index = 'Day_name',columns = 'period', values = 'msg' , aggfunc = 'count').fillna(0)
    return heatmap