#!/usr/bin/python
##############################################################
# Program name: NCAA Sports Stats Scraper (Settings file)
# Version: 1.0
##############################################################

#start_url = 'http://stats.ncaa.org/team/inst_team_list?sport_code=MBB&academic_year=' + str(academic_year) + "&division=1" 
#domain_base = 'http://stats.ncaa.org' # Base domain

from copy import deepcopy

class SportExtract() :
            base_url = 'http://stats.ncaa.org'
            headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
            params = {}
            default_params = { "division" : 1 ,
                                "conf_id" : -1,
                                "academic_year" : 2021
                              }
            @staticmethod
            def convert_params(default_args, kvargs) :
                ret = deepcopy(default_args)
                ret.update(kvargs)
                ret = "&".join([ "{}={}".format(key,value) for key, value in ret.items()])
                return "{}/team/inst_team_list?{}".format(SportExtract.base_url,ret)
            @staticmethod
            def parse(**kvargs) :
                ret = deepcopy(SportExtract.default_params)
                ret.update(kvargs)
                ret.update({ key : int(value) for key, value in ret.items() if key in ["conf_id","division","academic_year"] })
                return ret

class Lacrosse() :
            default_params = [{ "sport_code" : "MLA",
                                "division" : 1 #1,2,3
                              }]
            @classmethod
            def url_team_list(cls,**kvargs) :
                kvargs = SportExtract.parse(**kvargs)
                return [ SportExtract.convert_params(params,kvargs) for params in cls.default_params ]
class Basketball() :
            default_params = [{ "sport_code" : "MBB",
                                "division" : 1 #1,2,3
                              }]
            @classmethod
            def url_team_list(cls,**kvargs) :
                kvargs = SportExtract.parse(**kvargs)
                return [ SportExtract.convert_params(params,kvargs) for params in cls.default_params ]
class Football() :
            default_params = [{ "sport_code" : "MFB",
                                "division" : 11  #2,3,11,12 cooresponds to II,III,FBS,FCS
                              }]
            @classmethod
            def url_team_list(cls,**kvargs) :
                kvargs = SportExtract.parse(**kvargs)
                return [ SportExtract.convert_params(params,kvargs) for params in cls.default_params ]
class Soccer() :
            default_params = [{ "sport_code" : "MSO",
                                "division" : 1 #1,2,3
                              }]
            @classmethod
            def url_team_list(cls,**kvargs) :
                kvargs = SportExtract.parse(**kvargs)
                return [ SportExtract.convert_params(params,kvargs) for params in cls.default_params ]
