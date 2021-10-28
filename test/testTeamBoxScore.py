from sys import path
path.append("../")

import libCommon as COMMON
from scrapersettings import Lacrosse, Football, Basketball, Soccer, SportExtract as BASE
import create_box_scores as TEST
import unittest
import logging as log


def load_response(filename) :
    filename_list = COMMON.find_files(filename)
    with open(filename_list[0]) as fp :
         return "".join(fp.readlines())
class TestScrapeBoxScore(unittest.TestCase) :
    team_MLA_Navy = None
    def setUp(self) : 
        self.team_MLA_Navy = load_response("./test_input/team_MLA_Navy.html")
    def testLacrosseStep02(self) :
        obj = [ TEST.step02_parse_response_for_box_scores(team_list) for team_list in [self.team_MLA_Navy] ]
        log.debug(COMMON.pretty_print(obj))

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
