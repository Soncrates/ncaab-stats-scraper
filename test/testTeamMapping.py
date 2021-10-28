from sys import path
path.append("../")

import libCommon as COMMON
from scrapersettings import Lacrosse, Football, Basketball, Soccer, SportExtract as BASE
import create_team_mappings as TEST
import unittest
import logging as log

class TestScraperFunctions(unittest.TestCase) :
    def setUp(self) : pass
    def testLacrosseStep01(self) :
        obj = TEST.team_list_by_sport(*Lacrosse().url_team_list())
        log.debug(obj)

if __name__ == '__main__' :
   import sys
   log_file = COMMON.build_args(*sys.argv).replace('.py','') + '.log'
   log_file = COMMON.build_path('../log',log_file)
   COMMON.remove_file(log_file)
   COMMON.mkdir("../log")
   print(log_file)
   log.basicConfig(filename=log_file, format=COMMON.LOG_FORMAT_TEST, level=log.DEBUG)
   #log.basicConfig(stream = sys.stdout, format=COMMON.LOG_FORMAT_TEST, level=log.DEBUG)
   unittest.main()
