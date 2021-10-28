#!/usr/bin/python
##############################################################
# Program name: NCAA Stats Scraper (Functions Module)
# Version: 1.0
##############################################################
try:
    # For Python 3.0 and later
    import http.cookiejar as cookielib
    from urllib.request import urlopen, URLError, HTTPCookieProcessor, build_opener
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2
    import cookielib
    from urllib2 import urlopen, URLError, HTTPCookieProcessor, build_opener
    from urllib import urlencode
from libDecorator import retry

def create_cookie():
    cookie_jar = cookielib.LWPCookieJar()
    ret = HTTPCookieProcessor(cookie_jar)
    return build_opener(ret)
@retry(URLError, tries=4, delay=3, backoff=2)
def grabber(url, params, http_header):
    req = urlopen(url, urlencode(params).encode('utf-8'), http_header)
    res = create_cookie().open(req)
    data = res.read()
    return(data)
