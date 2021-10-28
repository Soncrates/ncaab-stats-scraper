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
    from urllib.request import urlopen, URLError, HTTPCookieProcessor, build_opener
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen, URLError, HTTPCookieProcessor, build_opener
    from urllib import urlencode
import re
import scrapersettings
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

def get_team_mappings():
    team_map = open(scrapersettings.team_mappingfile, "rb")
    team_map = team_map.readlines()[1:]
    team_map = dict([(var.split("\t")[0], (var.split("\t")[1], var.split("\t")[2].strip("\n"))) for var in team_map])
    return(team_map)

def get_game_mappings() :
    game_map = open(scrapersettings.schedule_mappingfile, "rb")
    game_map = game_map.readlines()[1:]
    game_map = dict([(var.split("\t")[0], (var.split("\t")[1], var.split("\t")[2], var.split("\t")[3], var.split("\t")[4], var.split("\t")[5].strip("\n"))) for var in game_map])
    return(game_map)
