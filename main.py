from copy import deepcopy
import pandas as PD
import libCommon as COMMON
import logging as log
import scrapersettings as SPORT
import create_team_mappings as TEAMS
import create_box_scores as SCORES

HELP = "1) Football, 2) Basketball, 3) Soccer, 4) Lacrosse"

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
    x['year'] = int(args.get('year',2021))
    log.debug(x)
    
    filename =  "output_team_list_{sport_code}_{year}.csv".format(**x)
    output = 'output_team_scores_{sport_code}_{year}.csv'.format(**x)
    log.info(filename)
    log.info(output)
    return sport, filename, output

def main(**args) :
    sport = args.get('sport',None)
    filename = args.get('filename',None)
    output = args.get('output',None)
    TEAMS.main(sport,filename)
    obj = SCORES.main(filename)
    log.debug(obj)
    obj = obj[obj['Player'] == 'Totals'] 
    obj.drop(['Player', 'Pos'], axis=1, inplace=True)
    obj['date'] = PD.to_datetime(obj['date']).dt.normalize()
    most_recent_date = obj['date'].max()
    obj = obj[obj['date'] == most_recent_date] 
    #obj=obj.reindex(columns= ['Rounded_score', 'Gender', 'Score','Name'])

    log.debug(obj)
    obj.to_csv(output,index = False, header=True, sep=',')
    # date_format = '%Y-%m-%d'    

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
        obj, filename, output = prep(**vars(args))
        main(sport=obj,filename=filename, output=output)
    except Exception as e:
        log.error('Error at %s', 'module', exc_info=e)
        