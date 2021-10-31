#!/usr/bin/python
##############################################################
# Program name: NCAA Stats Scraper (Functions Module)
# Version: 1.0
##############################################################
import logging
import requests
from libDecorator import retry

LOG = logging.getLogger(__name__) 

try:
    # For Python 3.0 and later
    from urllib.request import URLError
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import URLError

@retry(URLError, tries=4, delay=3, backoff=2)
def grabber(url, params, http_header):
    r = requests.get(url,http_header)
    return r.text
