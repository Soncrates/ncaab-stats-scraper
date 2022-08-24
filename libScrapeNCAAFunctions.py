#!/usr/bin/python
##############################################################
# Program name: NCAA Stats Scraper (Functions Module)
# Version: 1.0
##############################################################
import logging as log
import requests

from libDecorator import retry

LOG = log.getLogger(__name__) 

try:
    # For Python 3.0 and later
    from urllib.request import URLError
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import URLError

def try_01(url,headers) :
    base_url = '/'.join(url.split('/')[:3])
    log.debug(base_url)
    session = requests.Session()
    test = session.head(base_url)
    test.raise_for_status()
    log.debug(test.status_code)
    log.debug(session.cookies.get_dict())
    ret = session.get(url)
    ret.raise_for_status()
    log.debug(ret.status_code)
    return ret

def try_02(url,headers) :
    ret = requests.get(url, headers=headers)
    ret.raise_for_status()
    log.debug(ret.status_code)
    return ret
def validate(url,headers) :
    ret = requests.get(url, headers=headers)
    return ret.ok

@retry(URLError, tries=4, delay=3, backoff=2)
def grabber(url, params, http_header):
    log.debug(url)
    log.debug(http_header)
    ret = try_02(url,http_header)
    log.debug(ret.text[700:1000])
    return ret.text

@retry(URLError, tries=4, delay=8, backoff=2)
def grab_scores(url, params, http_header):
    log.debug(url)
    log.debug(http_header)
    ret = try_02(url,http_header)
    log.debug(ret.text[700:1000])
    return ret.text
