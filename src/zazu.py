#!/usr/bin/python
import logging
import configparser
import twitter
import random
import time
import os

SOURCEFILENAME = "tweets.txt"
LOGFILENAME = "zazu.log"
LOGLEVEL = logging.DEBUG
CONFIGFILE = "sampleconfig.txt"
RANDOMTIME = 5 * 60 # 5 minutes

# stub
# todo: account for links
def isValidTweet(text):
    text = text.strip()
    return len(text) <= 140 and len(text) > 0

def isEmpty(filename):
    filestat = os.stat(SOURCEFILENAME)
    return filestat.st_size == 0

def get_api():
    CONFIG = configparser.ConfigParser()
    CONFIG.read(CONFIGFILE)
    api = twitter.Api(
        consumer_key=CONFIG.get('api', 'consumer_key'),
        consumer_secret=CONFIG.get('api', 'consumer_secret'),
        access_token_key=CONFIG.get('api', 'access_token_key'),
        access_token_secret=CONFIG.get('api', 'access_token_secret')
    )
    return api

def main():
    # enable logging
    logging.basicConfig(format='%(asctime)s %(levelname)s: zazu %(message)s',filename=LOGFILENAME,level=LOGLEVEL)

    tweettext = ""
    while(not isValidTweet(tweettext) and not isEmpty(SOURCEFILENAME)):
        # open linefile, read first line
        sourcefile = open(SOURCEFILENAME,"r")
        tweettext = sourcefile.readline().strip()

        # read the tail of the source file, close the file
        sourcefile_tail = sourcefile.read()
        sourcefile.close()
        
        # process tweet
        if isValidTweet(tweettext):
            logging.info("Valid tweet text: \"%s\"", tweettext)
            print(tweettext)
            try:
                api = get_api()
                api.VerifyCredentials()
            except twitter.error.TwitterError as error:
                logging.error("TwitterError: %s",error)
                return # do not update the source file
            except Exception as error:
                logging.error("%s: %s",type(error),error)
                return # do not update the source file
            randomtime = random.randrange(0,RANDOMTIME)
            logging.info("sleeping for %d seconds (%.2f minutes) before posting tweet",randomtime,randomtime / 60)
            time.sleep(randomtime)
            try:
                post_update = api.PostUpdate(tweettext,trim_user=True,verify_status_length=True)
            except Exception as error:
                logging.error("%s: %s",type(error),error)
                return # do not update the source file
            logging.info("tweeted %s at %s",post_update.text,post_update.created_at)
            logging.debug("full post_update info: %s",str(post_update))
            
        else:
            logging.error("\"%s\" is not a valid tweet",tweettext)
            print("\"" + tweettext + "\"","is an unvalid tweet text")
        
        # update source file
        sourcefile = open(SOURCEFILENAME,"w")
        sourcefile.write(sourcefile_tail)
        sourcefile.close()
