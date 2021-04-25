from pygoogletranslation import Translator
import tweepy
import pandas as pd
import numpy as np
from wordcloud import WordCloud, STOPWORDS
import SentimentAnalyzer as vad
import DataCleaning as dc

consumer_key = '4CbZlBPw5KrXsa3O548z2FWje'
consumer_secret = 'Gdzs85HvKgNOj4gLILD7cySz1olX0uIHoxYpIF4GJ9CvF5pDVt'
access_key = '4800866562-EKKPjMQkOXY8xQmT4V7uawq5fPGBEibydQ56EtO'
access_secret = 'dhaOU2S4NbdkgV2DQwjHz683xsKoJFlg6pvLG2tmuYepr'


def initialize():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
    return api


def sentiment_analyzer_scores(text, engl=True):
    translator = Translator()
    analyser = vad.SentimentIntensityAnalyzer()
    if engl:
        trans = text
    else:
        trans = translator.translate(text).text
    score = analyser.polarity_scores(trans)
    return score


def word_cloud(wd_list):
    stopwords = set(STOPWORDS)
    all_words = ' '.join([text for text in wd_list])
    wordcloud = WordCloud(
        background_color='white',
        stopwords=stopwords,
        width=1600,
        height=800,
        random_state=21,
        colormap='jet',
        max_words=50,
        max_font_size=200).generate(all_words)
    wordcloud.to_file('word.png')


def getPositiveCount(list):
    cnt = 0
    for i in range(len(list)):
        if compound_list[i] > 0:
            cnt = cnt + 1
    return cnt


def getNeutralCount(list):
    cnt = 0
    for i in range(len(list)):
        if compound_list[i] == 0:
            cnt = cnt + 1
    return cnt


def getNegativeCount(list):
    cnt = 0
    for i in range(len(list)):
        if compound_list[i] < 0:
            cnt = cnt + 1
    return cnt


def isBully(list):
    avg_compound = np.mean(list)
    if avg_compound >= 0:
        return "Not Bully"
    else:
        return "Bully"


if __name__ == '__main__':
    api = initialize()
    t_handle = '@SenSanders'
    t_count = 100
    tweets = api.user_timeline(t_handle, count=t_count)
    sentiments = []
    for t in tweets:
        text = t["text"]
        sentiments.append({"User": t_handle,
                           "text": text,
                           "Date": t["created_at"]
                           })
    df = pd.DataFrame.from_dict(sentiments)
    df["text"] = dc.clean_tweets(df["text"])
    scores = []
    compound_list = []
    for i in range(df['text'].shape[0]):
        compound = sentiment_analyzer_scores(df['text'][i])["compound"]
        pos = sentiment_analyzer_scores(df['text'][i])["pos"]
        neu = sentiment_analyzer_scores(df['text'][i])["neu"]
        neg = sentiment_analyzer_scores(df['text'][i])["neg"]
        compound_list.append(compound)
        scores.append({"Positive": pos,
                       "Negative": neg,
                       "Neutral": neu,
                       "Compound": compound,
                       })
    sentiments_score = pd.DataFrame.from_dict(scores)
    df = df.join(sentiments_score)
    pd.options.display.max_columns = None
    pd.options.display.max_rows = None
    # print(df.head(100))
    word_cloud(df["text"])
    print(isBully(compound_list))
    print(getPositiveCount(compound_list))
    print(getNeutralCount(compound_list))
    print(getNegativeCount(compound_list))
