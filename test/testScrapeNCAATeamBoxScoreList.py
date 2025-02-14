import unittest
import logging as log
import os
from sys import path
from bs4 import BeautifulSoup as TRANSFORM

path.append(os.path.dirname(os.getcwd()))
import libCommon as COMMON
import libScrapeNCAATeamBoxScoreList as TEST

def load_response(filename) :
    filename_list = COMMON.find_files(filename)
    with open(filename_list[0]) as fp :
         return "".join(fp.readlines())

class TestScrapeBoxScore(unittest.TestCase) :
    team_MLA_Navy = None
    team_MLA_Navy_BoxSCore = None
    def setUp(self) : 
        self.team_MLA_Navy = load_response("./test_input/team_MLA_Navy.html")
        self.team_MLA_Navy_BoxSCore = load_response("./test_input/team_MLA_BoxScore.html")
    def testLacrosseBoxScoreList(self) :
        obj = TEST.TRANSFORM_LINKS.main('Navy', self.team_MLA_Navy)
        log.debug(COMMON.pretty_print(obj))
        log.debug(sorted(obj))
    def testLacrosseGetScore(self) :
        #obj_list = [ TEST.TRANSFORM_BOX_SCORES.main(team_list) for team_list in [self.team_MLA_Navy_BoxSCore] ]

        soup = TRANSFORM(self.team_MLA_Navy_BoxSCore,features="html.parser")
        table_list = soup.findAll('table', attrs={'class':'mytable'})
        log.debug(table_list)
        obj_list = TEST.TRANSFORM_BOX_SCORES.business_logic(table_list)
        
        for obj in obj_list :
            obj.to_csv(r'./test_output.csv', index=False)
            f = load_response(r'./test_output.csv')
            log.debug(f)
if __name__ == '__main__' :
   import sys
   log_file = COMMON.build_args(*sys.argv).replace('.py','') + '.log'
   log.basicConfig(filename=log_file, format=COMMON.LOG_FORMAT_TEST, level=log.DEBUG)
   unittest.main()
