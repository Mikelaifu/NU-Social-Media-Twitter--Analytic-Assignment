
## Explnation: 
    
In this project: I create a twitter bot(as a twitter monitoring system to spider the newst request(any mention "@DraculaisLaifu" sent from different account in thr format of "hi @DraculaisLaifu, can you analyze " @anything" ; then extract data from @anything for sentimental analysis and plot the analysis then send the graph into analysis account @DraculaisLaifu.

for example displaying: I tweeted about those key account:

@GeminiDotCom,
@coinbase,
@binance_2017,
@krakenfx,
@Bitcoin,
@CBSTweet,
@CBSSports,
@theGRAMMYs,
@TheAcademy,
@netflix,


```python
import tweepy
import pandas as pd
import matplotlib.pyplot as plt
import time
from time import gmtime, strftime
import random
import numpy 
import json
import requests
import numpy as np
import datetime
from pprint import pprint
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
```


```python
from config import (consumer_key, 
                    consumer_secret, 
                    access_token, 
                    access_token_secret)

from config2 import (Consumer_key, 
                    Consumer_secret, 
                    Access_token, 
                    Access_token_secret)

# Setup Tweepy API1 Authentication (first account)
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

# set up Tweepy API2 Authentication(2nd account)
auth = tweepy.OAuthHandler(Consumer_key, Consumer_secret)
auth.set_access_token(Access_token, Access_token_secret)
Api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
```


```python
api.update_status("Hi @DraculaisLaifu, please analyze @netflix !" )
```




    {'contributors': None,
     'coordinates': None,
     'created_at': 'Wed Mar 14 22:16:16 +0000 2018',
     'entities': {'hashtags': [],
      'symbols': [],
      'urls': [],
      'user_mentions': [{'id': 973375514982350851,
        'id_str': '973375514982350851',
        'indices': [3, 18],
        'name': 'Mike Wu',
        'screen_name': 'DraculaisLaifu'},
       {'id': 16573941,
        'id_str': '16573941',
        'indices': [35, 43],
        'name': 'Netflix US',
        'screen_name': 'netflix'}]},
     'favorite_count': 0,
     'favorited': False,
     'geo': None,
     'id': 974046582734774272,
     'id_str': '974046582734774272',
     'in_reply_to_screen_name': None,
     'in_reply_to_status_id': None,
     'in_reply_to_status_id_str': None,
     'in_reply_to_user_id': None,
     'in_reply_to_user_id_str': None,
     'is_quote_status': False,
     'lang': 'en',
     'place': None,
     'retweet_count': 0,
     'retweeted': False,
     'source': '<a href="https://github.com/Mikelaifu" rel="nofollow">NUTwitterAPITesting</a>',
     'text': 'Hi @DraculaisLaifu, please analyze @netflix !',
     'truncated': False,
     'user': {'contributors_enabled': False,
      'created_at': 'Wed Sep 06 16:15:33 +0000 2017',
      'default_profile': True,
      'default_profile_image': False,
      'description': '#Tech #Music #Artificialintelligence',
      'entities': {'description': {'urls': []}},
      'favourites_count': 30,
      'follow_request_sent': False,
      'followers_count': 47,
      'following': False,
      'friends_count': 77,
      'geo_enabled': True,
      'has_extended_profile': False,
      'id': 905464497481015296,
      'id_str': '905464497481015296',
      'is_translation_enabled': False,
      'is_translator': False,
      'lang': 'en',
      'listed_count': 0,
      'location': 'Chicago, IL',
      'name': 'MikeWDalmatian',
      'notifications': False,
      'profile_background_color': 'F5F8FA',
      'profile_background_image_url': None,
      'profile_background_image_url_https': None,
      'profile_background_tile': False,
      'profile_banner_url': 'https://pbs.twimg.com/profile_banners/905464497481015296/1504742367',
      'profile_image_url': 'http://pbs.twimg.com/profile_images/915323782243504134/k_OFLQKM_normal.jpg',
      'profile_image_url_https': 'https://pbs.twimg.com/profile_images/915323782243504134/k_OFLQKM_normal.jpg',
      'profile_link_color': '1DA1F2',
      'profile_sidebar_border_color': 'C0DEED',
      'profile_sidebar_fill_color': 'DDEEF6',
      'profile_text_color': '333333',
      'profile_use_background_image': True,
      'protected': False,
      'screen_name': 'mikewdalmatian',
      'statuses_count': 37,
      'time_zone': None,
      'translator_type': 'none',
      'url': None,
      'utc_offset': None,
      'verified': False}}




```python
# account
def search_newKeyWord(keyword):
    public_tweet = Api.search(keyword, count = 10, results_type = "recent")

    searchlist = {}
#     mention =[]
#     username = []
    if public_tweet['statuses']:
        
        for tweet in public_tweet['statuses']:
            mention =tweet['entities']['user_mentions'][1]['screen_name']
            username = tweet['user']['screen_name']
            
            searchlist[mention] = username
    
    return searchlist


# account 2
def comparison_mention() :
    
    public_tweet = Api.home_timeline(count = 30)

    comparList = []
 
    for tweet in public_tweet:
        
        #pprint(tweet)
        if tweet['entities']['user_mentions']:
            
            com_mention = tweet['entities']['user_mentions'][0]['screen_name']
            
            comparList.append(com_mention)
    
    return comparList
    
    
    
```


```python
search_newKeyWord('@DraculaisLaifu')

```




    {'Bitcoin': 'mikewdalmatian',
     'CBSSports': 'mikewdalmatian',
     'krakenfx': 'mikewdalmatian',
     'netflix': 'mikewdalmatian'}




```python
comparison_mention()
```




    ['GeminiDotCom', 'binance_2017']




```python
# 
def gettarget_user():
    searchlist = search_newKeyWord('@DraculaisLaifu')
    comparList  = comparison_mention()

    target_users = {}
    
    for keys, val in searchlist.items():
        if keys not in comparList:
            target_users[keys] = val
    return target_users

```


```python
gettarget_user()
```




    {'Bitcoin': 'mikewdalmatian',
     'CBSSports': 'mikewdalmatian',
     'krakenfx': 'mikewdalmatian',
     'netflix': 'mikewdalmatian'}




```python

# define a function that return the the dictionary conatin wanted info 
def NewsOrg_sentiment(target):

    counter = 1
    sentiments = []

    public_tweet = api.user_timeline(target, count = 500 )
    
    for tweet in public_tweet :
        
        results = analyzer.polarity_scores(tweet["text"])
        compound = results["compound"]
        tweets_ago = counter
        
        sentiments.append({
            "twitter source account" : target,
            "Compound" : compound,
            "Tweets ago" : tweets_ago,
        })
            
        
        counter = counter + 1
        
    return sentiments
```


```python
# create a function convertToDataFrame() that convert the dictionary into dataframe and save those dataframe into a list dataFrameDict
# target_users = ['@BBC'] #--- need to substitude by a function here to retrun hte target_user list 

def convertToDataFrame(target_users):
    
    dataFrameDict = []
    
    for target in target_users:
        
        sentiments = NewsOrg_sentiment(target)
        
        dataFrameDict.append({
        target: pd.DataFrame.from_dict(sentiments)
    })

    return dataFrameDict
    
```


```python

# create a funcion plottingaway() to use matplotlib to plot needed data 
def plottingaway(index, dictionarylist, target):
    plt.plot(dictionarylist[index][target]["Tweets ago"], dictionarylist[index][target]["Compound"], 
                             c = 'b', linewidth = 0.2, marker = "o", alpha = 0.5)

    plt.title("Sentiment Analysis of Tweets for {}".format(target))
    plt.ylabel("Tweet Polarity")
    plt.xlabel("Tweets Ago")
    plt.savefig("Sentiment Analysis {}.png".format(target))
    name = "Sentiment Analysis {}.png".format(target)
    print(name)
    
    return plt.plot(dictionarylist[index][target]["Tweets ago"], dictionarylist[index][target]["Compound"], 
                             c = 'b', linewidth = 0.2, marker = "o", alpha = 0.5)
    
```


```python
# create a transitional function makedict that conbine targetuser and length of dataframe we just created into a dict for a loop later
target_list = target_users
def makedict (target_list, dataFrameDict):
    
    nameDict = dict(zip(target_users,  range(0, len(dataFrameDict) +1)))
    
    return nameDict
```


```python
target_list = target_users
def makedict2 (mentioner, dataFrameDict , target_list):
    
    x = dict(zip(target_users,  mentioner))
    d = {}
    for i in range(0, len(x)):
        d[i] = x
    return d
```


```python
targetdict = gettarget_user()
target_users= []
mentioner = []
for key, val in targetdict.items():
    target_users.append(key)
    mentioner.append(val)
 
    
dictionarylist = convertToDataFrame(target_users)
target_list = target_users

visual = []
for keys, vals in makedict(target_list, dictionarylist).items():
    plot = plottingaway(vals, dictionarylist , keys)
    print(plot)
    visual.append(plot)
    

```

    Sentiment Analysis isDARTHVADER.png
    [<matplotlib.lines.Line2D object at 0x113cd0160>]
    Sentiment Analysis netflix.png
    [<matplotlib.lines.Line2D object at 0x113cd0240>]
    Sentiment Analysis CBSSports.png
    [<matplotlib.lines.Line2D object at 0x11e8f8940>]
    Sentiment Analysis krakenfx.png
    [<matplotlib.lines.Line2D object at 0x11e9d1128>]
    Sentiment Analysis Bitcoin.png
    [<matplotlib.lines.Line2D object at 0x11ec4df60>]



```python
target_list = target_users
mentioner = mentioner
y = makedict2 (mentioner, dataFrameDict , target_list)

list(y.values())[0]
```




    {'Bitcoin': 'mikewdalmatian',
     'CBSSports': 'mikewdalmatian',
     'isDARTHVADER': 'Orange_cc',
     'krakenfx': 'mikewdalmatian',
     'netflix': 'mikewdalmatian'}




```python

# for keyIndex in range(len(y)):
#     visual[keyIndex]
#     plt.show()
    
for key, val in (list(y.values())[0]).items():
    Api.update_with_media("Sentiment Analysis {}.png".format(key),
            "New Tweet Analysis: @{} ".format(key) + "(Thx @{} )".format(val))
    now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print(f"Sucessfully send analysis at {now}")
    
    time.sleep(5)
```
