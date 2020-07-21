### Importing modules
import time
import csv

import numpy as np
import pandas as pd

import tweepy
import nltk

##################################################################################################################################
# SCRAPING TWEETS
##################################################################################################################################

# Insert passwords for accessing Tweepy API
# consumer_key = "PASSCODE"
# consumer_secret = "PASSCODE"
# access_token = "PASSCODE"

# Uncomment next 2 lines to use API
# auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

# api = tweepy.API(auth, wait_on_rate_limit=True)


# Defining columns to insert into csv file
columns = ["Datetime", "TweetId", "Text", "FavouriteCount", "RetweetCount"]

### Created check loop to see whether title columns present in csv file
# Opening tweetsRAW.csv in reading mode
with open("tweetsRAW.csv", "r") as f:
    # Reading csv file
    csvReader = csv.reader(f, delimiter=",")
    # Creating 'for' loop to check if one of the column titles is present in the first row of the csv file
    # If columns present, 'columns present' is printed
    # If columns not present, csv file opened in write mode and columns added to first row
    for col in csvReader:
        if "FavouriteCount" in col[3]:
            print("columns present")
            break
        else:
            with open("tweetsRAW.csv", "w") as h:
                csvWritercol = csv.writer(h)
                csvWritercol.writerow(columns)
                print("columns added")
                break
            h.close()
f.close()

# Opening tweetsRAW.csv in append mode
csvFile = open("tweetsRAW.csv", "a")
csvWriter = csv.writer(csvFile)

### Creating a function to scrape tweets
def tweet_scraper(text_query, date_since, numTweets, numRuns):
    """
    Name:
    tweet_scraper

    Description:
    This function will scrape tweets which include words matching the text query using Tweepy API over a specified no. of runs from a specified date.

    Keyword Arguments:
    text_query -- Word searching for 
    date_since -- Limit: tweets can only be maximum 7 days old
    numTweets -- Number of Tweets to search for per iteration. Recommended amount: 2500.
    numRuns -- Number of iterations API is run. After each iteration, there is 15 minute sleep time.

    Returns:
    csvFIle -- csv file with appended values for Tweet Created Date/Time, ID, Text, FavouriteCount and RetweetCount.
    """
    print("Starting scraping!")

    # Creating 'for' loop to iterate cursor API attribute numRuns times
    for iteration in enumerate(range(0, numRuns)):
        print("This is iteration", iteration)

        # Tweepy cursor method to search for tweets.
        for tweet in tweepy.Cursor(
            api.search, q=text_query, lang="en", since=date_since, tweet_mode="extended"
        ).items(numTweets):
            # Removing retweets and replies from fetched tweets
            if (
                (not tweet.retweeted)
                and ("RT @" not in tweet.full_text)
                and ("@" not in tweet.full_text)
            ):
                # Writing tweets to CSV file
                csvWriter.writerow(
                    (
                        [
                            tweet.created_at,
                            tweet.id,
                            tweet.full_text,
                            tweet.favorite_count,
                            tweet.retweet_count,
                        ]
                    )
                )

        # Limit to number of tweets retrievable in 15 mins so pausing loop for another 15 mins to refresh API
        time.sleep(920)

    # CLosing csv File and letting user know function is complete
    csvFile.close()

    print("This search query is complete.")


### Creating function to remove any tweets which have been repeated in tweetsRAW.csv when scrapedtweets was called
def remove_repeated_tweets(tweets_csv_file):
    """
    Name: 
    remove_repeated_tweets
    
    Description: 
    This function will remove tweets which have been repeated or are not unique in a csv file of tweets and will create a new csv file of original tweets.

    Keyword Argument:
    tweets_csv_file -- specify csv file which contains information about tweets (e.g. tweet text). Place csv file in "".

    Returns:
    csvFIle -- csv file with repeated tweets removed.
    """
    # Creating empty array to store information about tweets
    tweetChecklist = []

    # Creating Pandas dataframe of tweets_csv_file
    tweetsRAWdf = pd.read_csv(tweets_csv_file, error_bad_lines=False)

    # Extracting all the values of tweets_csv_file into a list
    data_tweet_text_list = tweetsRAWdf["Text"].T.values.tolist()

    # Creating 'for' loop to check if tweets are repeated. If tweet not repeated, tweet appended to tweetChecklist.
    for current_tweet in data_tweet_text_list:
        if current_tweet not in tweetChecklist:
            tweetChecklist.append(current_tweet)

    # Storing unique tweets into pandas dataframe
    updatedtweetsdf = pd.DataFrame(data=tweetChecklist, columns=["Text"])

    # Converting pandas dataframe into csv
    updatedtweetsdf.to_csv("Scraped-Tweets.csv", index=False)

    print("Repeated tweets have been removed!")


# Defining filters for search query
text_query = "Arsenal OR #ARSENAL OR #Arsenal"
numTweets = 2500
numRuns = 6
date_since = "2020-07-12"

# Calling tweet scraper, uncomment below line to run.
# tweet_scraper(text_query, date_since, numTweets, numRuns)

# Removing repeated tweets, uncomment below line to run.
# remove_repeated_tweets("tweetsRAW.csv")


##################################################################################################################################
# STARTING SENTIMENT ANALYSIS
##################################################################################################################################

