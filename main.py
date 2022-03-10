from copy import deepcopy
import pandas as PD
from datetime import datetime
from math import floor
import logging as log

import libCommon as COMMON
from libEmail import EMAIL, CLIENTS
import scrapersettings as SPORT
import create_team_mappings as TEAMS
import create_box_scores as SCORES

from libCustom import PERSONAL

HELP = "1) Football, 2) Basketball, 3) Soccer, 4) Lacrosse"

most_recent_date = '1970_01_01'
client_list =  [{"user_email" : "justcollegefootball@gmail.com","first_name":"Steve","last_name":"Hiegel", "user_login":"Steve"},
                {"user_email" : "chriswithteal@gmail.com","first_name":"Martiel", "last_name":"and Staff", "user_login" : "Chris and Teal"}]
client_list =  [{"user_email" : "justcollegefootball@gmail.com","first_name":"Steve","last_name":"Hiegel", "user_login":"Steve"},
                {"user_email" : "martiel@martielbeatty.com","first_name":"Martiel", "last_name":"and Staff", "user_login" : "Chris and Teal"}]
#client_list =  [ {"user_email" : "chriswithteal@gmail.com","first_name":"Martiel", "last_name":"and Staff", "user_login" : "Chris and Teal"}]


class CUSTOM:
    _from = PERSONAL._from
    pswd = PERSONAL.pswd
    subject="Scores {sport_code}, {date} for {user_login}"
    body ="""
Good morning, {first_name} {last_name}

You are receiving this email as a test of our new automated system of ncaab score scraper.

The last recorded {sport_code} games occurred on {date}
There were {count} games played ({sport_code}).

Previous games

{summary}



"""


def prep(**args) :
    log.debug(args)
    sport = int(args.get('sport','1'))
    if sport == 1 :
       sport = SPORT.Football()
    elif sport == 2 :
       sport = SPORT.Basketball()
    elif sport == 3 :
       sport = SPORT.Soccer()
    elif sport == 4 :
       sport = SPORT.Lacrosse()
    if isinstance(sport,int) : 
        raise ValueError("Unexpected value for sport : {}".fomrat(sport))
        
    x = deepcopy(sport.default_params[0])
    x['date'] = '{date}' 
    x['team_year']= datetime.now().strftime("%Y")
    x['today']= datetime.now().strftime("%Y_%m_%d")
    log.debug(x)
     
    filename =  "output_team_list_{sport_code}_{team_year}.csv".format(**x)
    output = 'output_team_scores_{sport_code}_{date}.csv'.format(**x)
    summary = 'output_game_summary_{sport_code}_{today}.csv'.format(**x)
    log.info(filename)
    log.info(output)
    log.info(summary)
    return sport, filename, output, summary

def business_logic(obj, sport, output) :
    log.debug(obj)
    obj = obj[obj['Player'] == 'Totals'] 
    obj.drop(['Player', 'Pos','link'], axis=1, inplace=True)
    obj['date'] = PD.to_datetime(obj['date']).dt.normalize()
    most_recent_date = obj['date'].max()
    obj = obj[obj['date'] == most_recent_date] 
    #obj=obj.reindex(columns= ['Rounded_score', 'Gender', 'Score','Name'])

    x = deepcopy(sport.default_params[0])
    x['date'] = most_recent_date.strftime("%Y_%m_%d")
    x['count'] = int(floor(len(obj.index)/2))
    output = output.format(**x)
    
    x['date'] = most_recent_date.strftime("%m/%d/%Y")
    
    log.debug(obj)
    obj.to_csv(output,index = False, header=True, sep=',')
    return obj, x, output

def business_logic_summary(obj,summary) :
    ret = obj[obj['Player'] == 'Totals'] 
    ret = ret[['team', 'date','link']]
    ret['opponent']=ret.groupby('link')['team'].shift(-1)
    ret.dropna(inplace=True)
    ret['DD'] = PD.to_datetime(ret['date'])
    ret['vs'] = ret.agg('{0[team]} vs {0[opponent]}'.format, axis=1)
    ret.sort_values(by='DD',ascending=False, inplace=True)
    ret = ret[['date','vs','link']]
    ret.to_csv(summary,index = False, header=True, sep=',')
    log.info(ret)
    #ret['vs'] = ret.agg('{0[vs]} {0[link]}'.format, axis=1)
    ret = ret[['date','vs']]
    return ret, summary

def main(**args) :
    sport = args.get('sport',None)
    filename = args.get('filename',None)
    output_name = args.get('output',None)
    summary_name = args.get('summary',None)

    TEAMS.main(sport,filename)
    obj = SCORES.main(filename)
    summary, summary_name = business_logic_summary(obj,summary_name)
    games, x, output_name = business_logic(obj, sport, output_name)
    x['summary'] = summary.to_string(index=False)
    # date_format = '%Y-%m-%d'
    for client in client_list :
        client.update(x)

    server = EMAIL.gmail(user=CUSTOM._from,pswd=CUSTOM.pswd)
    for _from, _to, subject, msg in CLIENTS.transform(CUSTOM._from,CUSTOM.subject,CUSTOM.body,*client_list):
        obj = EMAIL.add_attachments(msg,*[output_name,summary_name])
        obj['From'] = _from
        obj['To'] = _to
        obj['Subject'] = subject
        server.sendmail(_from, _to, obj.as_string())
    server.quit()

if __name__ == "__main__":
    import sys
    import argparse

    log_file = COMMON.build_args(*sys.argv).replace('.py','') + '.log'
    log.basicConfig(filename=log_file, format=COMMON.LOG_FORMAT_TEST, level=log.DEBUG)
    
    # Create the parser and add arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--sport',required=True, dest='sport', help=HELP)
    
    # Parse and print the results
    args = parser.parse_args()
    try :
        obj, filename, output_name, summary_name = prep(**vars(args))
        main(sport=obj,filename=filename, output=output_name,summary=summary_name)
    except Exception as e:
        import traceback, sys
        log.error('Error at %s', 'module', exc_info=e)
        msg = '\n'.join(traceback.format_stack())
        log.info(msg)
        #server = EMAIL.gmail(user=CUSTOM._from,pswd=CUSTOM.pswd)
        #server.sendmail(CUSTOM._from, CUSTOM._from, msg)
        
        