from twitter import *
import login_credentials

creds = login_credentials.get_login_credentials()
twitter = Twitter(auth=OAuth(creds[0], creds[1], creds[2], creds[3]))
twitter.statuses.update(status="^-^")
