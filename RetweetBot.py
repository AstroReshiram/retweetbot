import tweepy
import datetime
import time

class RetweetBot:
    def __init__(self, config):
        print('Initializing RetweetBot...')

        # Set up the authorization tokens
        auth = tweepy.OAuthHandler(config.key, config.secret_key)
        auth.set_access_token(config.token, config.secret_token)
        self.api = tweepy.API(auth, wait_on_rate_limit=True)

        # Load master controls user
        self._master = self.api.get_user(screen_name=config.master_screen_name)
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
        self.me = self.api.verify_credentials()
        print('\nName: ' + str(self.me.name))
        print('Twitter Handle: @' + str(self.me.screen_name))
        print('ID:' + str(self.me.id))
        # print('User Info: \n' + str(self.me._json))
        # print('------------------------------------------------------------------------------------------------------\n')

    def run(self):
        if self._debug_mode:
            print("Debug Mode: ON")
        # self._check_mail()
        self._block_list = self.api.get_blocked_ids()
        self._retweet()

    def _check_mail(self):
        # Get list of mails
        try:
            message_list = self.api.get_direct_messages()
            owner_messages = []

            # Find and use only messages from the master owner
            if message_list:
                for message in message_list:
                    if message.message_create['sender_id'] == self._master_id:
                        owner_messages.append(message)
                    # Debug only
                    if self._debug_mode:
                        print(message)
                    self.api.delete_direct_message(message.id)

                # Look for password from owner
                if owner_messages:
                    owner_message = owner_messages[0]
                    if self._master_password in owner_message.message_create['message_data']['text']:
                        if self._debug_mode:
                            print("Password entered is correct")
                        self.api.send_direct_message(message.message_create['sender_id'], "The password is correct!")
                        # Perform actions:


                    else:
                        if self._debug_mode:
                            print("Password entered is incorrect")
                        self.api.send_direct_message(owner_message.message_create['sender_id'],
                                                     "Incorrect Password! Try again!")

                # Check if message_list contains any new messages...
                else:
                    if self._debug_mode:
                        print('No messages from master found')

            else:
                if self._debug_mode:
                    print('No messages found')

        except tweepy.TweepyException as error:
            print(error.__cause__)


    def _retweet(self):
        total_retweeted = 2

        while True:
            for query in self.queries:
                for tweet in tweepy.Cursor(self.api.search_tweets, query).items(self.tweets_queried):
                    if total_retweeted > self.max_total_retweeted:
                        print('I\'ve made 5 retweets! Taking a short break!')
                        print(datetime.datetime.now())
                        time.sleep(self.break_time) # 15 minute break
                        total_retweeted = 0
                        print('back to work!')
                        break

                    try:
                        print(tweet.text)
                        if self.api.get_user(user_id=tweet.user.id).id == self.me.id:
                            print('It\'s me! Ignoring me!')
                            time.sleep(self.step_pause)
                        else:
                            if tweet.user.id in self._block_list:
                                print('BLOCKED USER! Ignored~!')
                                # self.api.send_direct_message(self._master_id, "I detected a BLOCKED user named " +
                                #                              str(tweet.user.name) + "\nId: " + str(tweet.user.id) +
                                #                              "\n\nhttps://twitter.com/" + str(tweet.user.screen_name) +
                                #                              "/status/" + str(tweet.id))
                                time.sleep(self.step_pause)

                            else:
                                if hasattr(tweet, "retweeted_status") and tweet.retweeted_status.user.id in self._block_list:
                                    print('BLOCKED RETWEETER! Ignored~!')
                                    # self.api.send_direct_message(self._master_id, "I detected a BLOCKED user named " +
                                    #                              str(tweet.user.name) + "\nId: " + str(tweet.user.id) +
                                    #                              "\n\nhttps://twitter.com/" + str(tweet.user.screen_name) +
                                    #                              "/status/" + str(tweet.id))
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

                    except tweepy.TweepyException as e:
                        print(e.__cause__)
                    except StopIteration:
                        break

            print('break time!')
            print(datetime.datetime.now())
            time.sleep(self.end_of_queries_pause)
            print('back to work!')
