#!/usr/bin/python
##############################################################
# Program name: NCAA Stats Scraper (Team Mappings Module)
# Version: 1.0
##############################################################
from scraperfunctions import grabber as EXTRACT
from scrapersettings import SportExtract as BASE
from bs4 import BeautifulSoup as TRANSFORM
import pandas as PY

def step01_read_team_list(filename):
    with open(filename, "rb") as f :
         team_list = f.readlines()[1:]
         team_list = [ team.split("\t") for team in team_list ]
         return { var[0] : var[1] for var in team_list }
def step02_extract_team_data(*team_list):
    return [ EXTRACT(url, BASE.params, BASE.headers) for url in team_list ]
def step02_parse_response_for_box_scores(response) :
    table = TRANSFORM(response,features="html.parser").find('tbody')
    row_list = table.findAll('tr')
    td_list = [ row.findAll('td') for row in row_list ]
    td_list = extract_table_rows(td_list)
    date_list = [ ele[0] for ele in td_list if len(ele) > 1]
    print(date_list)
    link_list = table.findAll('a')
    link_list = [row.findAll('a') for row in row_list]
    print(link_list)
    link_list = [ step02_transform(link) for link in link_list if step02_test(link) ]
    return dict(zip(link_list,date_list))
def step02_test(link) :
    return link.get('href').endswith('box_score')
def step02_transform(link) :
    return str(BASE.base_url  + link.get('href'))
def step03_transform_box_scores(response) :
    soup = TRANSFORM(response,features="html.parser")
    table_list = soup.findAll('table', attrs={'class':'mytable'})
    return [ step03_transform_table(table) for table in table_list if step03_test(table) ]
def step03_test(table) :
    tr_list = table.findAll('tr', attrs={'class':'grey_heading'})
    td_list = [ tr.findAll('td') for tr in tr_list ]
    td_list = flatten_table_rows(td_list)
    td_list = [ td for td in td_list if td in ['1st Quarter', '2nd Quarter', '3rd Quarter', '4th Quarter'] ]
    if len(td_list) > 0 :
        return False
    return True
def step03_transform_table(soup_table) :
    team_name = soup_table.find('tr', attrs={'class':'heading'}).find('td').text.strip()
    grey_header_list = soup_table.findAll('tr', attrs={'class':'grey_heading'})
    column_list = [ col.text.strip() for col in grey_header_list[0].findAll('th') ]

    row_list = soup_table.findAll('tr', attrs={'class':'smtext'})
    td_list = [ tr.findAll('td') for tr in row_list ]
    row_list = extract_table_rows(td_list)

    total = grey_header_list[-1]
    td_list = total.findAll('td')
    total = extract_table_rows(td_list)
    row_list.extend(total)
    
    ret = PY.DataFrame(row_list,columns=column_list)
    return { team_name : ret }
def extract_table_rows(tr_list) :    
    ret = []
    for td_list in tr_list :
        ret.append([ ele.text.strip() for ele in td_list ])
    return ret
def flatten_table_rows(tr_list) :    
    ret = []
    for td_list in tr_list :
        ret.extend([ ele.text.strip() for ele in td_list ])
    return ret
def by_sport(filename) :
    team_url_list = step01_read_team_list(filename).values()
    box_scores = [ step02_parse_response_for_box_scores(response) for response in step02_extract_team_data(*team_url_list) ]
    box_score_list = [ step03_extract_box_scores_by_team(table) for table in table_list for table_list in step03_extract_box_scores(url) for url in list(set(box_scores)) ]
        
def main(*sport_list) :
    ret  = [ by_sport(sport) for sport in sport_list]
if __name__ == "__main__" :
   sport_list = COMMON.find_files("team_list*csv")
   main(*sport_list)
