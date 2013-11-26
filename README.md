█████████ ███
============

'Redaction Bot' is a Twitter bot that randomly loads and redacts Tweets from the live Twitter stream.

**LOAD OAUTH SETTINGS**  
Assumes Twitter OAuth settings, saved in a file called OAuthSettings.py, saved in the following format:
	
    settings = {
      'consumer_key': 'xxxx',
      'consumer_secret': 'xxxx',
      'access_token_key': 'xxxx',
      'access_token_secret': 'xxxx'
    }

**REQUIRES**
+ OAuthlib  
https://github.com/requests/requests-oauthlib
+ Python Twitter  
https://github.com/bear/python-twitter
+ And, to access the live Twitter stream, another Twitter library  
https://pypi.python.org/pypi/twitter
