#!/usr/bin/env python3

import logging
import configparser
import os
import zazu_twitter as sm

CONFIGFILE = "config.txt"

def isEmpty(filename):
    """Return True if `filename` is empty, otherwise False

    >>> zazu.isEmpty("../tests/emptyfile.txt")
    True
    >>> zazu.isEmpty("../tests/badtweets.txt")
    False
    """
    statinfo = os.stat(filename)
    return statinfo.st_size == 0

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

def main():
    config = process_config(CONFIGFILE)
    enable_logging(config)
    
    sourcefilename = config.get('general','source_file_name')

    posttext = ""
    while(not sm.isValidPost(posttext) and not isEmpty(sourcefilename)):
        # open linefile, read first line
        sourcefile = open(sourcefilename,"r")
        posttext = sourcefile.readline().strip()

        # read the tail of the source file, close the file
        sourcefile_tail = sourcefile.read()
        sourcefile.close()

        # process post
        if sm.isValidPost(posttext):
            logging.info("Valid post text: \"%s\"", posttext)
            post_update = sm.post(config,posttext)
        else:
            logging.error("\"%s\" is not a valid post",posttext)

        # update source file
        sourcefile = open(sourcefilename,"w")
        sourcefile.write(sourcefile_tail)
        sourcefile.close()

if __name__ == "__main__":
    main()
