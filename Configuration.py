# This file loads the configuration from the files.
import json

class Configuration:

    def __init__(self, filename):
        self._file = open(filename)
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

        # Master Control
        self._master = self._config['MasterControl']
        self.master_screen_name = self._master['ScreenName']
        self.master_user_id = self._master['UserID']
        self.master_password = self._master['Password']

        # Debug Mode
        self.debug_mode = self._str2bool(self._settings['DebugMode'])

    def _str2bool(self, v):
        return v.lower() in ("yes", "true", "t", "1")