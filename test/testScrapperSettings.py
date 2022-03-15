import unittest
import logging as log
import os
from sys import path

path.append(os.path.dirname(os.getcwd()))
import libCommon as COMMON
import libScrapeNCAASettings as TEST

class TestScraperSettings(unittest.TestCase) :
    def setUp(self) : pass
    def testLacrosse(self) :
        sport = TEST.Lacrosse()
        log.debug(sport.url_team_list())
    def testBasketball(self) :
        sport = TEST.Basketball()
        log.debug(sport.url_team_list())
    def testFootball(self) :
        sport = TEST.Football()
        log.debug(sport.url_team_list())
    def testSoccer(self) :
        sport = TEST.Soccer()
        log.debug(sport.url_team_list())

if __name__ == '__main__' :
   import sys
   log_file = COMMON.build_args(*sys.argv).replace('.py','') + '.log'
   log.basicConfig(filename=log_file, format=COMMON.LOG_FORMAT_TEST, level=log.DEBUG)
   unittest.main()
