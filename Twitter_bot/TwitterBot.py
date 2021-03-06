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
#--------------------------------------------------------------------------------------
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


#****************************************************************************************
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
    
#****************************************************************************************

# get key word dict
def gettarget_user():
    searchlist = search_newKeyWord('@DraculaisLaifu')
    comparList  = comparison_mention()

    target_users = {}
    
    for keys, val in searchlist.items():
        if keys not in comparList:
            target_users[keys] = val
    return target_users    
    
#****************************************************************************************
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
#****************************************************************************************

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

#***************************************************************************************************

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
    

#*******************************************************************************************************
# create a transitional function makedict that conbine targetuser and length of dataframe we just created into a dict for a loop later
target_list = target_users
def makedict (target_list, dataFrameDict):
    
    nameDict = dict(zip(target_users,  range(0, len(dataFrameDict) +1)))
    
    return nameDict

#**************************************************************************
target_list = target_users
def makedict2 (mentioner, dataFrameDict , target_list):
    
    x = dict(zip(target_users,  mentioner))
    d = {}
    for i in range(0, len(x)):
        d[i] = x
    return d
# --------------------------------------------start plotting and analysis------------------------------------------------------

# now combine the makedict () function - for loop, and plottingaway() to save the plots into list visual
targetdict = gettarget_user()
target_users= []
mentioner = []
for key, val in targetdict.items():
    target_users.append(key)
    mentioner.append(val)
 
    
dictionarylist = convertToDataFrame(target_users)
target_list = target_users
mentioners = mentioner
visual = []
for keys, vals in makedict(target_list, dictionarylist).items():
    plot = plottingaway(vals, dictionarylist , keys)
    print(plot)
    visual.append(plot)
    
    
# ----------------------sentimental analysis sent out--------------------------------
# send those two saved graph into my new account #Draculalaifu
for key, val in (list(y.values())[0]).items():
    Api.update_with_media("Sentiment Analysis {}.png".format(key),
            "New Tweet Analysis: @{} ".format(key) + "(Thx @{} )".format(val))
    now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print(f"Sucessfully send analysis at {now}")
    
    time.sleep(5)