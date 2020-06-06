# This file loads the configuration from the files.
import json

class Configuration:

    def __init__(self):
        self._file = open('config.json')
        self._config = json.load(self._file)
        self._keys = self._config['TwitterKeys']
        self._settings = self._config['BotSettings']

        # Load authorization tokens
        self.key = self._keys['ConsumerKey']
        self.secret_key = self._keys['ConsumerSecretKey']
        self.token = self._keys['AccessToken']
        self.secret_token = self._keys['AccessSecretToken']

        # Load bot settings
        self.queries = self._settings['Queries']
        self.tweets_queried = self._settings['TotalTweetsQueried']
        self.retweets_per_break = self._settings['TotalRetweetsPerBreak']
        self.step_pause = self._settings['StepPauseSeconds']
        self.retweet_period = self._settings['RetweetPeriodSeconds']
        self.break_time = self._settings['BreakTimeSeconds']
        self.end_of_queries_pause = self._settings['EndOfQueriesPauseSeconds']

