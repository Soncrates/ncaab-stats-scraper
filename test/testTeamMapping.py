from sys import path
path.append("../")

import libCommon as COMMON
import logging as log
import unittest
import create_team_mappings as TEST

def load_response(filename) :
    filename_list = COMMON.find_files(filename)
    with open(filename_list[0]) as fp :
         return "".join(fp.readlines())
class TestScraperFunctions(unittest.TestCase) :
    team_list_MLA = None
    def setUp(self) : 
        self.team_list_MLA = load_response("./test_input/team_list_MLA.html")
    def testLacrosseStep02(self) :
        obj = [ TEST.step01_parse_response(team_list) for team_list in [self.team_list_MLA] ]
        obj = TEST.merge_divisions(*obj)
        log.debug(COMMON.pretty_print(obj))

if __name__ == '__main__' :
   import sys
   log_file = COMMON.build_args(*sys.argv).replace('.py','') + '.log'
   log_file = COMMON.build_path('../log',log_file)
   COMMON.remove_file(log_file)
   COMMON.mkdir("../log")
   log.basicConfig(filename=log_file, format=COMMON.LOG_FORMAT_TEST, level=log.DEBUG)
   unittest.main()
