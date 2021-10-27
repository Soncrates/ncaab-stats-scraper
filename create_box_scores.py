#!/usr/bin/python
##############################################################
# Program name: NCAA Stats Scraper (Team Mappings Module)
# Version: 1.0
##############################################################
from glob import glob
from scraperfunctions import grabber as POST
from scrapersettings import SportExtract as BASE
from bs4 import BeautifulSoup

def step01_read_team_list(filename):
    with open(filename, "rb") as f :
         team_map = f.readlines()[1:]
         return { name : url for name, url in v[0],v[1] for v in vars.split("\t") for vars in team_map }
def step02_extract_team_data(**team_list):
    for name, url in team_list.items() :
        yield name, POST(url, BASE.params, BASE.headers)
def step02_parse_response_for_box_scores(team_response) :
    link_list = BeautifulSoup(teamlist_response).find_all('a')
    return [ step02_transform(link) for link in link_list if step02_test(link) ]
def step02_test(link) :
    return link.get('href').endswith('box_score')
def step02_transform(link) :
    return str(BASE.base_url  + link.get('href'))
def step03_extract_box_scores_by_team(soup_table) :
    table_body = soup_table.find('tbody')
    team_name = table_body.find('tr', attrs={'class':'heading'}).find('td').text.strip()
    column_list = [ col.text.strip() for col in table_body.find_all('tr', attrs={'class':'grey_heading'})[-1].find_all('th') ]
    row_list = [ ele.text.strip() for ele in cols for cols in row.find_all('td') for row in table_body.find_all('tr', attrs={'class':'smtext'})]
    return team_name, column_list, row_list
def step03_extract_box_scores(url) :
    response = POST(url, BASE.params, BASE.headers)
    soap = BeautifulSoup(response)
    return soup.find_all('table', attrs={'class':'mytable'})
def by_sport(filename) :
    team_list = step01_read_team_list(filename)
    box_scores = { name : step02_parse_response_for_box_scores(response) in name, response in step02_extract_team_data(**team_list) }
    box_score_list = list(set(box_scores.values()))
    box_score_list = [ step03_extract_box_scores_by_team(table) for table in table_list for table_list in step03_extract_box_scores(url) for url in box_score_list ]
        
def main() :
    for sport in glob("*csv") :
         by_sport(sport) :
if __name__ == "__main__" :
   main()
