#!/usr/bin/python
##############################################################
# Program name: NCAA Stats Scraper (Functions Module)
# Version: 1.0
##############################################################
import logging
import requests
try:
    # For Python 3.0 and later
    import http.cookiejar as cookielib
    from urllib.request import urlopen, URLError, HTTPCookieProcessor, build_opener, Request as POST
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2
    import cookielib
    from urllib2 import urlopen, URLError, HTTPCookieProcessor, build_opener
    from urllib import urlencode
from libDecorator import retry

LOG = logging.getLogger(__name__) 

def create_cookie():
    cookie_jar = cookielib.LWPCookieJar()
    ret = HTTPCookieProcessor(cookie_jar)
    return build_opener(ret)
@retry(URLError, tries=4, delay=3, backoff=2)
def grabber(url, params, http_header):
    print((url,http_header))
    print(http_header)
    #req = POST(url, urlencode(params).encode('utf-8'), http_header)
    req = POST(url, headers=http_header)
    res = urlopen(req)
    data = res.read()
    #res = create_cookie().open(req)
    #data = res.read()
    return data.decode("utf-8")
@retry(URLError, tries=4, delay=3, backoff=2)
def grabber(url, params, http_header):
    r = requests.get(url,http_header)
    return r.text
