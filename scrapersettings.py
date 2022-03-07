#!/usr/bin/python
##############################################################
# Program name: NCAA Sports Stats Scraper (Settings file)
# Version: 1.0
##############################################################
from copy import deepcopy
import logging as log


#Cookie: _stats_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWNhOTNiMzJhZWRjOTRkNjBmMTZkMjJiNzRlZGQ1OTA5BjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMWtGdXo2WWhBSzQ1a1c3anlzU2JEVU5hb2tWQ2lhZ0RiNHNWMjc5SjNoUWM9BjsARg%3D%3D--07eaa7fdd1c60bc5a8b8cb98735a57db88e54b60; RT="z=1&dm=ncaa.org&si=2sc49f8mhox&ss=l0bdzvb2&sl=0&tt=0"
#If-None-Match: W/"1350915d74096308fbff5f079a1e055b"

class SportExtract() :
            base_url = 'http://stats.ncaa.org'
            headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                       'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
                       ,'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
                       ,'Accept-Encoding' : 'gzip, deflate'
                       ,'Accept-Language': 'en-US,en;q=0.9'
                       ,'Cache-Control': 'max-age=0'
                       ,'Connection': 'keep-alive'
                       ,'Host': 'stats.ncaa.org'
                       ,'sec-gpc': '1'
                       ,'Upgrade-Insecure-Requests': '1' 
                       ,'Cookie' : '_stats_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWNhOTNiMzJhZWRjOTRkNjBmMTZkMjJiNzRlZGQ1OTA5BjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMWtGdXo2WWhBSzQ1a1c3anlzU2JEVU5hb2tWQ2lhZ0RiNHNWMjc5SjNoUWM9BjsARg==--07eaa7fdd1c60bc5a8b8cb98735a57db88e54b60; RT="z=1&dm=ncaa.org&si=1uk94hj66ee&ss=l0bdzvb2&sl=0&tt=0"'
                       }
            
            params = {}
            default_params = { "division" : 1 ,
                                "conf_id" : -1,
                                "academic_year" : 2021
                              }
            @staticmethod
            def convert_params(params,kvargs) :
                if kvargs :
                   log.debug(kvargs)
                else :
                   log.warn("no args")
                ret = deepcopy(SportExtract.default_params)
                ret.update(params)
                ret.update(kvargs)
                ret = "&".join([ "{}={}".format(key,value) for key, value in ret.items()])
                log.debug(ret)
                return "{}/team/inst_team_list?{}".format(SportExtract.base_url,ret)
            @staticmethod
            def parse(**ret) :
                if ret :
                   log.debug(ret)
                else :
                   log.warn("no args")
                ret.update({ key : int(value) for key, value in ret.items() if key in ["conf_id","division","academic_year"] })
                log.debug(ret)
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
