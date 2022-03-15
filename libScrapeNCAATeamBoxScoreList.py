#!/usr/bin/python
##############################################################
# Program name: NCAA Stats Scraper (Team Mappings Module)
# Version: 1.0
##############################################################
from bs4 import BeautifulSoup as TRANSFORM
from datetime import datetime
import logging as log
import pandas as PD
import re

import libCommon as COMMON
from libScrapeNCAASettings import SportExtract as BASE
from libScrapeNCAAFunctions import grab_scores as EXTRACT_SCORES, grabber as EXTRACT_TEAMS

BOX_SCORE_RE = re.compile(r'(\d+/\d+/\d+)')
BOX_SCORE_DATE_FORMAT = '%m/%d/%Y'
BOX_SCORE_LINGO = ['1st Quarter', '2nd Quarter', '3rd Quarter', '4th Quarter', '1st Half','2nd Half']

class READ_FILE_INPUT :
    @staticmethod
    def get_team_list(filename):
        log.info("Reading team file {}".format(filename))
        with open(filename, "r") as f :
             team_list = f.readlines()[1:]
             team_list = [ team.split("\t") for team in team_list ]
             log.info(team_list[:5])
             ret = { var[0] : var[1] for var in team_list }
             return ret
class TRANSFORM_BS4 :
    @staticmethod
    def extract_table_rows(tr_list) :    
        ret = []
        for td_list in tr_list :
            ret.append([ col.text.strip() for col in td_list ])
        return ret
    @staticmethod
    def flatten_table_rows(tr_list) :    
        ret = []
        for td_list in tr_list :
            ret.extend(td_list)
        return ret

class TRANSFORM_LINKS :
    @staticmethod
    def main(team,response) :
        log.info("Trasforming links box scores for {}".format(team))
        row_list  = TRANSFORM_LINKS.get_game_table(response)
        if not row_list :
            log.warn(response)
            return {}
        ret = TRANSFORM_LINKS.business_logic(row_list)
        log.info("Completed Trasforming links box scores for {}".format(team))
        return ret
    @staticmethod
    def business_logic(row_list) :
        log.debug(row_list)
        date_list = [ ele.text.strip() for ele in row_list[0::4] if BOX_SCORE_RE.match(ele.text) ]
        link_list = [ TRANSFORM_LINKS.get_score(cell) for cell in row_list[2::4]]
        ret = dict(zip(date_list,link_list))
        ret = { key : ret[key] for key in ret if TRANSFORM_LINKS.is_boxscore(ret[key]) }
        log.debug(ret)
        return ret
    @staticmethod
    def get_game_table(response) :
        table = TRANSFORM(response,features="html.parser").find('tbody')
        row_list = table.findAll('tr')
        row_list = [ row.findAll('td') for row in row_list ]
        row_list = [ tr for tr in row_list if len(tr) > 2 ]
        row_list = TRANSFORM_BS4.flatten_table_rows(row_list)
        log.debug(row_list)
        return row_list
    @staticmethod    
    def get_links(**box_scores) :
        dates = list(box_scores.keys())
        if not dates :
            return []
        log.debug(dates)
        dates.sort(key = lambda date: datetime.strptime(date, BOX_SCORE_DATE_FORMAT))
        current = dates[-1]
        log.info(current)
        link = box_scores[current]
        log.debug(link)
        return [link]
    @staticmethod
    def get_score(row) :
        ret = row.findAll('a')
        if not ret :
           ret = row.text.strip()
           log.debug(ret)
           return ret
        ret = [ ele.get('href') for ele in ret]
        ret = [ TRANSFORM_LINKS.transform(link) for link in ret if TRANSFORM_LINKS.is_boxscore(link) ]
        ret = ret[0]
        log.debug(ret)
        return ret
    @staticmethod
    def is_boxscore(link) :
        #if 'contest' not in link :
        #    return False
        return link.endswith('box_score')
    @staticmethod
    def is_stat(link) :
        #if 'contest' not in link :
        #    return False
        return link.endswith('team_stats')
    @staticmethod
    def transform(link) :
        return str(BASE.base_url  + link)
    
class TRANSFORM_BOX_SCORES :
    @staticmethod
    def main(team, url) :
        log.info("Extracting box score for {}".format(team))
        log.debug(url)
        response = EXTRACT_SCORES(url, BASE.params, BASE.headers)
        log.info("Transforming box score for {}".format(team))

        soup = TRANSFORM(response,features="html.parser")
        table_list = soup.findAll('table', attrs={'class':'mytable'})
        ret = TRANSFORM_BOX_SCORES.business_logic(table_list)        
        if ret :
           ret = PD.concat(ret)
        ret['date'] = TRANSFORM_BOX_SCORES.business_logic_find_date(soup)
        ret['link'] = url
        log.debug(ret)
        log.info("Completed transforming box score for {}".format(team))
        return ret
    @staticmethod
    def business_logic(table_list) :
        ret = [ TRANSFORM_BOX_SCORES.transform_score(table) for table in table_list if TRANSFORM_BOX_SCORES.is_score(table) ]
        if not ret :
            ret = [ table.replace('box_score','team_stats') for table in table_list]
            log.debug(ret)
            ret = [ TRANSFORM_BOX_SCORES.transform_stat(table) for table in table_list if TRANSFORM_BOX_SCORES.is_stat(table) ]
            log.debug(ret)
        log.debug(type(ret))
        return ret
    @staticmethod
    def business_logic_find_date(soup) :
        date_field = [ col.text.strip() for col in soup.findAll('td') ]
        date_field = [ col for col in date_field if BOX_SCORE_RE.match(col) ]
        if len(date_field) == 0 :
            date_field = 'NAN'
        else :
            date_field = date_field[0]
        log.debug(date_field)
        return date_field
    @staticmethod
    def is_score(table) :
        log.debug(type(table))
        if not table :
            return False
        tr_list = table.findAll('tr', attrs={'class':'grey_heading'})
        td_list = [ tr.findAll('td') for tr in tr_list ]
        td_list = [ ele.text.strip() for ele in TRANSFORM_BS4.flatten_table_rows(td_list) ]
        td_list = [ td for td in td_list if td in BOX_SCORE_LINGO ]
        if len(td_list) > 0 :
            return False
        return True
    @staticmethod
    def is_stat(table) :
        log.debug(type(table))
        if not table :
            return False
        tr_list = table.findAll('tr', attrs={'class':'grey_heading'})
        td_list = [ tr.findAll('td') for tr in tr_list ]
        td_list = [ ele.text.strip() for ele in TRANSFORM_BS4.flatten_table_rows(td_list) ]
        if len(td_list) > 0 :
            return False
        return True
    @staticmethod
    def transform_score(soup_table) :
        team_name = soup_table.find('tr', attrs={'class':'heading'}).find('td').text.strip()
        log.debug(team_name)
        grey_header_list = soup_table.findAll('tr', attrs={'class':'grey_heading'})
        column_list = [ col.text.strip() for col in grey_header_list[0].findAll('th') ]
        player_list = soup_table.findAll('tr', attrs={'class':'smtext'})
        player_list = [ tr.findAll('td') for tr in player_list ]
        player_list = TRANSFORM_BS4.extract_table_rows(player_list)
        team_totals = grey_header_list[-1]
        team_totals = [ tr.findAll('td') for tr in [team_totals] ]
        team_totals = TRANSFORM_BS4.extract_table_rows(team_totals)
        player_list.extend(team_totals)
        ret = PD.DataFrame(player_list,columns=column_list)
        ret['team'] = team_name
        log.debug(ret)
        return ret
    @staticmethod
    def transform_stat(soup_table) :
        team_name = soup_table.find('tr', attrs={'class':'heading'}).find('td').text.strip()
        log.debug(team_name)
        grey_header_list = soup_table.findAll('tr', attrs={'class':'grey_heading'})
        column_list = [ col.text.strip() for col in grey_header_list[0].findAll('th') ]
        player_list = soup_table.findAll('tr', attrs={'class':'smtext'})
        player_list = [ tr.findAll('td') for tr in player_list ]
        player_list = TRANSFORM_BS4.extract_table_rows(player_list)
        team_totals = grey_header_list[-1]
        team_totals = [ tr.findAll('td') for tr in [team_totals] ]
        team_totals = TRANSFORM_BS4.extract_table_rows(team_totals)
        player_list.extend(team_totals)
        ret = PD.DataFrame(player_list,columns=column_list)
        ret['team'] = team_name
        log.debug(ret)
        return ret
def extract(filename) :
    team_url_list = READ_FILE_INPUT.get_team_list(filename)
    for team in team_url_list :
        log.info("Extracting games for {}".format(team))
        yield team, EXTRACT_TEAMS(team_url_list[team], BASE.params, BASE.headers)
    log.info("Complete Extracting games")
        
def main(filename) :
    ret = PD.DataFrame()
    registered_links = set()
    for team, team_url in extract(filename) :
        box_scores = TRANSFORM_LINKS.main(team,team_url)
        for link in TRANSFORM_LINKS.get_links(**box_scores) :
            if link in registered_links :
                log.info(link)
                continue
            registered_links.add(link)
            score = TRANSFORM_BOX_SCORES.main(team,link)
            log.debug(score)
            ret = PD.concat([ret, score])
#        if len(registered_links) > 6 :
#            break
    return ret.drop_duplicates()
if __name__ == "__main__" :
   sport_list = COMMON.find_files("team_list*csv")
   for filename in sport_list :
       main(filename)
