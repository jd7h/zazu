#!/usr/bin/env python3

import logging
import configparser
import twitter
import random
import time
import os
import re
import sys

CONFIGFILE = "config.txt"

def isValidTweet(text):
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


def isEmpty(filename):
    """Return True if `filename` is empty, otherwise False

    >>> zazu.isEmpty("../tests/emptyfile.txt")
    True
    >>> zazu.isEmpty("../tests/badtweets.txt")
    False
    """
    statinfo = os.stat(filename)
    return statinfo.st_size == 0

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

def process_config(config_location):
    # check for configfile
    if isEmpty(config_location):
        raise ValueError("The configuration file " + config_location + " is empty")

    # read configfile
    config = configparser.ConfigParser()
    config.read(config_location)
    return config

def enable_logging(config):
    logfilename = config.get('general','log_file_name')
    logging.basicConfig(format='%(asctime)s %(levelname)s: zazu %(message)s',filename=logfilename,level=config.get('general','log_level'))
    
def post_tweet(config,tweettext):
    try:
        api = getApi(config)
        api.VerifyCredentials()
    except twitter.error.TwitterError as error:
        logging.error("TwitterError: %s",error)
        sys.exit(1) # do not update the source file
    except Exception as error:
        logging.error("%s: %s",type(error),error)
        sys.exit(1) # do not update the source file
    randomtime = 60 * random.randrange(0,int(config.get('general','random_time')))
    logging.info("sleeping for %d seconds (%.2f minutes) before posting tweet",randomtime,randomtime / 60)
    time.sleep(randomtime)
    try:
        post_update = api.PostUpdate(tweettext,trim_user=True,verify_status_length=True)
    except Exception as error:
        logging.error("%s: %s",type(error),error)
        sys.exit(1) # do not update the source file
    logging.info("tweeted %s at %s",post_update.text,post_update.created_at)
    logging.debug("full post_update info: %s",str(post_update))
    return post_update

def main():
    config = process_config(CONFIGFILE)
    enable_logging(config)
    
    sourcefilename = config.get('general','source_file_name')

    tweettext = ""
    while(not isValidTweet(tweettext) and not isEmpty(sourcefilename)):
        # open linefile, read first line
        sourcefile = open(sourcefilename,"r")
        tweettext = sourcefile.readline().strip()

        # read the tail of the source file, close the file
        sourcefile_tail = sourcefile.read()
        sourcefile.close()

        # process tweet
        if isValidTweet(tweettext):
            logging.info("Valid tweet text: \"%s\"", tweettext)
            post_update = post_tweet(config,tweettext)
        else:
            logging.error("\"%s\" is not a valid tweet",tweettext)

        # update source file
        sourcefile = open(sourcefilename,"w")
        sourcefile.write(sourcefile_tail)
        sourcefile.close()

if __name__ == "__main__":
    main()
