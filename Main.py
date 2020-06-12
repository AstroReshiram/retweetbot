# Main file that runs the entire bot program
from Configuration import Configuration
from RetweetBot import RetweetBot

config = Configuration('config.json')
rtbot = RetweetBot(config)
rtbot.run()