import re
import util
import bs4
import queue
import json
import sys
import csv
import sqlite3


def make_database():
    conn = sqlite3.connect("statistics.db")
    c = conn.cursor()
    #c.execute('''CREATE TABLE games
                 #(game_id, date, team1, team2, winner, team1_runs, team2_runs, team1_hits, team2_hits, team1_hr, team2_hr)''')
    
    c.execute('''CREATE TABLE player_employment
                 (player_id VARCHAR, teams VARCHAR, years VARCHAR)''')
    #cur.execute('CREATE TABLE IF NOT EXISTS mytable (field2 VARCHAR, field4 VARCHAR)')
    reader = csv.reader(open("player_employment_table.txt", "r"))
    for player_id, teams, years in reader:
        c.execute('INSERT INTO player_employment (player_id, teams, years) VALUES (?,?,?)', (player_id, teams, years))



    #with open('player_employment_table.csv','rb') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
        #dr = csv.DictReader(fin, fieldnames = ["player_id", "teams", "years"]) # comma is default delimiter
        #for i in dr:
            #print(i['player_id'])

        #to_db = [(i['player_id'], i['teams'], i['years']) for i in dr]

    #cur.executemany("INSERT INTO t (player_id, teams, years) VALUES (?, ?, ?);", to_db)
    conn.commit()
    

    #c.execute('''CREATE TABLE player_bios
                 #(player_id, position, player_name, playoffs, won_ws, years_played, span)''')
    #c.execute('''CREATE TABLE stats_nonpitcher 
                 #(player_id, season, WAR, UBR, AVG, OBP, SLG, WRC+, WPA, clutch)''')
    #c.execute('''CREATE TABLE stats_pitcher
                 #(player_id, season, WAR, ERA, IP, GS, K%, BB%, FIP, E-F, FIP-)''')
    #conn.commit()
    conn.close()

def url_check(url, parent_url):
    '''
    Takes a url, the limiting domain, and its parent url, and does various checks on the url, 
    returning the url in the correct format if it is ok to use and returning None if not.
    '''

    if not util.is_absolute_url(url):
        url = util.convert_if_relative_url(parent_url, url)
    url = util.remove_fragment(url)
    if url:
        return url
    else:
        return None

   


def go_player_employment():
    '''
    Creates a dictionary with all the data from baseball-reference for the players and converts
    that into a csv file called player_employment_table.csv
    '''
    br_player_dict = make_br_player_dict()
    make_player_employment_csv_file(br_player_dict, "player_employment_table.csv")
    
def make_player_employment_csv_file(data_dict, filename):
    '''
    Makes a csv file for the player_employment table info from a dictionary
    '''
    with open(filename, 'w') as csvfile:
        indexwriter = csv.writer(csvfile)
        for player_id in data_dict.keys():
            indexwriter.writerow([player_id, data_dict[player_id]["teams"], data_dict[player_id]["years"]])   

#FOR THE GAMES TABLE (ALL FROM BASEBALL REFERENCE)
def make_br_games_dict():
    master_game_dict = {}
    master_regular_game_dict = {}

    urls_visited = []
    starting_url = "http://www.baseball-reference.com/boxes/"
    parent_url = "http://www.baseball-reference.com"
    if starting_url not in urls_visited:
        urls_visited.append(starting_url)
        request = util.get_request(starting_url)
        #print("request:", request)
        if request:
            text = request.text
            soup = bs4.BeautifulSoup(text, parse_only=bs4.SoupStrainer("table", class_="large_text"))
            regular_season_year_urls = get_regular_season_year_urls(soup, urls_visited)
            master_regular_game_dict = get_day_urls(regular_season_year_urls, urls_visited, parent_url, master_regular_game_dict)
            #master_ps_game_dict = get_post_season_urls(soup, urls_visited, parent_url)
    return master_game_dict

def get_post_season_urls(soup, urls_visited, parent_url):
    #need to get all urls for all the world series/postseason stuff until it gets to 1903, when I 
    #should stop getting data bc there is barely any data
    ps_link = soup.find("a", href="/postseason/")
    ps_url = ps_link.get("href")
    if ps_url not in urls_visited:
        urls_visited.append(ps_url)
        abs_ps_url = url_check(ps_url, parent_url)
        if abs_ps_url:
            parent_url = abs_ps_url
            ps_request = util.get_request(abs_ps_url)
            if ps_request:
                ps_text = ps_request.text
                ps_soup1 = bs4.BeautifulSoup(ps_text, parse_only=bs4.SoupStrainer("table", class_="stats_table nav_table"))
                table_rows = ps_soup1.find_all("tr")
                #print("table_rows", table_rows)
                for row in table_rows:
                    possible_links = row.find_all("a", href=True)
                    #print("possible links", possible_links)
                    print("len possible_links", len(possible_links))
                    if len(possible_links) > 3:
                        series_urls = [possible_links[0].get("href"), possible_links[len(possible_links)//2].get("href")]
                    elif len(possible_links) > 0:
                        series_urls = [possible_links[0].get("href")]
                    for series_url in series_urls:
                        master_ps_game_dict = get_ps_game_info(series_url, urls_visited, parent_url)

                    
                ps_soup2 = bs4.BeautifulSoup(text, parse_only=bs4.SoupStrainer("table", class_="stats_table"))

def get_ps_game_info(series_url, urls_visited, parent_url):
    if series_url not in urls_visited:
        urls_visited.append(series_url)
        abs_series_url = url_check(series_url, parent_url)
        if abs_series_url:
            series_request = util.get_request(abs_series_url)
            if series_request:
                series_text = series_request.text
                series_soup = bs4.BeautifulSoup(series_text, parse_only=bs4.SoupStrainer("pre"))
                games = series_soup.find_all("pre")
                print("games", games)
                #for game in games:
                    #date = 

                


def get_regular_season_year_urls(soup, urls_visited):
    regular_season_year_urls = []
    possible_urls = soup.find_all("a", href=True)
    for url in possible_urls:
        if len(url.text) <= 2 and url not in urls_visited:
            urls_visited.append(url)
            regular_season_year_urls.append(url.get("href"))
    #print("regular_season_year_urls:", regular_season_year_urls)
    return regular_season_year_urls

def get_day_urls(regular_season_year_urls, urls_visited, parent_url, master_regular_game_dict):
    parent_url = "www.baseball-reference.com/boxes/"
    for year_url in regular_season_year_urls:
        if year_url not in urls_visited:
            urls_visited.append(year_url)
            abs_year_url = url_check(year_url, parent_url)
            print("if abs_year_url", abs_year_url)
            if abs_year_url:
                year_request = util.get_request(abs_year_url)
                if year_request:
                    year_text = year_request.text
                    year_soup = bs4.BeautifulSoup(year_text, parse_only=bs4.SoupStrainer("table", class_="wide_container"))
                    #print("year soup", year_soup)
                    day_urls = [a.attrs.get("href") for a in year_soup.select("a")]
                    day_links = year_soup.find("a")
                    print("day urls:", day_urls)
                    print("day links", day_links)
                    #idk why it can't find "a" bc it's there this is so annoying 
                    #parent_url = abs_year_url
                    master_regular_game_dict = get_game_urls(master_regular_game_dict, day_urls, urls_visited)
    return master_regular_game_dict

def get_game_urls(master_regular_game_dict, day_urls, urls_visited):
    game_id = 0
    parent_url = "www.baseball-reference.com"
    for day_url in day_urls:
        if day_url not in urls_visited:
            urls_visited.append(day_url)
            abs_day_url = url_check(day_url, parent_url)
            if abs_day_url:
                #print("abs_day_url", abs_day_url)
                day_request = util.get_request(abs_day_url)
                if day_request:
                    day_text = day_request.text
                    day_soup = bs4.BeautifulSoup(day_text, parse_only=bs4.SoupStrainer("pre"))
                    possible_links = day_soup.find_all("a")
                    #print("possible_links", possible_links)
                    #game_url = possible_urls[0].get("href")
                    game_urls = []
                    for link in possible_links:
                        if re.search('[a-zA-Z]', link.text) == None:
                            game_urls.append(link.get("href"))
                    num_games = len(game_urls)
                    #print("game_urls", game_urls)
                    for game_url in game_urls:
                        game_dict = get_game_info(game_url, parent_url, urls_visited, num_games)
                        game_id += 1
                        master_regular_game_dict[game_id] = game_dict
    return master_regular_game_dict

def get_game_info(game_url, parent_url, urls_visited, num_games):
    game_dict = {"date": "", "stadium": "", "team1": "", "team2": "", "team1_runs": "", "team2_runs": "", "team1_hits": "", "team2_hits": "", "team1_hr": "", "team2_hr": "", "winner": ""}
    if game_url not in urls_visited:
        urls_visited.append(game_url)
        #print('parent_url', parent_url)
        #print('game url', game_url)
        abs_game_url = url_check(game_url, parent_url)
        if abs_game_url:
            print("abs_game_url", abs_game_url)
            game_request = util.get_request(abs_game_url)
            if game_request:
                game_text = game_request.text
                game_soup = bs4.BeautifulSoup(game_text, parse_only=bs4.SoupStrainer("div", id="page_content"))
                all_tables = game_soup.find_all("table", class_=False)
                game_table = all_tables[num_games]
                game_table_rows = game_table.find_all("tr")
                date_and_stadium_table = game_table_rows[0]
                date_and_stadium = date_and_stadium_table.find_all("div", class_="bold_text float_left")
                date = date_and_stadium[0].text
                stadium = date_and_stadium[1].text
                hits_runs_and_teams_table = game_table_rows[3]
                teams = hits_runs_and_teams_table.find_all("a", href=True)
                team1 = teams[0].text
                team2 = teams[1].text
                game_data = hits_runs_and_teams_table.find_all("strong")
                team1_runs = game_data[2].text[4]
                team2_runs = game_data[4].text[4]
                team1_hits = game_data[2].text[7]
                team2_hits = game_data[4].text[7]
                team1_hr_table = all_tables[num_games+5]
                team1_hr_row = team1_hr_table.find("tfoot")
                team1_hr = team1_hr_row.find_all("td")[7]
                team2_hr_table = all_tables[num_games+4]
                team2_hr_row = team2_hr_table.find("tfoot")
                team2_hr = team2_hr_row.find_all("td")[7]
                if int(team1_runs) > int(team2_runs):
                    winner = team1
                elif int(team2_runs) > int(team1_runs):
                    winner = team2
                else:
                    winner = "tie"
                game_dict["date"] = date
                game_dict["stadium"] = stadium[2:]
                game_dict["team1"] = team1
                game_dict["team2"] = team2
                game_dict["team1_runs"] = team1_runs
                game_dict["team2_runs"] = team2_runs
                game_dict["team1_hits"] = team1_hits
                game_dict["team2_hits"] = team2_hits
                game_dict["team1_hr"] = team1_hr
                game_dict["team2_hr"] = team2_hr
                game_dict["winner"] = winner
    print("game dict", game_dict)
    return game_dict



#ALL FROM BASEBALL REFERENCE PLAYERS SECTION 
#all of the player_employment table
#postion, name, years, span, player_id for player_bios table
#WAR, season/year, player_id for stats_nonpitcher table
#WAR, ERA, FIP, IP, GS, E-F, season/year, player_id for stats_pitcher table


def make_br_player_dict():
    '''
    Crawls through the players part of baseball-reference and makes a dictionary where the keys are 
    the player_id for each player, which map to the teams each player played for and the corresponding 
    year for each team
    '''
    master_player_dict = {}
    
    letter_urls = []
    player_urls = []
    urls_visited = []
    starting_url = "http://www.baseball-reference.com/players/"
    parent_url = starting_url
    if starting_url not in urls_visited:
        urls_visited.append(starting_url)
        request = util.get_request(starting_url)
        if request:
            text = request.text
            soup = bs4.BeautifulSoup(text, parse_only=bs4.SoupStrainer("td", class_="xx_large_text bold_text"))
            letter_urls = [a.attrs.get("href") for a in soup.select("a")]#makes list of letter urls
            #print("letter urls:", letter_urls)
            master_player_dict = get_player_urls(letter_urls, urls_visited, parent_url, master_player_dict)
        
    return master_player_dict


def get_player_urls(letter_urls, urls_visited, parent_url, master_player_dict):
    '''
    Loops through the the list of letter urls and gets a list of player urls, which it passes down to
    create_players so that the info for each player can be made into a mini dictionary that can be
    added to the master dictionary
    '''
    
    for letter_url in letter_urls:
        if letter_url not in urls_visited:
            urls_visited.append(letter_url)
            abs_letter_url = url_check(letter_url, parent_url)
            if abs_letter_url:
                letter_request = util.get_request(abs_letter_url)
                if letter_request:
                    letter_text = letter_request.text
                    letter_soup = bs4.BeautifulSoup(letter_text, parse_only=bs4.SoupStrainer("pre"))
                    #players = letter_soup.find_all("a",href=True)
                    player_urls = [a.attrs.get("href") for a in letter_soup.select("a")] #makes list of player urls
                    #print("player_urls:", player_urls)
                    parent_url = abs_letter_url
                    master_player_dict = create_players(master_player_dict, player_urls, parent_url, urls_visited)
    return master_player_dict
    

def create_players(master_player_dict, player_urls, parent_url, urls_visited):
    '''
    Loops through the list of player urls and passes the rows of the standard batting table
    down to get_player info so that function can get the team and year information
    '''
    id_number = 0
    for player_url in player_urls:
        if player_url not in urls_visited:
            #print("player_url:", player_url)
            player_dict = {"name": "", "positions": "", "years": "", "span": "", "years_played": "", "teams": "", "WARs_nonpitcher": "", "WARs_pitcher": "", "ERAs": "", "IPs": "", "GSs": "", "FIPs": "", "E_Fs": ""}
            urls_visited.append(player_url)
            abs_player_url = url_check(player_url, parent_url)
            if abs_player_url:
                player_request = util.get_request(abs_player_url)
                if player_request:
                    player_text = player_request.text
                    #all the things to put in the player_employment_dict
                    years = get_player_info_from_standard_batting(player_text)[0]
                    teams = get_player_info_from_standard_batting(player_text)[1]
                    player_name = get_player_info_from_main_player_page(player_text)[0]
                    positions = get_player_info_from_main_player_page(player_text)[1]
                    #put them in the player_employment_dict
                    player_dict["years"] = years
                    player_dict["teams"] = teams
                    player_dict["name"] = player_name
                    player_dict["positions"] = positions

                    if "Pitcher" in positions:
                        eras = get_player_info_from_standard_pitching(player_text)[0]
                        ips = get_player_info_from_standard_pitching(player_text)[1]
                        gss = get_player_info_from_standard_pitching(player_text)[2]
                        fips = get_player_info_from_standard_pitching(player_text)[3]
                        e_fs = get_player_info_from_standard_pitching(player_text)[4]
                        wars_pitcher = get_player_info_from_player_value_pitchers(player_text)
                        player_dict["ERAs"] = eras
                        player_dict["IPs"] = ips
                        player_dict["GSs"] = gss
                        player_dict["FIPs"] = fips
                        player_dict["E_Fs"] = e_fs
                        player_dict["WARs_pitcher"] = wars_pitcher 
                    #else:should this be an else or should there always be nonpitcher stats?
                    wars_nonpitcher = get_player_info_from_player_value_batters(player_text)
                    player_dict["WARs_nonpitcher"] = wars_nonpitcher 
            if player_dict["years"] != "":
                player_dict["span"] = "-".join([player_dict["years"][:4], player_dict["years"][len(player_dict["years"])-4:]])
                player_dict["years_played"] = int(player_dict["years"][len(player_dict["years"])-4:]) - int(player_dict["years"][:4])
            #print("id number:", id_number)
            #print("player dict:", player_dict)
            master_player_dict[id_number] = player_dict
            id_number += 1
    return master_player_dict

def get_player_info_from_standard_batting(player_text):
    '''
    Takes the text for a player's webpage and gets a string that contains every team
    that a certain player has played for as well as the corresponding year for each team from
    the standard batting table for that player.
    '''
    player_soup = bs4.BeautifulSoup(player_text, parse_only=bs4.SoupStrainer("table", id="batting_standard")) 
    rows = player_soup.find_all("tr", {"class" : ["full" , "partial_table"]})
    years = ""
    teams = ""
    for row in rows:
        year = None
        team = None
        valid_year = re.compile("^[12][0-9]{3}(?:\.\d{0,2})?$")
        team_str = re.compile("teams", re.IGNORECASE)
        year_ck = row.find("td",{"csk": valid_year})
        if year_ck:
            year = year_ck.get("csk")[:4]
        team_ck = row.find("a", {"href" : team_str, "title" : True})
        if team_ck:
            team = team_ck.get("title")
        if year and team:
            if years != "":
                updated_teams = "|".join([teams, team])
                updated_years = "|".join([years, year])
            else:
                updated_teams = team
                updated_years = year
            years = updated_years
            teams = updated_teams
        
    return years, teams
    

def get_player_info_from_standard_pitching(player_text):
    '''
    Takes the text for a player's webpage and returns strings for the ERAs, IPs, GSs, FIPs, and E_Fs
    for that player from the standad pitching table.
    '''
    player_soup = bs4.BeautifulSoup(player_text, parse_only=bs4.SoupStrainer("table", id="pitching_standard")) 
    rows = player_soup.find_all("tr", class_="full")
    ERAs = ""
    IPs = ""
    GSs = ""
    FIPs = ""
    E_Fs = ""
    for row in rows:
        era = None
        ip = None
        gs = None
        fip = None
        row_values = row.find_all("td")
        era = row_values[7].text
        ip = row_values[14].text
        gs = row_values[9].text
        fip = row_values[27].text
        if era and era != "" and ip and ip != "" and gs and gs != "" and fip and fip != "":
            e_f = str(float(era) - float(fip))
            ERAs = "|".join([ERAs, era])
            IPs = "|".join([IPs, ip])
            GSs = "|".join([GSs, gs])
            FIPs = "|".join([FIPs, fip])
            E_Fs = "|".join([E_Fs, e_f])
    
    return ERAs[1:], IPs[1:], GSs[1:], FIPs[1:], E_Fs[1:]

def get_player_info_from_main_player_page(player_text):
    '''
    Takes the text from the player's webpage and returns strings for the player's name and position(s)
    '''
    player_soup = bs4.BeautifulSoup(player_text, parse_only=bs4.SoupStrainer("div", id="info_box")) 
    player_name = player_soup.find("span", id="player_name").text
    positions_with_and = player_soup.find("span", itemprop="role").text
    positions_list = positions_with_and.split(" and ")
    positions = "|".join(positions_list) 

    return player_name, positions

def get_player_info_from_player_value_batters(player_text):
    '''
    Takes the text from the player's webpage and returns a string of the player's WARs if they 
    are not a pitcher
    '''
    war_soup = bs4.BeautifulSoup(player_text, parse_only=bs4.SoupStrainer("table", id="batting_value")) 
    wars = [td.text for td in war_soup.select('tr.full > td:nth-of-type(16)')]
    WARs_nonpitcher = "|".join(wars)
    return WARs_nonpitcher


def get_player_info_from_player_value_pitchers(player_text):
    '''
    Takes the text from the player's webpage and returns a string of the player's WARs if they
    are a pitcher
    '''
    war_soup = bs4.BeautifulSoup(player_text, parse_only=bs4.SoupStrainer("table", id="pitching_value")) 
    wars = [td.text for td in war_soup.select('tr.full > td:nth-of-type(16)')]
    WARs_pitcher = "|".join(wars)
    return WARs_pitcher
