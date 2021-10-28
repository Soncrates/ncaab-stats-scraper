#!/usr/bin/python
##############################################################
# Program name: NCAA Stats Scraper (Team Mappings Module)
# Version: 1.0
##############################################################

# Import modules and libraries
from scraperfunctions import grabber as EXTRACT
from scrapersettings import SportExtract as BASE
from bs4 import BeautifulSoup as TRANSFORM

def step01_request_team_list(sport,**kvargs) :
    return [ EXTRACT(url, BASE.params, BASE.headers) for url in sport.extract_team_list(**kvargs) ]  
def step02_parse_response(response) :
    link_list = TRANSFORM(response,features="html.parser").findAll('a')
    return  {k:v for link in link_list for (k,v) in step02_transform(link) if step02_test(link) }
    link_list = [ step02_transform(link) for link in link_list if step02_test(link) ]
    return { key : value for key,value in link_list }
def step02_test(link) :
    ctx = link.get('href')
    return ctx.startswith('/team/') and 'division' not in ctx
def step02_transform(link) :
    return str(link.get_text()),  str(BASE.base_url  + link.get('href'))
def merge_divisions(*division_list) :
    ret = [ division.items() for division in division_list ]
    print(ret)
    return { k: v for k, v in ret }
    return {k:v for division in division_list for (k,v) in division.items()}
def write_csv(filename,team_list) :
    with open(filename,'w') as f:
         f.writelines("team_name\tteam_url\n")
         for name, url in team_list.items() :
             f.writelines("{}\t{}\n".format(name,url))
def main(*sport_list) :
    name_list =  [ "team_list_{sport_code}.csv".format(**sport.default_params) for sport in sport_list ]
    division_list = [ step01_request_team_list(sport) for sport in sport_list ]
    for i, name in enumerate(name_list) :
        division_list = [ step02_parse_response(division) for division in division_list[i] ]
        team_list = merge_divisions(*division_list)
        write_csv(name_list[i], team_list)        

if __name__ == "__main__" :
   from scrapersettings import Lacrosse, Football, Basketball, Soccer
   sport_list = [Lacrosse(),Football(),Basketball(),Soccer()]
   main(*sport_list)
