import tweepy
import datetime
import time

class RetweetBot:
    def __init__(self, config):
        print('Initializing RetweetBot...')

        # Set up the authorization tokens
        auth = tweepy.OAuthHandler(config.key, config.secret_key)
        auth.set_access_token(config.token, config.secret_token)
        self.api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        # Load master controls user
        self._master = self.api.get_user(config.master_screen_name)
        self._master_id = config.master_user_id
        self._master_password = config.master_password

        # Debug On/Off?
        self._debug_mode = config.debug_mode

        # Load queries
        self.queries = config.queries
        self.tweets_queried = config.tweets_queried
        self.max_total_retweeted = config.retweets_per_break

        # # timers
        self.step_pause = config.step_pause
        self.retweet_period = config.retweet_period
        self.break_time = config.break_time
        self.end_of_queries_pause = config.end_of_queries_pause

        # Print information about myself
        self.me = self.api.me()
        print('\nName: ' + str(self.me.name))
        print('Twitter Handle: @' + str(self.me.screen_name))
        print('ID:' + str(self.me.id))
        # print('User Info: \n' + str(self.me._json))
        # print('------------------------------------------------------------------------------------------------------\n')

    def run(self):
        if self._debug_mode:
            print("Debug Mode: ON")
        # self._check_mail()
        self._retweet()

    def _check_mail(self):
        # Get list of mails
        try:
            message_list = self.api.list_direct_messages()
        except tweepy.TweepError as error:
            print(error.reason)

        owner_messages = []
        for message in message_list:
            if message.message_create['sender_id'] == self._master_id:
                owner_messages.append(message)
            # Debug only
            if self._debug_mode:
                print(message)


        # Get Messages only by Owner with password


        # Check mail sender and passwords

        # Read Mail

        # Perform actions and update


    def _retweet(self):
        total_retweeted = 2
        while True:
            for query in self.queries:
                for tweet in tweepy.Cursor(self.api.search, query).items(self.tweets_queried):
                    if total_retweeted > self.max_total_retweeted:
                        print('I\'ve made 5 retweets! Taking a short break!')
                        print(datetime.datetime.now())
                        time.sleep(self.break_time) # 15 minute break
                        total_retweeted = 0
                        print('back to work!')
                        break

                    try:
                        print(tweet.text)
                        if self.api.get_user(tweet.user.id).id == self.me.id:
                            print('It\'s me! Ignoring me!')
                            time.sleep(self.step_pause)
                        else:
                            if self.api.get_status(tweet.id).retweeted:
                                print('I\'ve retweeted this! Ignoring!')
                                time.sleep(self.step_pause)
                            else:
                                tweet.retweet()
                                print('Retweeted! - ID: ' + str(tweet.id) + ' | User:' + str(tweet.user.name)
                                      + ' | UserID:' + str(tweet.user.id) + ' | Status: ' + str(tweet.text))
                                total_retweeted = total_retweeted + 1

                                time.sleep(self.retweet_period)  # Let's make this 30 secs

                        print('-------------------------------------------------------------------')

                    except tweepy.TweepError as e:
                        print(e.reason)
                    except StopIteration:
                        break

            print('break time!')
            print(datetime.datetime.now())
            time.sleep(self.end_of_queries_pause)
            print('back to work!')
