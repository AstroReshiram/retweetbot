# Main file that runs the entire bot program
from Configuration import Configuration
from RetweetBot import RetweetBot


def main():
    config = Configuration('config.json')
    rtbot = RetweetBot(config)
    rtbot.run()

if __name__ == "__main__":
    main()