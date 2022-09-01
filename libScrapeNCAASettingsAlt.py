# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 23:54:58 2022

@author: emers

$0.42 per scraping

"""

#!/usr/bin/python
##############################################################
# Program name: NCAA Sports Stats Scraper (Settings file)
# Version: 1.0
##############################################################
from copy import deepcopy
import logging as log
import datetime
import pandas as PD

from libCommon import pretty_print, find_subset
from libScrapeNCAAFunctions import try_02, validate as validate_url

#Cookie: _stats_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWNhOTNiMzJhZWRjOTRkNjBmMTZkMjJiNzRlZGQ1OTA5BjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMWtGdXo2WWhBSzQ1a1c3anlzU2JEVU5hb2tWQ2lhZ0RiNHNWMjc5SjNoUWM9BjsARg%3D%3D--07eaa7fdd1c60bc5a8b8cb98735a57db88e54b60; RT="z=1&dm=ncaa.org&si=2sc49f8mhox&ss=l0bdzvb2&sl=0&tt=0"
#If-None-Match: W/"1350915d74096308fbff5f079a1e055b"

class SportExtract() :
            url_weekly = 'https://data.ncaa.com/casablanca/scoreboard/{sport_code}/{year}/{week}/scoreboard.json'
            url_stats_football = 'https://data.ncaa.com/casablanca{url}/teamStats.json'
            url_score_football = 'https://data.ncaa.com/casablanca{url}/gameInfo.json'
            url_stats_lacrosse = 'https://data.ncaa.com/casablanca{url}/boxscore.json'
            headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                       'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
                       ,'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
                       ,'Accept-Encoding' : 'gzip, deflate, br'
                       ,'Accept-Language': 'en-US,en;q=0.9'
                       ,'Cache-Control': 'public'
                       #,'Connection': 'keep-alive'
                       ,'Host': 'data.ncaa.com'
                       ,'sec-gpc': '1'
                       ,'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"'
                       ,'Upgrade-Insecure-Requests': '1' 
                       #,'Cookie' : '_stats_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWNhOTNiMzJhZWRjOTRkNjBmMTZkMjJiNzRlZGQ1OTA5BjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMWtGdXo2WWhBSzQ1a1c3anlzU2JEVU5hb2tWQ2lhZ0RiNHNWMjc5SjNoUWM9BjsARg==--07eaa7fdd1c60bc5a8b8cb98735a57db88e54b60; RT="z=1&dm=ncaa.org&si=1uk94hj66ee&ss=l0bdzvb2&sl=0&tt=0"'
                       , 'Cookie' : '_gcl_au=1.1.485433972.1651778693; AMCVS_7FF852E2556756057F000101@AdobeOrg=1; _fbp=fb.1.1651778694996.374165749; __gads=ID=f37898144f566074:T=1651778695:S=ALNI_MZHKnW2gxt0g3Rtql9n2xeJJwuH9w; s_ecid=MCMID|85767230977939443311930608067594513607; s_cc=true; WMUKID_STABLE=88c3fd7c-7aaf-4781-af98-f226d37a620d; CDPID={"cdpId":"b1fb7e54-4fcf-4285-a02a-b2cb1bec37c1","wmukId":"88c3fd7c-7aaf-4781-af98-f226d37a620d"}; sendAuthToken=false; sendHHID=false; isInAuthTokenExperiment=false; isInHHIDExperiment=false; sendWMSegs=false; _cb=ZeE5CCxHPTWCxurF3; AMCV_7FF852E2556756057F000101@AdobeOrg=-1124106680|MCIDTS|19167|MCMID|85767230977939443311930608067594513607|MCAAMLH-1656560634|7|MCAAMB-1656560634|RKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y|MCOPTOUT-1655963034s|NONE|MCAID|NONE|vVersion|5.2.0; hhidVersion=38; idrTimestamp="2022-06-23T03:43:55.328Z"; _v__chartbeat3=SwSWsBC8Jcm35htj; bea4r=62b3e5f5ba41450a3f85a100142579c8; umto=1; hkgc=5621516d-8a23-11ec-ba50-11a7500c0003; goiz=d719dfb56fb34c039f4985a2a27daac0; zwmc=8445067193507211047; bea4=o2642_7062929716609386160; _ga=GA1.2.345788970.1655956981; _gid=GA1.2.1374650772.1655956981; ncaa_ga=GA1.2.345788970.1655956981; ncaa_ga_gid=GA1.2.571905446.1655956981; OptanonControl=ccc=US&csc=&cic=1&otvers=6.35.0&pctm=2022-06-23T04:03:00.459Z&reg=ccpa&ustcs=1YYN&vers=3.1.14; usprivacy=1YNN; RT="z=1&dm=ncaa.com&si=q2g8kmeej0q&ss=l4qhci1z&sl=0&tt=0"; _chartbeat2=.1651778692805.1655958169480.0000000000000011.Co-HV1CoOk-FBbwCEVhXrVaBsnBE0.15; OptanonConsent=isIABGlobal=false&datestamp=Thu+Jun+23+2022+00:22:49+GMT-0400+(Eastern+Daylight+Time)&version=6.35.0&hosts=&consentId=d03bb987-151e-4752-9365-bb5717a2f80b&interactionCount=0&landingPath=NotLandingPage&groups=BG173:1,smv:1,pfv:1,pzv:1,ven:1,sav:1,adv:1,pf:1,sa:1,ad:1,sm:1,tdc:1,2:1,ai:1,fc:1,tc:1,pcd:1,req:1&AwaitingReconsent=false; cto_bundle=IHb4HF92T0slMkJhRHJCU29RV0p2b2wlMkZxY3dvMTZidHpzZzBWRW9SRXZRejRhNEowWUhydFR4TjdjJTJGV1ZRaSUyRlFxanZLNjFuRkNXcXlxQk1oV0kxZHlNdW5BSEc4MFA3MGdxaUQ0OXM1cXdlJTJCVkQ0OWpMOGZRbUU4cThjR0FwZVlWMmhMQmdXcHZWRkI1NkE0ZEI1MGJYNDZPMzN3JTNEJTNE; psmPageLoadId=1; s_sq=sidncaa=%26pid%3Dhttps%253A%252F%252Fwww.ncaa.com%252Fscoreboard%252Ffootball%252Ffbs%26oid%3Dhttps%253A%252F%252Fwww.ncaa.com%252Fscoreboard%252Ffootball%252Ffbs%252F2021%252F02%252Fall-conf%26ot%3DA; __gpi=UID=000004a4d135c801:T=1651778695:RT=1656022528:S=ALNI_MZm8WzR52TMH8_3BUv-nbzcRZ8EEA; psmSessionId=3ef4465b-fe2f-40bd-bb03-d1e2de6e4a22; psmSessionStart=2022-06-24T02:03:26.888Z; psmLastActiveTimestamp=2022-06-24T02:07:26.891Z; akacd_ems=1656037089~rv=58~id=6aaa75c94b5c60836f87429bed7124ae'
                       }
            
            params = {}
            default_params = { "year" : 2021
                              }
            @staticmethod
            def extract(sport, **kvargs):
                ret = []
                for game_value, score_list, stat_value in SportExtract.extract_value(sport, **kvargs) :
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
            @staticmethod
            def extract_value(sport, **kvargs):
                for count, game_url in enumerate(sport.url_game_list(**kvargs)) :
                    for game_key, game_value in GameExtract.get_team_list(sport,game_url).items() :
                            game_value['Week'] = count + 1
                            score_list = ExtractPage.extract_score(sport,**game_value)
                            url_stat = game_value.get('url_stat')
                            for stat_key, stat_value in StatsExtract.get_stat_list(url_stat).items():
                                yield game_value, score_list, stat_value
            @staticmethod
            def get_url_game_list(**ret) :
                ret = SportExtract.convert_params(ret)
                ret = SportExtract.get_date_range(**ret)
                ret = [ SportExtract.url_weekly.format(**params) for params in ret ]
                ret = [ url for url in ret if validate_url(url,SportExtract.headers) ]
                msg = pretty_print(ret)
                log.debug(msg)
                return ret
            @staticmethod
            def convert_params(kvargs) :
                if kvargs :
                   log.debug(kvargs)
                else :
                   log.warn("no args")
                ret = deepcopy(SportExtract.default_params)
                ret.update(kvargs)
                return ret
            @staticmethod
            def addWeeks(week,**kvargs) :
                ret = deepcopy(kvargs)
                ret['week'] = week
                return ret
            @staticmethod
            def get_date_range(**kvargs) :
                year = int(kvargs.get('year',2021))
                month = int(kvargs.get('month',1))
                sport_code = kvargs.get('sport_code','fakesport/d1')
                param_date = kvargs.get('start',datetime.datetime(year,month,1))
                param_range = int(kvargs.get('range',12))
                ret = [ param_date + datetime.timedelta(days=days) for days in range(0,param_range) ]
                ret = [ { 'sport_code' : sport_code,'year' : x.strftime("%Y"), 'week' : x.strftime("%m/%d") } for x in ret ]
                #msg = pretty_print(ret)
                #log.debug(msg)
                return ret
class ExtractPage() :
        @classmethod
        def extract(cls,sport, url) :
            ret = [ stat for stat in cls.extract_stats(sport, url)]
            #msg = pretty_print(ret)
            #log.debug(msg)
            return ret
        @classmethod
        def extract_stats(cls,sport, url) :
            for game_key, game_value in GameExtract.get_team_list(sport,url).items() :
                team_url = game_value.get('url_stat')
                for stat_key, stat_value in StatsExtract.get_stat_list(team_url).items():
                    stat_value.update(game_value)
                    msg = pretty_print(stat_value)
                    log.debug(msg)
                    yield stat_value
        @classmethod
        def extract_score(cls,sport, **ret) :
                log.debug(ret)
                url_score = ret.get('url_score')
                return ScoreExtract.get_score(sport,url_score)
class ScoreExtract :
        @classmethod
        def get_score(cls,sport,url) :
            try :
                log.debug(url)
                response = try_02(url,SportExtract.headers) 
                return cls.extract(sport, **response.json())
            except :
                return {}
        @classmethod
        def extract(cls,sport, **args) :
            ret = { key : value for key, value in args.items() if key in ['home','away']}
            for key, value in ret.items() :
                names = value.pop('names')
                value.update(names)
                ret[key] = { x : y for x, y in value.items() if x in sport.score_columns }
            msg = pretty_print(ret)
            log.debug(msg)
            return ret
      
class GameExtract() :
        fields = ["away","gameID", "home", "startTime", "startDate", "startTimeEpoch", "title", "url"]
        fields = ["gameID", "startTime", "startDate", "startTimeEpoch", "title", "url"]
        @classmethod
        def get_team_list(cls,sport,url) :
            try :
                response = try_02(url,SportExtract.headers) 
                return cls.extract(sport, **response.json())
            except :
                return {}
        @classmethod
        def extract(cls,sport, **kvargs) :
            args = cls.get_game_list(**kvargs)
            args = { r.pop('gameID','0') : r for r in args}
            msg = pretty_print(args)
            log.debug(msg)
            stats = { key : cls.get_meta(sport, **value) for key, value in args.items()}
            msg = pretty_print(stats)
            log.debug(msg)
            return stats
        @classmethod
        def get_game_list(cls,**kvargs) :
            ret = kvargs.get('games')
            if not isinstance(ret,list) :
                ret = [ ret ]
            ret = [ find_subset(field.get('game'),*cls.fields) for field in ret ]
            #msg = pretty_print(ret)
            #log.debug(msg)
            return ret
        @classmethod
        def get_meta(cls,sport, **record) :
            msg = pretty_print(record)
            log.debug(msg)
            url_stat = sport.get_stat_url().format(**record)
            url_score = sport.get_score_url().format(**record)
            log.info(url_stat)
            record['path'] = record.pop('url')
            record['url_stat'] = url_stat
            record['url_score'] = url_score
            msg = pretty_print(record)
            log.debug(msg)
            return record
class StatsExtract() :
        columns = ['stats','goalieTotals','playerTotals','totalStats']
        @classmethod
        def get_stat_list(cls,url) :
            try :
              response = try_02(url ,SportExtract.headers)
              return cls.extract(**response.json())
            except :
                return {}
        @classmethod
        def extract(cls,**kvargs) :
            ret = { key: value for key, value in cls.extract_alt(**kvargs) }
            msg = pretty_print(ret)
            log.debug(msg)
            return ret
        @classmethod
        def extract_alt(cls,**kvargs) :
            teams = kvargs.pop('meta').pop('teams')
            stats = kvargs.pop('teams')
            ret = [ cls.extract_stats(**team) for team in stats ]
            teams = { str(data.pop('id','0')) : data for data in teams}
            msg = pretty_print(teams)
            log.debug(msg)
            ret = { str(data.pop('teamId','0')) : data.pop('stats',{}) for data in ret}
            for key, record in ret.items() :
                team_meta = teams.get(key,{})
                record.update(**team_meta)
                log.debug(pretty_print(record))
                yield key, record
        @classmethod
        def extract_stats(cls,**kvargs) :
            log.debug((sorted(kvargs)))
            teamID = kvargs.pop('teamId')
            stats = { key : value for key,value in kvargs.items() if key in cls.columns}
            stats1 = stats.pop('stats',None)
            if isinstance(stats1,list) :
                stats = [ cls.extract_breakdown(**stat) for stat in stats1]
            else :
                stats = ['goalieTotals','playerTotals','totalStats']
                stats = [ value for key, value in kvargs.items() if key in stats ]
                
            ret = {}
            [ ret.update(stat) for stat in stats]
            ret = { 'teamId' : teamID, 'stats' : ret}
            msg = pretty_print(ret)
            log.debug(msg)
            return ret
        @classmethod
        def extract_breakdown(cls,**kvargs) :
            breakdown = kvargs.pop('breakdown',[] )
            stat = kvargs.pop('stat')
            ret = { stat : kvargs.pop('data')}
            breakdown = [cls.extract_breakdown(**stat) for stat in breakdown ]
            if len(breakdown) == 0 :
                return ret
            bd = {}
            [ bd.update(stat) for stat in breakdown ]
            breakdown = { stat + " " + key : value for (key,value) in bd.items() }
            ret.update(breakdown)
            return ret
        
'''
    2022 Season
    1054 total records ~1000
    ~2.5 minutes per record ~42 hours
    ~10 dollars per hour ~$420
    ~12 months ~$35 per month
'''
class Lacrosse() :
        default_params = { "sport_code" : "lacrosse-men/d1"
                            ,'range':160, 'month':1 }
        basic_columns = ['startDate', 'startTime', 'title', 'homeTeam','sixCharAbbr','shortName','nickName']
        @classmethod
        def url_game_list(cls,**kvargs) :
            ret = deepcopy(cls.default_params)
            ret.update(kvargs)
            ret.update({ 'year':2022})
            return SportExtract.get_url_game_list(**ret)
        @classmethod
        def get_stat_url(cls) :
            return SportExtract.url_stats_lacrosse
        @classmethod
        def get_score_url(cls) :
            return SportExtract.url_score_football
        @classmethod
        def pretty(cls,data) :                
            ret = PD.DataFrame(data)
            log.debug(list(ret.columns))
            drop = [ name for name in list(ret.columns) if name in ['url', 'color ','path','startTimeEpoch','seoName']]
            ret.drop(drop, axis=1, inplace=True)
            columns = cls.sort_columns(*list(ret.columns))
            ret = ret.reindex(columns=columns)
            ret['startDate'] = PD.to_datetime(ret['startDate'], format='%m-%d-%Y')
            return ret
        @classmethod
        def sort_columns(cls,*ref) :                
            ret=deepcopy(cls.basic_columns)
            ret.extend([key for key in sorted(ref) if key not in cls.basic_columns])
            log.debug(ret)
            return ret
'''
    2022 Season
    12054 total records ~12000
    ~2.5 minutes per record ~500 hours
    ~10 dollars per hour ~$5,000
    ~12 months ~$415 per month
'''
class Basketball() :
        default_params = { "sport_code" : "basketball-men/d1"
                            ,'range':220, 'month': 10}
        basic_columns = ['startDate', 'startTime', 'title', 'homeTeam','sixCharAbbr','shortName','nickName']
        @classmethod
        def url_game_list(cls,**kvargs) :
            ret = deepcopy(cls.default_params)
            ret.update(kvargs)
            ret.update({ 'year':2021})
            return SportExtract.get_url_game_list(**ret)
        @classmethod
        def get_stat_url(cls) :
            return SportExtract.url_stats_lacrosse
        @classmethod
        def get_score_url(cls) :
            return SportExtract.url_score_football
        @classmethod
        def pretty(cls,data) :                
            ret = PD.DataFrame(data)
            log.debug(list(ret.columns))
            drop = [ name for name in list(ret.columns) if name in ['url', 'color ','path','startTimeEpoch','seoName']]
            ret.drop(drop, axis=1, inplace=True)
            columns = cls.sort_columns(*list(ret.columns))
            ret = ret.reindex(columns=columns)
            ret['startDate'] = PD.to_datetime(ret['startDate'], format='%m-%d-%Y')
            return ret
        @classmethod
        def sort_columns(cls,*ref) :                
            ret=deepcopy(cls.basic_columns)
            ret.extend([key for key in sorted(ref) if key not in cls.basic_columns])
            log.debug(ret)
            return ret
'''
    2021 Season
    3544 total records ~3500
    ~2.5 minutes per record ~146 hours
    ~10 dollars per hour ~$1470
    ~12 months ~$120 per month
'''
class Soccer() :
        default_params = { "sport_code" : "soccer-men/d1"
                            ,'range':160, 'month': 8}
        basic_columns = ['startDate', 'startTime', 'title', 'homeTeam','sixCharAbbr','shortName','nickName']
        @classmethod
        def url_game_list(cls,**kvargs) :
            ret = deepcopy(cls.default_params)
            ret.update(kvargs)
            ret.update({ 'year':2021})
            return SportExtract.get_url_game_list(**ret)
        @classmethod
        def get_stat_url(cls) :
            return SportExtract.url_stats_lacrosse
        @classmethod
        def get_score_url(cls) :
            return SportExtract.url_score_football
        @classmethod
        def pretty(cls,data) :                
            ret = PD.DataFrame(data)
            log.debug(list(ret.columns))
            drop = [ name for name in list(ret.columns) if name in ['url', 'color ','path','startTimeEpoch','seoName']]
            ret.drop(drop, axis=1, inplace=True)
            columns = cls.sort_columns(*list(ret.columns))
            ret = ret.reindex(columns=columns)
            ret['startDate'] = PD.to_datetime(ret['startDate'], format='%m-%d-%Y')
            return ret
        @classmethod
        def sort_columns(cls,*ref) :                
            ret=deepcopy(cls.basic_columns)
            ret.extend([key for key in sorted(ref) if key not in cls.basic_columns])
            log.debug(ret)
            return ret
'''
    2021 Season
    1787 total records ~1800
    ~2.5 minutes per record ~75 hours
    ~10 dollars per hour ~$750
    ~12 months ~$65 per month
'''
class Football() :
        default_params = { "sport_code" : "football/fbs"
                         }
        basic_columns = ['startDate', 'startTime', 'homeTeam', 'shortname', 'title']
        default_columns = ['1st Downs', 'Passing', 'Passing Interceptions', 'Rushing',  'Total Offense', 'Total Offense Plays', 'Fumbles: Number-Lost','Punting: Number-Yards', 'Fourth-Down Conversions', 'Fumbles:Number-Lost', 'Penalties: Number-Yards', 'Third-Down Conversions']
        drop_columns = ['url', 'color ','path','startTimeEpoch','seoName','sixCharAbbr']
        score_columns = ["6Char","full","score","seo","short"]

        @classmethod
        def url_game_list(cls,**kvargs) :
            ret = deepcopy(cls.default_params)
            ret.update(kvargs)
            ret = SportExtract.convert_params(ret)
            weeks = cls.get_weeks()
            [ w.update(ret) for w in weeks ]
            ret = [ SportExtract.url_weekly.format(**params) for params in weeks ]
            msg = pretty_print(ret)
            log.debug(msg)
            return ret
        @classmethod
        def get_stat_url(cls) :
            return SportExtract.url_stats_football
        @classmethod
        def get_score_url(cls) :
            return SportExtract.url_score_football
        @classmethod
        def get_weeks(cls) :
            ret = [ str(week).rjust(2,'0') for week in range(1,16 ) ]
            ret.append('P')
            ret = [ {'week' : w } for w in ret ]
            log.debug(ret)
            return ret
        @classmethod
        def pretty(cls,data) :                
            ret = PD.DataFrame(data)
            ret['homeTeam'] = ret['homeTeam'].replace(['true'],'Home')
            ret['homeTeam'] = ret['homeTeam'].replace(['false'],'Away')
            ret['startDate'] = PD.to_datetime(ret['startDate'], format='%m-%d-%Y')
            return ret
        @classmethod
        def sort_columns(cls,*ref) :                
            ret=deepcopy(cls.basic_columns)
            ret.extend([key for key in sorted(ref) if key in cls.default_columns])
            log.debug(ret)
            return ret
                
class Football_Steve() :
        basic_columns_pre = ['startDate', 'startTime', 'homeTeam', 'shortname', 'title', 'score','week']
        basic_columns_post = ['startDate', 'startTime', 'Home Team', 'Name', 'title', 'score']
        default_columns_pre = ['1st Downs', 'Passing', 'Passing Interceptions', 'Rushing',  'Total Offense', 'Total Offense Plays', 'Fumbles: Number-Lost','Punting: Number-Yards', 'Fourth-Down Conversions', 'Fumbles:Number-Lost', 'Penalties: Number-Yards', 'Third-Down Conversions']
        default_columns_post = ['1st Downs', 'Passing', 'Passing Interceptions', 'Rushing',  'Total Offense', 'Total Offense Plays', 'Fumbles: Number-Lost','Punting: Number-Yards', 'Fourth-Down Conversions', 'Fumbles:Number-Lost', 'Penalties: Number-Yards', 'Third-Down Conversions']
        rename = {"homeTeam":"Home Team", "shortname" : "Team Name"}
        @classmethod
        def pretty(cls,data) :                
            ret = PD.DataFrame(data)
            log.debug((len(ret.columns),list(ret.columns)))
            
            columns=deepcopy(cls.basic_columns_pre)
            columns.extend(cls.default_columns_pre)
            columns = [key for key in columns if key in sorted(list(ret.columns)) ]
            #log.debug(columns)
            
            ret = ret[columns]
            ret = ret.reindex(columns=columns)
            ret = ret.rename(columns=cls.rename)
            log.debug((len(ret.columns),list(ret.columns)))
            log.debug(ret.head())
            return ret
        @classmethod
        def addIcon(cls,ret,icon) :
            ret = ret.merge(icon, left_on='Team Name', right_on='Team',how="outer")
            ret['Icon'].fillna(ret['Team Name'],inplace=True)
            ret = ret[ ~(ret['startDate'].isna() & ret['startTime'].isna()) ]
            ret = ret.rename(columns={'Icon':'Name'})

            columns = deepcopy(cls.basic_columns_post)
            columns.extend(cls.default_columns_post)
            columns = [key for key in columns if key in sorted(list(ret.columns)) ]
            log.debug((len(ret.columns),list(ret.columns)))

            ret.sort_values(by=columns,inplace=True,ascending=False)
            ret = ret[columns]
            return ret
        @classmethod
        def sort_columns_all(cls,*ref) :                
            ret=deepcopy(cls.basic_columns)
            ret.extend([key for key in sorted(ref) if "1st Down" in key])
            ret.extend([key for key in sorted(ref) if "Passing" in key])
            ret.extend([key for key in sorted(ref) if "Rushing" in key])
            ret.extend([key for key in sorted(ref) if "Offense" in key])
            ret.extend([key for key in sorted(ref) if "Punt" in key])
            ref = [key for key in sorted(ref) if key not in ret]
            ret.extend(ref)
            log.debug(ret)
            return ret
