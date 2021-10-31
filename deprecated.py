# Select year for parsing
academic_year = "2014" # Set the academic year (2012 refers to 2011-2012 season). As of writing, this can range from 2010 to 2013.
year_index = "11540" # Set the index that maps to the academic year. 
# This may be obtained from looking at the team URLs on the list of available teams, for the given academic year. 
# As of writing, the [academic_year, year_index] mappings are: [2013, 11220], [2012, 10740], [2011, 10440], and [2010, 10260]

# What do you want to do? (Note: Lower tiers need higher tiers, i.e., ind_game_stats requires map_players (Tier 2), which requires map_teams (Tier 1).)
map_teams = 1 # Create a team mapping (0 = no, 1 = yes) -- TIER 1
map_schedule = 1 # Create schedule mapping (0 = no, 1 = yes)
map_players = 1 # Create a player mapping (0 = no, 1 = yes)
summary_teams = 1 # Get summary statistics for each team (0 = no, 1 = yes)
summary_players = 1 # Get summary statistics for each player (0 = no, 1 = yes)
ind_game_stats = 1 # Get individual game statistics (0 = no, 1 = yes)
ind_player_stats = 1 # Get individual player statistics (0 = no, 1 = yes)
ind_team_stats = 1 # Get individual team statistics (a line per team, such that each game will have two lines (one for away team, one for home team)) (0 = no, 1 = yes)

# Where do you want to save the data?
team_mappingfile = "mappings/team_mappings.tsv" # Data file for team mappings
player_mappingfile = "mappings/player_mappings.tsv" # Data file for player mappings
schedule_mappingfile = "mappings/schedule_mappings.tsv" # Data file for schedule mappings
summary_player_data = "data/summary_player_data.tsv" # Data file for individual player summary statistics
summary_team_data = "data/summary_team_data.tsv" # Data file for team summary statistics
game_data = "data/game_data.tsv" # Data file for each game
player_data = "data/player_data.tsv" # Data file for each player
team_data = "data/team_data.tsv" # Data file for each team

#### The variables below could be set, but probably don't need any modification #####
debugmode = 1 # Output program steps (0 = off, 1 = on)
params = { } # Any POST parameters that need to be sent (default)
http_header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0",
            "Accept": "text/plain, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.5",
            "DNT": "1",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "http://stats.ncaa.org/team/inst_team_list?sport_code=MBB&division=1",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache"
            } # Variables from the HTTP header (default)
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
