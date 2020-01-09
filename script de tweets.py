from __future__ import print_function
import tweepy
import json
from pymongo import MongoClient

WORDS = ['#Ecuador']

CONSUMER_KEY = "HvCg23VwyIGwnVe5krvHKuZGO"
CONSUMER_SECRET = "KUwAEDDqogw0xlHr1LQiaECD4q42gpFRPkUS0NLHZm51Y9gMRF"
ACCESS_TOKEN = "115946548-x5JL2LFNp26y2t0WlBvQE7GirkGeNZUaYLUM1GGL"
ACCESS_TOKEN_SECRET = "ul2Q4nw9112ATj4iyFu2VIj12IElGb0GRIr3wBnBPxBAE"


class StreamListener(tweepy.StreamListener):
    #This is a class provided by tweepy to access the Twitter Streaming API.

    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("Conectado a la API de transmision")

    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        print('Error: ' + repr(status_code))
        return False

    def on_data(self, data):
        #This is the meat of the script...it connects to your mongoDB and stores the tweet
        try:
            client = MongoClient("mongodb://jhoel1:SuxKg986DNxTfxjH@mongodb01-shard-00-01-bphud.mongodb.net:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass%20Community&ssl=true")

            # Use twitterdb database. If it doesn't exist, it will be created.
            db = client.base1

            # Decode the JSON from Twitter
            datajson = json.loads(data)

            #grab the 'created_at' data from the Tweet to use for display
            created_at = datajson['created_at']

            #print out a message to the screen that we have collected a tweet
            print("Tweet collected at " + str(created_at))

            #insert the data into the mongoDB into a collection called twitter_search
            #if twitter_search doesn't exist, it will be created.
            db.collection1.insert(datajson)
        except Exception as e:
           print(e)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
#Set up the listener. The 'wait_on_rate_limit=True' is needed to help with Twitter API rate limiting.
listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True))
streamer = tweepy.Stream(auth=auth, listener=listener)
print("Tracking: " + str(WORDS))
streamer.filter(track=WORDS)