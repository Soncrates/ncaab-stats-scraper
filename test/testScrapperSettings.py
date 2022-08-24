import unittest
import logging as log
import os
from sys import path

path.append(os.path.dirname(os.getcwd()))
import libCommon as COMMON
import libScrapeNCAASettingsAlt as TEST2

def extract(sport, **kvargs):
    ret = []
    [ ret.extend(TEST2.ExtractPage.extract(sport, url)) for url in sport.url_game_list(**kvargs) ]
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
    def testFootball2(self) :
        ret = extract(TEST2.Football())
        #ret.dropna(axis = 1, how ='any', inplace = True)
        first = ret[ret.startDate == ret.startDate.min()]
        last = ret[ret.startDate == ret.startDate.max()]
        home = ret[ret['Home Team'] == 'Home']
        away = ret[ret['Home Team'] == 'Away']
        home = ret[ret['Home Team'] == 'Home'] 
        ret.to_csv('football_all.csv',index = False, header=True, sep=',')
        first.to_csv('football_first.csv',index = False, header=True, sep=',')
        last.to_csv('football_last.csv',index = False, header=True, sep=',')
        home.to_csv('football_home.csv',index = False, header=True, sep=',')
        away.to_csv('football_away.csv',index = False, header=True, sep=',')
        log.debug(first)
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

if __name__ == '__main__' :
   import sys
   log_file = COMMON.build_args(*sys.argv).replace('.py','') + '.log'
   log.basicConfig(filename=log_file, format=COMMON.LOG_FORMAT_TEST, level=log.DEBUG)
   unittest.main()
