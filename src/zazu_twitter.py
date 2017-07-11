#!/usr/bin/python

import time
import re
import sys
import configparser
import random
import logging
import twitter



def isValidPost(text):
    """
    >>> isValidTweet("Hoi dit is een test")
    True
    >>> isValidTweet("LONG "* 100 + "TWEET")
    False
    >>> isValidTweet("https://en.wikipedia.org/wiki/Python_(programming_language " * 7)
    False
    >>> isValidTweet("https://en.wikipedia.org/wiki/Python_(programming_language " * 5)
    True
    """

    text = text.strip()
    relative_length = len(text)
    for match in re.findall("https?://[\S]*",text):
        relative_length = relative_length + 23 - len(match)
    return relative_length <= 140 and relative_length > 0

def getApi(config):
    api = twitter.Api(
        consumer_key=config.get('api', 'consumer_key'),
        consumer_secret=config.get('api', 'consumer_secret'),
        access_token_key=config.get('api', 'access_token_key'),
        access_token_secret=config.get('api', 'access_token_secret')
    )
    user = api.VerifyCredentials()
    logging.info("running with valid api credentials for user %s (%s)", user.name, user.screen_name)
    return api

def post(config,posttext):
    try:
        api = getApi(config)
    except twitter.error.TwitterError as error:
        logging.error("TwitterError: %s",error)
        sys.exit(1) # do not update the source file
    except Exception as error:
        logging.error("%s: %s",type(error),error)
        sys.exit(1) # do not update the source file
    randomtime = 60 * random.randrange(0,int(config.get('general','random_time')))
    logging.info("sleeping for %d seconds (%.2f minutes) before posting",randomtime,randomtime / 60)
    time.sleep(randomtime)
    try:
        post_update = api.PostUpdate(posttext,trim_user=True,verify_status_length=True)
    except Exception as error:
        logging.error("%s: %s",type(error),error)
        sys.exit(1) # do not update the source file
    logging.info("posted %s at %s",post_update.text,post_update.created_at)
    logging.debug("full post_update info: %s",str(post_update))
    return post_update
