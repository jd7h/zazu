#!/usr/bin/python
import logging
import configparser
import twitter
import random
import time
import os
import re

CONFIGFILE = "sampleconfig.txt"

def isValidTweet(text):
    text = text.strip()
    relative_length = len(text)
    for match in re.findall("https?://[\S]*",text):
        relative_length = relative_length + 23 - len(match)
    return relative_length <= 140 and relative_length > 0

def isEmpty(filename):
    filestat = os.stat(filename)
    return filestat.st_size == 0

def getApi(config)
    api = twitter.Api(
        consumer_key=config.get('api', 'consumer_key'),
        consumer_secret=config.get('api', 'consumer_secret'),
        access_token_key=config.get('api', 'access_token_key'),
        access_token_secret=config.get('api', 'access_token_secret')
    )
    return api

def main():
    # read configfile
    config = configparser.ConfigParser()
    config.read(CONFIGFILE)

    sourcefilename = config.get('general','source_file_name')
    logfilename = config.get('general','log_file_name')

    # enable logging
    logging.basicConfig(format='%(asctime)s %(levelname)s: zazu %(message)s',filename=logfilename,level=config.get('general','log_level')

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
            print(tweettext)
            try:
                api = getApi(config)
                api.VerifyCredentials()
            except twitter.error.TwitterError as error:
                logging.error("TwitterError: %s",error)
                return # do not update the source file
            except Exception as error:
                logging.error("%s: %s",type(error),error)
                return # do not update the source file
            randomtime = random.randrange(0,config.get('general','random_time'))
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
        sourcefile = open(sourcefilename,"w")
        sourcefile.write(sourcefile_tail)
        sourcefile.close()
