# zazu
Twitter bot in Python3 for populating my own timeline with texts from a text file.

## Etymology

`zazu` was named after Zazu, the hornbill from Disney's The Lion King.

## Requirements

 * python3
 * python-twitter (`pip install python-twitter`). 
 * API keys from [Twitter](https://apps.twitter.com/)
 
Zazu supports Twitters new 280-character limit. Note that [python-twitter 3.3](https://pypi.python.org/pypi/python-twitter/3.3) (from pypi.python.org) does not yet support this. If you want to post tweets of more than 140 characters, you need to [upgrade python-twitter to version 3.3.1](https://github.com/bear/python-twitter) or [patch your python-twitter package by hand](https://github.com/bear/python-twitter/commit/d4f3dcd08c555e8ae67b87034ac4820aa188d33b).
 
## Setup

 * Clone this repo
 * Create a plain text source file to store your tweets.
 * Copy sampleconfig.txt to config.txt and enter your preferred settings. At the very least, submit valid Twitter API keys and point to your source file.
 * Fill your source file with a few tweets.
 * [Optional] Run `python3 zazu.py` to post your first tweet as a test run.
 * Make a cron-job for zazu.
