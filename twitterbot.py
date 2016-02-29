from twitter import *
import login_credentials


class TwitterBot():
    """My twitterbot, aptly named."""
    def __init__(self):
        self.creds = login_credentials.get_login_credentials()
        self.twitter = Twitter(auth=OAuth(self.creds[0], self.creds[1],
                               self.creds[2], self.creds[3]))
        print("Logged in to twitter! :D")

    def tweet2file(self, handle='@zachary_taira'):
        """Saves the text of a certain user's original tweets to file.
        File name is handle.txt"""
        file = open(handle+'.txt', 'w+')
        userID = login_credentials.get_user(handle)
        tweets = self.twitter.statuses.user_timeline(user_id=userID,
                                                     count=100,
                                                     trim_user=True,
                                                     exclude_replies=True,
                                                     include_rts=False)
        for tweet in tweets:
            file.write('\n(')
            file.write(tweet['text'])
            file.write(')\n')
        file.close()

    def searchtweets(self, handle='@zachary_taira', sstring='Hello, world!'):
        """Saves the text of a certain user's tweets to file and searches it.
        Only uses 1 API call, to avoid hitting the API rate limit."""
        self.tweet2file(handle)
        file = open(handle+'.txt', 'r')
        filetext = file.read()
        file.close()
        if sstring in filetext:
            return True
        else:
            return False
