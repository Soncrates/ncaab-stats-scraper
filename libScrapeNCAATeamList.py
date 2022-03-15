#!/usr/bin/python
##############################################################
# Program name: NCAA Stats Scraper (Team Mappings Module)
# Version: 1.0
##############################################################

from libScrapeNCAASettings import SportExtract as BASE
from libScrapeNCAAFunctions import grabber as EXTRACT
from bs4 import BeautifulSoup as TRANSFORM
import logging as log

class TRANSFORM_TEAM :
    @staticmethod
    def main(response) :
        link_list = TRANSFORM(response,features="html.parser").findAll('a')
        link_list = [ TRANSFORM_TEAM.transform(link) for link in link_list if TRANSFORM_TEAM.is_team(link) ]
        return { key : value for key,value in link_list }
    @staticmethod
    def is_team(link) :
        ctx = link.get('href')
        return ctx.startswith('/team/') and 'division' not in ctx
    @staticmethod
    def transform(link) :
        return str(link.get_text()),  str(BASE.base_url  + link.get('href'))
def merge_divisions(*division_list) :
    return {k:v for division in division_list for (k,v) in division.items()}
def write_csv(filename,team_list) :
    log.debug(filename)
    with open(filename,'w') as f:
         f.writelines("team_name\tteam_url\n")
         for name, url in team_list.items() :
             f.writelines("{}\t{}\n".format(name,url))
def main(sport,filename) :
    division_list = [ EXTRACT(url, BASE.params, BASE.headers) for url in sport.url_team_list() ] 
    log.debug(division_list[:5])
    division_list = [ TRANSFORM_TEAM.main(division) for division in division_list ]
    log.debug(division_list[:5])
    team_list = merge_divisions(*division_list)
    log.debug(team_list)
    write_csv(filename, team_list)

if __name__ == "__main__" :
   from scrapersettings import Lacrosse, Football, Basketball, Soccer
   for sport in [Lacrosse(),Football(),Basketball(),Soccer()] :
       main(sport)
