#!/usr/bin/python
##############################################################
# Program name: NCAA Stats Scraper (Functions Module)
# Version: 1.0
##############################################################

try:
    import cookielib
except:
    import http.cookiejar
    cookielib = http.cookiejar

import urllib
try:
    # For Python 3.0 and later
    from urllib.request import urlopen, URLError, HTTPCookieProcessor, build_opener
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen, URLError, HTTPCookieProcessor, build_opener
    from urllib import urlencode
import re
import scrapersettings

### Retry Decorator code taken from the SaltyCrane Blog (http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/)
import time
from functools import wraps

def retry(ExceptionToCheck, tries=4, delay=3, backoff=2, logger=None):
    """Retry calling the decorated function using an exponential backoff.

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    :param ExceptionToCheck: the exception to check. may be a tuple of
        exceptions to check
    :type ExceptionToCheck: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    :param logger: logger to use. If None, print
    :type logger: logging.Logger instance
    """
    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck as e:
                    msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
                    if logger:
                        logger.warning(msg)
                    else:
                        print (msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry

### Define our functions
def create_cookie():
    # Create a cookie handler, if necessary
    cookie_jar = cookielib.LWPCookieJar()
    cookie = HTTPCookieProcessor(cookie_jar)
    
    opencookies = build_opener(cookie)
    return(opencookies)

@retry(URLError, tries=4, delay=3, backoff=2)
def grabber(url, params, http_header):
    cookiejar = create_cookie()
    req = urlopen(url, urlencode(params).encode('encoding'), http_header)
    
    res = cookiejar.open(req)
    data = res.read()
    return(data)

def get_team_mappings():
    team_map = open(scrapersettings.team_mappingfile, "rb")
    team_map = team_map.readlines()[1:]
    team_map = dict([(var.split("\t")[0], (var.split("\t")[1], var.split("\t")[2].strip("\n"))) for var in team_map])
    return(team_map)

def get_game_mappings():
    game_map = open(scrapersettings.schedule_mappingfile, "rb")
    game_map = game_map.readlines()[1:]
    game_map = dict([(var.split("\t")[0], (var.split("\t")[1], var.split("\t")[2], var.split("\t")[3], var.split("\t")[4], var.split("\t")[5].strip("\n"))) for var in game_map])
    return(game_map)
