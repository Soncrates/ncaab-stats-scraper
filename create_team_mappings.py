#!/usr/bin/python
##############################################################
# Program name: NCAA Stats Scraper (Team Mappings Module)
# Version: 1.0
##############################################################

# Import modules and libraries
from scraperfunctions import grabber as EXTRACT
from scrapersettings import Lacrosse, Football, Basketball, Soccer, SportExtract as BASE
from bs4 import BeautifulSoup as TRANSFORM

def step01_request_team_list(sport,**kvargs) :
    return [ EXTRACT(url, BASE.params, BASE.headers) for url in sport.extract_team_list(**kvargs) ]  
def step02_parse_response(response) :
    link_list = TRANSFORM(response,features="html.parser").findAll('a')
    link_list = [ link for link in link_list if step02_test(link)]
    print(link_list)
    return { key : value for key, value in step02_transform(link) for link in link_list if step02_test(link) }
def step02_test(link) :
    return link.get('href').startswith('/team/')
def step02_transform(link) :
    return str(link.get_text()),  str(BASE.base_url  + link.get('href'))
def team_list_by_sport(*url_by_division_list) :
    team_list_by_division_response_list = [ POST(url, BASE.params, BASE.headers) for url in url_by_division_list]  
    ret = [ step02_parse_response(team_list) for team_list in team_list_by_division_response_list ]
    return { k: v for k, v in team_list.items() for team_list in ret }
def write_csv(filename,team_list) :
    with open(filename,'w') as f:
         f.writelines("team_name\tteam_url\n")
         for name, url in team_list.items() :
             f.writelines("{}\t{}\n".format(name,url))
def main() :
    sport_list = [Lacrosse(),Football(),Basketball(),Soccer()]
    team_list = [ step01_request_team_list(sport) for sport in sport_list ]

    sport_list = { "team_list_{sport_code}.csv".format(**sport.default_params) : step01_request_team_list(sport) for sport in sport_list }
    for filename, team_list in sport_list.items() :
        write_csv(filename, team_list)

if __name__ == "__main__" :
   main()
