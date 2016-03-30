from twitter import *
import login_credentials
import time


class TwitterBot():
    """My twitterbot, aptly named."""
    def __init__(self):
        self.creds = login_credentials.get_login_credentials()
        self.twitter = Twitter(auth=OAuth(self.creds[0], self.creds[1],
                               self.creds[2], self.creds[3]))
        print("Logged in to twitter! :D")
        print("Executing programmed behavior...")
        self.handle='@zachary_taira'
        self.behavior()

    # Tweets
    # ================================================================
    def tweet2file(self, handle='@zachary_taira'):
        """Saves the text of a certain user's original tweets to file.
        File name is handle.txt
        Uses 1 API call to get the tweets, and then one for each new user."""
        file = open(handle+'.txt', 'w+')
        userID = login_credentials.get_user(handle)
        tweets = self.twitter.statuses.user_timeline(user_id=userID,
                                                     count=100,
                                                     trim_user=True,
                                                     exclude_replies=True,
                                                     include_rts=False)
        users = {}
        for tweet in tweets:
            if tweet['user']['id_str'] not in users:
                user = self.twitter.users.show(user_id=tweet['user']['id_str'])
                users[tweet['user']['id_str']] = user['screen_name']
            file.write('\n(')
            file.write(repr(tweet['text']))
            file.write(') by @' + users[tweet['user']['id_str']])
            file.write('\n')
        file.close()

    def searchtweets(self, handle='@zachary_taira', sstring='Hello, world!',
                     update=False):
        """Searches a string against a given user's tweet log.
        If update is true, updates tweet logs before checking.
        Only uses 1 API call via self.tweet2file"""
        if update is True:
            self.tweet2file(handle)
        file = open(handle+'.txt', 'r')
        filetext = file.read()
        file.close()
        if sstring in filetext:
            return True
        else:
            return False

    def hasnewtweet(self, handle='@zachary_taira'):
        """Returns True if the user has a new tweet since the last check.
        Does this by getting the most recent tweet and checking it.
        If it's in the log, it's old. If it's not, it's new.
        Uses 1 API call."""
        userID = login_credentials.get_user(handle)
        tweet = self.twitter.statuses.user_timeline(user_id=userID,
                                                    count=1,
                                                    trim_user=True,
                                                    exclude_replies=True,
                                                    include_rts=False)
        file = open(handle+'.txt', 'r')
        filetext = file.read()
        file.close()
        if repr(tweet[0]['text']) in filetext:
            return False
        else:
            self.tweet2file()
            return True

    def getnewtweetid(self, handle='@zachary_taira'):
        """Get the IDs of a user's newest tweets. Uses 1 API call."""
        userID = login_credentials.get_user(handle)
        tweets = self.twitter.statuses.user_timeline(user_id=userID,
                                                    count=100,
                                                    trim_user=True,
                                                    exclude_replies=True,
                                                    include_rts=False)
        id_list = []
        file = open(handle+'.txt')
        filetext = file.read()
        file.close()
        for tweet in tweets:
            if repr(tweet['text']) not in filetext:
                id_list.append(tweet['id_str'])
        return id_list

    def getnewtweettext(self, handle='@zachary_taira'):
        """Get the text of a user's newest tweets. Uses 1 API call."""
        userID = login_credentials.get_user(handle)
        tweets = self.twitter.statuses.user_timeline(user_id=userID,
                                                    count=1,
                                                    trim_user=True,
                                                    exclude_replies=True,
                                                    include_rts=False)
        text_list = []
        file = open(handle+'.txt')
        filetext = file.read()
        file.close()
        for tweet in tweets:
            if repr(tweet['text']) not in filetext:
                text_list.append(repr(tweet['text']))
        return text_list

    def getnewtweets(self, handle='@zachary_taira'):
        """Get a user's newest tweet. Uses 1 API call."""
        userID = login_credentials.get_user(handle)
        tweets = self.twitter.statuses.user_timeline(user_id=userID,
                                                    count=1,
                                                    trim_user=True,
                                                    exclude_replies=True,
                                                    include_rts=False)
        tweet_list = []
        file = open(handle+'.txt')
        filetext = file.read()
        file.close()
        for tweet in tweets:
            if repr(tweet['text']) not in filetext:
                tweet_list.append(tweet)
        return tweet_list


    # Statuses
    # ================================================================
    def poststatus(self, new_status="Hello World!"):
        """Posts a new status to twitter. Uses 1 API Call."""
        self.twitter.statuses.update(status=new_status)

    def postfromfile(self, fname="queue.txt"):
        """Takes the first line of a file, posts it to twitter, then removes it.
        Uses 1 API Call."""
        # creates a line store
        line_list = []
        # reads and posts the first line
        file = open(fname, 'r')
        firstline = file.readline()
        self.twitter.statuses.update(status=firstline)
        # removes it and writes the rest of the lines over the original file
        for line in file:
            line_list.append(line)
        file.close()
        file = open(fname, 'w+')
        for line in line_list:
            file.write(line)
        file.close()

    # Mentions
    # TODO:
    # Make the getnewmention__ functions take more than 1 thing
    # ================================================================
    def mention2file(self):
        """writes all mentions to file. Uses 1 API call."""
        mentions = self.twitter.statuses.mentions_timeline()
        file = open(self.handle+'m.txt', 'w+')
        for mention in mentions:
            file.write('\n(')
            file.write(mention['text'])
            file.write(') ' + str(mention['user']['name']) + '\n')
        file.close()

    def getnewmention(self):
        """Gets the latest mention. Uses 1 API call."""
        mentions = self.twitter.statuses.mentions_timeline(count=1)
        return mentions[0]

    def getnewmentionuser(self):
        """Gets the user who did the latest mention."""
        mentions = self.twitter.statuses.mentions_timeline(count=1)
        return mentions[0]['user']['name']

    def getnewmentionhandle(self):
        """Gets the handle of the user who did the latest mention."""
        mentions = self.twitter.statuses.mentions_timeline(count=1)
        return '@'+str(mentions[0]['user']['screen_name'])

    def searchmentions(self, handle='@zachary_taira', sstring='Hello, world!',
                     update=False):
        """Searches a string against a given user's tweet log.
        If update is true, updates tweet logs before checking.
        Only uses 1 API call via self.mention2file"""
        if update is True:
            self.mention2file(handle)
        file = open(handle+'m.txt', 'r')
        filetext = file.read()
        file.close()
        if sstring in filetext:
            return True
        else:
            return False

    def hasnewmention(self):
        """Returns true if there's a new mention. Uses 1 API call."""
        mention = self.getnewmention()
        file = open(self.handle+'m.txt', 'r')
        filetext = file.read()
        file.close()
        if mention['text'] in filetext:
            return False
        else:
            self.mention2file()
            return True

    def getnewmentiontext(self):
        """Gets the text of the latest mention."""
        mentions = self.twitter.statuses.mentions_timeline(count=1)
        return str(mentions[0]['text'])

    def behavior(self):
        """This is what the twitterbot does when running"""
        # do stuff
        return 0

if __name__ == '__main__':
    z = TwitterBot()
