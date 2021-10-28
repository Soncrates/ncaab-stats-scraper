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

try:
    # For Python 3.0 and later
    from urllib3.request import urlopen, URLError, HTTPCookieProcessor, build_opener
    from urllib3.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen, URLError, HTTPCookieProcessor, build_opener
    from urllib import urlencode
from libDecorator import retry

def create_cookie():
    # Create a cookie handler, if necessary
    cookie_jar = cookielib.LWPCookieJar()
    cookie = HTTPCookieProcessor(cookie_jar)
    
    opencookies = build_opener(cookie)
    return(opencookies)

@retry(URLError, tries=4, delay=3, backoff=2)
def grabber(url, params, http_header):
    cookiejar = create_cookie()
    req = urlopen(url, urlencode(params).encode('utf-8'), http_header)
    
    res = cookiejar.open(req)
    data = res.read()
    return(data)
