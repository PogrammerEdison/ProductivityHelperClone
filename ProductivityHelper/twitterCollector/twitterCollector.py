import snscrape.modules.twitter as sntwitter
import random
from PyQt5.QtGui import QFont
class Twitter():
    def __init__(self, label):
        self.displayLabel = label
        font = QFont("HelveticaNeueLTPro-Roman.otf")
        font.setPointSize(10)
        self.displayLabel.setFont(font)
        self.tweets_list1 = []
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper('from:UpliftingQuotes').get_items()):
            if i > 100:
                break
            self.tweets_list1.append([tweet.date, tweet.id, tweet.content, tweet.user.username])
        result = random.choice(self.tweets_list1)
        self.displayLabel.setText(result[2])
        

