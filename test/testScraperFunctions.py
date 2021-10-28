from sys import path
path.append("../")

import libCommon as COMMON
import scraperfunctions as TEST
import unittest
import logging as log

class TestScraperFunctions(unittest.TestCase) :
    def setUp(self) : 
        COMMON.mkdir("../log")

if __name__ == '__main__' :
   import sys
   log_file = COMMON.build_args(*sys.argv).replace('.py','') + '.log'
   log_file = COMMON.build_path('../log',log_file)
   COMMON.remove_file(log_file)
   print(log_file)
   log.basicConfig(filename=log_file, format=COMMON.LOG_FORMAT_TEST, level=log.DEBUG)
   #log.basicConfig(stream = sys.stdout, format=COMMON.LOG_FORMAT_TEST, level=log.DEBUG)
   unittest.main()
