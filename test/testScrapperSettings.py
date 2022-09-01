import unittest
import logging as log
import os
from sys import path
import pandas as PD

path.append(os.path.dirname(os.getcwd()))
import libCommon as COMMON
import libScrapeNCAASettingsAlt as TEST2

'''
   "28582": {
      "startDate": "08-27-2022",
      "startTime": "12:30PM ET",
      "startTimeEpoch": "1661617800",
      "title": "Northwestern Nebraska",
      "url": "/game/6005567"
   }
   
   DEBUG [libScrapeNCAASettingsAlt.extract_alt:105] {
   "1st Downs": "23",
   "1st Downs Passing": "16",
   "1st Downs Penalty": "3",
   "1st Downs Rushing": "4",
   "Fourth-Down Conversions": "0-0",
   "Fumbles: Number-Lost": "1-1",
   "Interception Returns: Number-Yards": "0-0",
   "Kickoff Returns: Number-Yards": "3-62",
   "Passing": "355",
   "Passing Attempts": "42",
   "Passing Avg. Per Pass": "0.6",
   "Passing Completions": "25",
   "Passing Interceptions": "0",
   "Penalties: Number-Yards": "1-5",
   "Punt Returns: Number-Yards": "0-0",
   "Punting: Number-Yards": "6-283",
   "Punting: Number-Yards Avg. Per Punt": "47.17",
   "Rushing": "124",
   "Rushing Attempts": "31",
   "Rushing Avg. Per Rush": "4",
   "Third-Down Conversions": "9-16",
   "Total Offense": "541",
   "Total Offense Avg. Per Play": "6.56",
   "Total Offense Plays": "73",
   "color": "#C8102E",
   "homeTeam": "false",
   "path": "/game/6005567",
   "seoName": "nebraska",
   "shortname": "Nebraska",
   "sixCharAbbr": "NEB",
   "startDate": "08-27-2022",
   "startTime": "12:30PM ET",
   "startTimeEpoch": "1661617800",
   "title": "Northwestern Nebraska",
   "url_score": "https://data.ncaa.com/casablanca/game/6005567/gameInfo.json",
   "url_stat": "https://data.ncaa.com/casablanca/game/6005567/teamStats.json"
}

'''
          
def extract(sport, **kvargs):
    ret = []
    for game_value, score_list, stat_value in TEST2.SportExtract.extract_value(sport, **kvargs) :
        stat_value.update(game_value)
        score = 'away'
        if stat_value.get('homeTeam') == 'true' :
            score = 'home'
        score = score_list.get(score)
        if score.get('seo') != stat_value.get('seoName') :
            log.warn("unexpected mismatch seo {} vs {}".format(score.get('seo'),stat_value.get('seoName')))
            continue
        stat_value['score'] = score.get('score')
        log.debug(stat_value) 
        ret.append(stat_value)
        #break
    return sport.pretty(ret)
class TestScraperSettings(unittest.TestCase) :
    def setUp(self) : pass
    @unittest.skip
    def test_Lacrosse(self) :
        ret = extract(TEST2.Lacrosse())
        #ret.dropna(axis = 1, how ='any', inplace = True)
        first = ret[ret.startDate == ret.startDate.min()]
        last = ret[ret.startDate == ret.startDate.max()]
        ret.to_csv('lacrosse_all.csv',index = False, header=True, sep=',')
        first.to_csv('lacrosse_first.csv',index = False, header=True, sep=',')
        last.to_csv('lacrosse_last.csv',index = False, header=True, sep=',')
        log.debug(first)
    @unittest.skip
    def test_Basketball(self) :
        ret = extract(TEST2.Basketball())
        #ret.dropna(axis = 1, how ='any', inplace = True)
        first = ret[ret.startDate == ret.startDate.min()]
        last = ret[ret.startDate == ret.startDate.max()]
        ret.to_csv('basketball_all.csv',index = False, header=True, sep=',')
        first.to_csv('basketball_first.csv',index = False, header=True, sep=',')
        last.to_csv('basketball_last.csv',index = False, header=True, sep=',')
        log.debug(first)
    @unittest.skip
    def testFootball2(self) :
        ret = extract(TEST2.Football(),**{ "year" : 2022})
        #ret.dropna(axis = 1, how ='any', inplace = True)
        ret.to_csv('football_raw.csv',index = False, header=True, sep=',')
    def testFootballEnrich(self) :
        data = PD.read_csv('football_raw.csv')
        data = TEST2.Football_Steve.pretty(data)
        icon = PD.read_csv('../data/icon.csv')
        data = TEST2.Football_Steve.addIcon(data,icon)
        log.debug(data)
        data.to_csv('football_all.csv', index=False)
    @unittest.skip
    def test_Soccer(self) :
        ret = extract(TEST2.Soccer())
        first = ret[ret.startDate == ret.startDate.min()]
        last = ret[ret.startDate == ret.startDate.max()]
        ret.to_csv('soccer_all.csv',index = False, header=True, sep=',')
        first.to_csv('soccer_first.csv',index = False, header=True, sep=',')
        last.to_csv('soccer_last.csv',index = False, header=True, sep=',')
        log.debug(first)
    @unittest.skip
    def test_DateRange(self) :
        football = TEST2.Football()
        log.debug(football.url_game_list())
        lacross = TEST2.Lacrosse()
        lacross_matches = lacross.url_game_list()
        soccer = TEST2.Soccer()
        soccer_matches = soccer.url_game_list()
        basketball = TEST2.Basketball()
        basketball_matches = basketball.url_game_list()
        log.debug("{} {}".format(len(lacross_matches),lacross_matches[:5]))
        log.debug("{} {}".format(len(soccer_matches),soccer_matches[:5]))
        log.debug("{} {}".format(len(basketball_matches),basketball_matches[:5]))
    @unittest.skip
    def test_StatsExtract(self) :
        args = {    "url_score": "https://data.ncaa.com/casablanca/game/6005567/gameInfo.json",
                "url_stat": "https://data.ncaa.com/casablanca/game/6005567/teamStats.json"
        }
        stat = TEST2.StatsExtract.get_stat_list(args["url_stat"])
        log.debug(stat)
        score = TEST2.ExtractPage.extract_score(TEST2.Football(),**args)
        log.debug(score)
        
if __name__ == '__main__' :
   import sys
   log_file = COMMON.build_args(*sys.argv).replace('.py','') + '.log'
   log.basicConfig(filename=log_file, format=COMMON.LOG_FORMAT_TEST, level=log.DEBUG)
   unittest.main()
