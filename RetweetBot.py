import tweepy
import datetime
import json
import time
from Configuration import Configuration

# Load up configuration file
config = Configuration()

# Set up the authorization tokens
auth = tweepy.OAuthHandler(config.key, config.secret_key)
auth.set_access_token(config.token, config.secret_token)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Print information about myself
me = api.me()
print('\nName: ' + str(me.name))
print('Twitter Handle: @' + str(me.screen_name))
print('ID:' + str(me.id))
print('User Info: \n' + str(me._json))
print('------------------------------------------------------------------------------------------------------\n')

queries = config.queries
tweets_queried = config.tweets_queried
max_total_retweeted = config.retweets_per_break

# # timers
step_pause = config.step_pause
retweet_period = config.retweet_period
break_time = config.break_time
end_of_queries_pause = config.end_of_queries_pause

total_retweeted = 0

class RetweetBot:
    def __init__(self, config):
        print('Initializing RetweetBot...')

while True:
    for query in queries:
        for tweet in tweepy.Cursor(api.search, query).items(tweets_queried):
            if total_retweeted > max_total_retweeted:
                print('I\'ve made 5 retweets! Taking a short break!')
                print(datetime.datetime.now())
                time.sleep(break_time) # 15 minute break
                total_retweeted = 0
                print('back to work!')
                break

            try:
                status_str = json.dumps(tweet._json)
                print(tweet.text)
                if api.get_user(tweet.user.id).id == me.id:
                    print('It\'s me! Ignoring me!')
                    time.sleep(step_pause)
                else:
                    if api.get_status(tweet.id).retweeted:
                        print('I\'ve retweeted this! Ignoring!')
                        time.sleep(step_pause)
                    else:
                        tweet.retweet()
                        print('Retweeted! - ID: ' + str(tweet.id) + ' | User:' + str(tweet.user.name)
                              + ' | UserID:' + str(tweet.user.id) + ' | Status: ' + str(tweet.text))
                        total_retweeted = total_retweeted + 1

                        time.sleep(retweet_period)  # Let's make this 30 secs

                print('-------------------------------------------------------------------')

            except tweepy.TweepError as e:
                print(e.reason)
            except StopIteration:
                break

    print('break time!')
    print(datetime.datetime.now())
    time.sleep(end_of_queries_pause)
    print('back to work!')