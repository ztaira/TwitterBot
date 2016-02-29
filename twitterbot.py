from twitter import *
import login_credentials


class TwitterBot():
    """My twitterbot, aptly named."""
    def __init__(self):
        self.creds = login_credentials.get_login_credentials()
        self.twitter = Twitter(auth=OAuth(self.creds[0], self.creds[1],
                               self.creds[2], self.creds[3]))
        print("Logged in to twitter! :D")

    def tweet2file(self, twitterhandle='@zachary_taira', fname='output.txt'):
        file = open(fname, 'w+')
        userID = login_credentials.get_user(twitterhandle)
        tweets = self.twitter.statuses.user_timeline(user_id=userID)
        for tweet in tweets:
            file.write('\n(')
            file.write(tweet['text'])
            file.write(')\n')
