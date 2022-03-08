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

HELP = "1) Football, 2) Basketball, 3) Soccer, 4) Lacrosse"

most_recent_date = '1970_01_01'
client_list =  [{"user_email" : "shiegel@laescrow.netx","first_name":"Steve","last_name":"Hiegel", "user_login":"Steve"},
                {"user_email" : "chriswithteal@gmail.com","first_name":"Martiel", "last_name":"and Staff", "user_login" : "Chris and Teal"}]
client_list =  [
                {"user_email" : "chriswithteal@gmail.com","first_name":"Martiel", "last_name":"and Staff", "user_login" : "Chris and Teal"}]


class CUSTOM:
    _from = "emersoncus@gmail.com"
    pswd = "qhxbqkhdvzsbaxjk"
    subject="Team Scores, {date} for {user_login}"
    body ="""
Hi {first_name} {last_name}

You are receiving this email as a test of our new automated system of ncaab score scraper.

These were the last recorded {sport_code} games on {date}
There were {count} {sport_code} games played.



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
    log.info(filename)
    log.info(output)
    return sport, filename, output

def business_logic(obj, sport, output) :
    log.debug(obj)
    obj = obj[obj['Player'] == 'Totals'] 
    obj.drop(['Player', 'Pos'], axis=1, inplace=True)
    obj['date'] = PD.to_datetime(obj['date']).dt.normalize()
    most_recent_date = obj['date'].max()
    obj = obj[obj['date'] == most_recent_date] 
    #obj=obj.reindex(columns= ['Rounded_score', 'Gender', 'Score','Name'])

    x = deepcopy(sport.default_params[0])
    x['date'] = most_recent_date.strftime("%Y_%m_%d")
    x['count'] = int(floor(len(obj.index)/2))
    output = output.format(**x)
    
    log.debug(obj)
    return obj, x, output

def main(**args) :
    sport = args.get('sport',None)
    filename = args.get('filename',None)
    TEAMS.main(sport,filename)
    obj = SCORES.main(filename)
    output = args.get('output',None)
    obj, x, output = business_logic(obj, sport, output)
    obj.to_csv(output,index = False, header=True, sep=',')
    # date_format = '%Y-%m-%d'
    for client in client_list :
        client.update(x)

    server = EMAIL.gmail(user=CUSTOM._from,pswd=CUSTOM.pswd)
    for _from, _to, subject, msg in CLIENTS.transform(CUSTOM._from,CUSTOM.subject,CUSTOM.body,*client_list):
        obj = EMAIL.add_attachments(msg,*[output])
        obj['From'] = _from
        obj['To'] = _to
        obj['Subject'] = subject
        server.sendmail(_from, _to, obj.as_string())
    server.quit()

if __name__ == "__main__":
    import sys
    import argparse

    log_file = COMMON.build_args(*sys.argv).replace('.py','') + '.log'
    log.basicConfig(filename=log_file, format=COMMON.LOG_FORMAT_TEST, level=log.INFO)
    
    # Create the parser and add arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--sport',required=True, dest='sport', help=HELP)
    
    # Parse and print the results
    args = parser.parse_args()
    try :
        obj, filename, output = prep(**vars(args))
        main(sport=obj,filename=filename, output=output)
    except Exception as e:
        import traceback, sys
        log.error('Error at %s', 'module', exc_info=e)
        msg = '\n'.join(traceback.format_stack())
        log.info(msg)
        #server = EMAIL.gmail(user=CUSTOM._from,pswd=CUSTOM.pswd)
        #server.sendmail(CUSTOM._from, CUSTOM._from, msg)
        
        