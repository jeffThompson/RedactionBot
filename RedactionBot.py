
'''
REDACTION BOT
Jeff Thompson | 2013 | www.jeffreythompson.org

A Twitter bot that randomly loads and redacts Tweets
from the live Twitter stream.

LOAD OAUTH SETTINGS
Assumes Twitter OAuth settings, saved in a file
called OAuthSettings.py, saved in the following format:
	
	settings = {
		'consumer_key': 'xxxx',
		'consumer_secret': 'xxxx',
		'access_token_key': 'xxxx',
		'access_token_secret': 'xxxx'
	}

REQUIRES
+ OAuthlib
	- https://github.com/requests/requests-oauthlib
+ Python Twitter
	- https://github.com/bear/python-twitter
+ And, to access the live Twitter stream, another Twitter library
	- https://pypi.python.org/pypi/twitter

'''

from OAuthSettings import settings				# import from settings.py
import random															# for random words
import twitter														# for posting to Twitter
import TwitterStream											# another Twitter library, used here for Twitter stream access
import os																	# for getting current directory
from sys import exit											# for exiting when done posting
import re																	# regular expressions for redacting


# CLEAR SCREEN
os.system('cls' if os.name=='nt' else 'clear')


# BASIC VARIABLES
chance_redacted = 0.8											# chance that a word will be redacted
leave_spaces = False											# leave spaces between words or redact those too?
replace_string = re.compile(r'\S')				# ignore anything but a space (redacts punctuation too)
black = u'\u2588'.encode('utf-8')					# black-block Unicode character


# LOAD OAUTH DETAILS FROM FILE TO ACCESS TWITTER
# see notes at top for format
consumer_key = settings['consumer_key']
consumer_secret = settings['consumer_secret']
access_token_key = settings['access_token_key']
access_token_secret = settings['access_token_secret']


# LOAD INPUT TWEET FROM STREAM
auth = TwitterStream.OAuth( consumer_key = consumer_key, consumer_secret = consumer_secret, token = access_token_key, token_secret = access_token_secret )
ts = TwitterStream.TwitterStream(auth=auth, domain='stream.twitter.com')
iterator = ts.statuses.sample()
for t in iterator:												# go through Tweets (note: this is live!)
	if 'text' in t.keys():									# if this Tweet has text (ie: isn't a meta action)
		tweet = t['text'].encode('UTF-8')			# grab and encode to UTF-8 (for non-ASCII characters)
		break																	# quit iterator


# PRINT SOURCE TWEET
print '\n'
print 'SOURCE TWEET:'
print tweet


# REDACT RANDOMLY
tweet_words = tweet.split(' ')									# split input Tweet into words
tweet = []																			# create blank output Tweet
for word in tweet_words:												# go through word-by-word...
	if random.random() < chance_redacted:					# if random value is below redaction threshold
		word = re.sub(replace_string, black, word)	# replace with black block
	tweet.append(word)


# CLEAN UP MISC
tweet = ' '.join(tweet)
if leave_spaces == False:																	# remove spaces if specified
	tweet = re.sub(black + '(\s)' + black, black, tweet)
if black not in tweet:																		# if nothing redacted, redact it all!
	print 'nothing'
	tweet = (black * len(tweet))


# PRINT THE RESULTING TWEET
print '\n'
print 'REDACTED TWEET:'
print tweet


# CONNECT TO TWITTER API, POST and PRINT RESULT
# catch any errors and let us know
try:
	api = twitter.Api(consumer_key = consumer_key, consumer_secret = consumer_secret, access_token_key = access_token_key, access_token_secret = access_token_secret)
	print '\n\n' + 'posting to Twitter...'
	status = api.PostUpdate(tweet)
	print '  post successful!\n\n'
except twitter.TwitterError:
	#print api.message
	print 'error posting!'


# SAVE TWEETS TO FILE
# get current directory, prepend to word list paths
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
with open(os.path.join(__location__, 'Tweets.txt'), 'a') as file:
	file.write(tweet + '\n\n')


# ALL DONE!
print '\n\n'
exit()
