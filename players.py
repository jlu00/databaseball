import requests
import bs4
import re
import queue
import json
import sys
import csv
from datetime import datetime


start=datetime.now().time()


import requests
import bs4
import re
import queue
import json
import sys
import csv


#functions that make the csv files for each table from the dictionary of all data
def make_player_employment_csv_file(data_dict, filename):
    '''
    Makes a csv file for the player_employment table info from a dictionary
    '''
    strfilename = "%s.csv" % (filename)
    with open(strfilename, 'w') as csvfile:
        indexwriter = csv.writer(csvfile)
        indexwriter.writerow(["player_id","teams","years"])
        for player_id in data_dict.keys():
            indexwriter.writerow([player_id, data_dict[player_id]["teams"], data_dict[player_id]["years"]])

def make_player_bio_csv_file(data_dict, filename):
    '''
    Makes a csv file for the player_bio table info from a dictionary
    '''
    strfilename = "%s_bios.csv" % (filename)
    with open(strfilename, 'w') as csvfile:
        indexwriter = csv.writer(csvfile)
        indexwriter.writerow(["player_id","positions","name","Playoffs","Playoffs_Won","World_Series","World_Series_Won","years_played","span"])
        for player_id in data_dict.keys():
            indexwriter.writerow([player_id, data_dict[player_id]["positions"], data_dict[player_id]["name"],data_dict[player_id]["Playoffs"],
data_dict[player_id]["Playoffs_Won"], data_dict[player_id]["World_Series"], data_dict[player_id]["World_Series_Won"], data_dict[player_id]["years_played"],
data_dict[player_id]["span"]])

def make_player_stats_nonpitcher_csv_file(data_dict, filename):
    '''
    Makes a csv file for the player_stats_nonpitcher table info from a dictionary
    '''
    strfilename = "%s_stats_nonpitcher.csv" % (filename)
    with open(strfilename, 'w') as csvfile:
        indexwriter = csv.writer(csvfile)
        indexwriter.writerow(["player_id","years","WARS_nonpitcher", "AVGs", "OBPs", "SLGs", "UBR_WRC_Years", "UBRs", "WRCs", "WPA_Years", "WPAs", "Clutchs"])
        for player_id in data_dict.keys():
            indexwriter.writerow([player_id, data_dict[player_id]["years"], data_dict[player_id]["WARs_nonpitcher"],
data_dict[player_id]["AVGs"],data_dict[player_id]["OBPs"], data_dict[player_id]["SLGs"], data_dict[player_id]["UBR_WRC_Years"], 
data_dict[player_id]["UBRs"],data_dict[player_id]["WRCs"], data_dict[player_id]["WPA_Years"], 
data_dict[player_id]["WPAs"],data_dict[player_id]["Clutchs"]])

def make_player_stats_pitcher_csv_file(data_dict, filename):
    '''
    Makes a csv file for the player_stats_pitcher table info from a dictionary
    '''
    strfilename = "%s_stats_pitcher.csv" % (filename)
    print("start stats pitcher csv",datetime.now().time())
    with open(strfilename, 'w') as csvfile:
        indexwriter = csv.writer(csvfile)
        indexwriter.writerow(["player_id","Pitcher_Years", "WARS_pitcher", "ERAs", "IPs", "GSs", "FIPs", "E_Fs", "K_Pers", "BB_Pers"])
        for player_id in data_dict.keys():
            indexwriter.writerow([player_id, data_dict[player_id]["Pitcher_Years"], data_dict[player_id]["WARs_pitcher"],
data_dict[player_id]["ERAs"],data_dict[player_id]["IPs"], data_dict[player_id]["GSs"], data_dict[player_id]["FIPs"], 
data_dict[player_id]["E_Fs"],data_dict[player_id]["K_Pers"], data_dict[player_id]["BB_Pers"]])
    print("finish stats pitcher csv",datetime.now().time())

def make_player_full_csv_file(data_dict, filename):
    '''
    Makes a csv file for the player from a dictionary
    '''
    strfilename = "%s_player_full.csv" % (filename)
    with open(strfilename, 'w') as csvfile:
        indexwriter = csv.writer(csvfile)
        indexwriter.writerow(["player_id","teams","years","positions","name","Playoffs","Playoffs_Won","World_Series","World_Series_Won","years_played",
"span", "years","WARS_nonpitcher", "AVGs", "OBPs", "SLGs", "UBR_WRC_Years", "UBRs", "WRCs", "WPA_Years", "WPAs", "Clutchs",
"Pitcher_Years", "WARS_pitcher", "ERAs", "IPs", "GSs", "FIPs", "E_Fs", "K_Pers", "BB_Pers"])
        for player_id in data_dict.keys():
            indexwriter.writerow([player_id, data_dict[player_id]["teams"], data_dict[player_id]["years"], data_dict[player_id]["positions"], data_dict[player_id]["name"],data_dict[player_id]["Playoffs"],
data_dict[player_id]["Playoffs_Won"], data_dict[player_id]["World_Series"], data_dict[player_id]["World_Series_Won"], data_dict[player_id]["years_played"],
data_dict[player_id]["span"], data_dict[player_id]["WARs_nonpitcher"],
data_dict[player_id]["AVGs"],data_dict[player_id]["OBPs"], data_dict[player_id]["SLGs"], data_dict[player_id]["UBR_WRC_Years"], 
data_dict[player_id]["UBRs"],data_dict[player_id]["WRCs"], data_dict[player_id]["WPA_Years"], 
data_dict[player_id]["WPAs"],data_dict[player_id]["Clutchs"], data_dict[player_id]["Pitcher_Years"], data_dict[player_id]["WARs_pitcher"],
data_dict[player_id]["ERAs"],data_dict[player_id]["IPs"], data_dict[player_id]["GSs"], data_dict[player_id]["FIPs"], 
data_dict[player_id]["E_Fs"],data_dict[player_id]["K_Pers"], data_dict[player_id]["BB_Pers"]])

#functions that scrape data from baseball-reference
def make_br_player_dict():
    '''
    Crawls through the players part of baseball-reference and makes a dictionary where the keys are
    the player_id for each player, which map to the teams each player played for and the corresponding
    year for each team
    '''
    master_player_dict = {}
    letter_urls = []
    player_urls = []
    starting_url = "http://www.baseball-reference.com/players/"
    parent_url = "http://www.baseball-reference.com"
    request = requests.get(starting_url)
    if request:
        text = request.text
        soup = bs4.BeautifulSoup(text, parse_only=bs4.SoupStrainer("td", class_="xx_large_text bold_text"))
        letter_urls = [a.attrs.get("href") for a in soup.select("a")]#makes list of letter urls
        player_urls = get_player_urls(letter_urls, parent_url)
        master_player_urls = player_urls
        master_player_dict = create_players(master_player_dict, player_urls, parent_url, master_player_urls)

    return master_player_dict


def make_br_alpha_player_dict(letter):
    '''
    Crawls through the players part of baseball-reference and makes a dictionary for players whose last 
    names start with letter, where the keys are the player_id for each player, which map to the teams each 
    player played for and the corresponding year for each team
    '''
    master_player_dict = {}
    player_urls = []
    letter_url = "%s%s/" % ("http://www.baseball-reference.com/players/",letter)
    parent_url = "http://www.baseball-reference.com"
    master_player_urls = get_master_player_urls(parent_url)
    player_urls = get_alpha_player_urls(letter_url)
    master_player_dict = create_players(master_player_dict, player_urls, parent_url, master_player_urls)

    return master_player_dict


def get_alpha_player_urls(letter_url):
    '''
    Gets a master list of player urls from the letter_url, which it passes down to
    create_players so that the player can be assigned the correct id_number
    '''
    player_urls = []
    abs_letter_url = letter_url
    letter_request = requests.get(abs_letter_url)
    if letter_request:
        letter_text = letter_request.text
        letter_soup = bs4.BeautifulSoup(letter_text, parse_only=bs4.SoupStrainer("pre"))
        player_urls = [a.attrs.get("href") for a in letter_soup.select("a")] #makes list of player urls
        player_names = [a.text for a in letter_soup.select("a")] #makes a list of player names unencoded

    print(letter_url, len(player_urls))
    return player_urls, player_names            

def get_master_player_urls(parent_url):
    '''
    Loops through the the list of letter urls and gets a master list of player urls, which it passes down to
    create_players so that the player can be assigned the correct id_number
    '''
    master_player_urls = []
    lookup_url = "%s/players/" % (parent_url)
    request = requests.get(lookup_url)
    if request:
        text = request.text
        soup = bs4.BeautifulSoup(text, parse_only=bs4.SoupStrainer("td", class_="xx_large_text bold_text"))    
        letter_urls = [a.attrs.get("href") for a in soup.select("a")]#makes list of letter urls

        for letter_url in letter_urls:
            abs_letter_url = "%s%s" % (parent_url, letter_url)
            letter_request = requests.get(abs_letter_url)
            if letter_request:
                letter_text = letter_request.text
                letter_soup = bs4.BeautifulSoup(letter_text, parse_only=bs4.SoupStrainer("pre"))
                master_player_urls += [a.attrs.get("href") for a in letter_soup.select("a")] #makes list of player urls

    return master_player_urls

def get_player_urls(letter_urls, parent_url):
    '''
    Loops through the the list of letter urls and gets a list of player urls, which it passes down to
    create_players so that the info for each player can be made into a mini dictionary that can be
    added to the master dictionary
    '''
    for letter_url in letter_urls:
        abs_letter_url = "%s%s" % (parent_url,letter_url)
        letter_request = requests.get(abs_letter_url)
        if letter_request:
            letter_text = letter_request.text
            letter_soup = bs4.BeautifulSoup(letter_text, parse_only=bs4.SoupStrainer("pre"))
            player_urls = [a.attrs.get("href") for a in letter_soup.select("a")] #makes list of player urls
            player_names = [a.text for a in letter_soup.select("a")] #makes a list of player names unencoded

    return player_urls, player_names


def create_players(master_player_dict, player_urls, parent_url, master_player_urls):
    '''
    Loops through the list of player urls and passes the retrieved page text to 
    related functions to parse the necessary player information to place into the dictionary
    '''
    name_index = 0
    for player_url in player_urls[0]:
        player_dict = {"name": "", "positions": "", "years": "", "span": "", "years_played": "", "teams": "", "WARs_nonpitcher": "",
 "WARs_pitcher": "", "ERAs": "", "IPs": "", "GSs": "", "FIPs": "", "E_Fs": "", "K_Pers" : "", "BB_Pers" : "",
 "Pitcher_Years" : "", "AVGs" : "", "OBPs" : "", "SLGs" : "", "Playoffs" : "", "Playoffs_Won" : "", "World_Series": "", "World_Series_Won" : "",
"UBR_WRC_Years" : "", "UBRs" : "", "WRCs" : "", "WPA_Years" : "", "WPAs" : "", "Clutchs" : ""}
        abs_player_url = "%s%s" % (parent_url,player_url)       
        player_request = requests.get(abs_player_url)
        if player_request:
            player_text = player_request.text
            id_number = master_player_urls.index(player_url)
            
            player_name = player_urls[1][name_index]
            name_index += 1

            #reset
            years = ""
            teams = ""
            years_played = ""
            year_span = ""

            #all the things to put in the player_employment_dict
            player_info = get_player_info_from_main_player_page(player_text)
            positions = player_info

            player_batting_info = get_player_info_from_standard_batting(player_text)
            player_pitching_info = get_player_info_from_standard_pitching(player_text)

            if player_batting_info:
                #not all pitchers bat
                years = player_batting_info[0]
                teams = player_batting_info[1]
                years_played = player_batting_info[2]
                year_span = player_batting_info[3]
                avgs = player_batting_info[4]
                obps = player_batting_info[5]
                slgs = player_batting_info[6]
                player_dict["AVGs"] = avgs
                player_dict["OBPs"] = obps
                player_dict["SLGs"] = slgs
                wars_nonpitcher = get_player_info_from_player_value_batters(player_text)
                player_dict["WARs_nonpitcher"] = wars_nonpitcher
                fangraph_stats = get_player_stats_from_fangraphs(player_name,year_span[4:])
                if fangraph_stats:
                    adv_years = fangraph_stats[0]
                    adv_ubrs = fangraph_stats[1]
                    adv_wrcs = fangraph_stats[2]
                    wpa_years = fangraph_stats[3]
                    wpa_wpas = fangraph_stats[4]
                    wpa_clutchs = fangraph_stats[5]
                    player_dict["UBR_WRC_Years"] = adv_years
                    player_dict["UBRs"] = adv_ubrs
                    player_dict["WRCs"] = adv_wrcs
                    player_dict["WPA_Years"] = wpa_years
                    player_dict["WPAs"] = wpa_wpas
                    player_dict["Clutchs"] = wpa_clutchs
            elif player_pitching_info:
                years = player_pitching_info[0]
                teams = player_pitching_info[1]
                years_played = player_pitching_info[2]
                year_span = player_pitching_info[3]
            #check all pitcher stats even if they have batting info             
            if "Pitcher" in positions:
                eras = player_pitching_info[4]
                ips = player_pitching_info[5]
                gss = player_pitching_info[6]
                fips = player_pitching_info[7]
                e_fs = player_pitching_info[8]
                k_pers = player_pitching_info[9]
                bb_pers = player_pitching_info[10]
                wars_pitcher = get_player_info_from_player_value_pitchers(player_text)
                player_dict["ERAs"] = eras
                player_dict["IPs"] = ips
                player_dict["GSs"] = gss
                player_dict["FIPs"] = fips
                player_dict["E_Fs"] = e_fs
                player_dict["K_Pers"] = k_pers
                player_dict["BB_Pers"] = bb_pers
                player_dict["WARs_pitcher"] = wars_pitcher
                player_dict["Pitcher_Years"] = player_pitching_info[0]

            #put values in the player_employment_dict
            player_dict["years"] = years
            player_dict["teams"] = teams
            player_dict["name"] = player_name
            player_dict["positions"] = positions 
            player_dict["span"] = year_span
            player_dict["years_played"] = years_played

            #collect postseason information, if available
            player_postseason_batting_info = get_player_info_from_postseason_batting(player_text)
            player_postseason_pitching_info = get_player_info_from_postseason_pitching(player_text)
            if player_postseason_batting_info:
                playoffs = player_postseason_batting_info[0]
                playoffs_won = player_postseason_batting_info[1]
                worldseries = player_postseason_batting_info[2]
                worldseries_won = player_postseason_batting_info[3]
                player_dict["Playoffs"] = playoffs
                player_dict["Playoffs_Won"] =playoffs_won
                player_dict["World_Series"] = worldseries
                player_dict["World_Series_Won"] = worldseries_won     
            elif player_postseason_pitching_info:
                playoffs = player_postseason_pitching_info[0]
                playoffs_won = player_postseason_pitching_info[1]
                worldseries = player_postseason_pitching_info[2]
                worldseries_won = player_postseason_pitching_info[3]
                player_dict["Playoffs"] = playoffs
                player_dict["Playoffs_Won"] =playoffs_won
                player_dict["World_Series"] = worldseries
                player_dict["World_Series_Won"] = worldseries_won

            master_player_dict[id_number] = player_dict

    return master_player_dict

def get_player_info_from_standard_batting(player_text):
    '''
    Takes the text for a player's webpage and gets a string that contains every team
    that a certain player has played for as well as the corresponding year for each team from
    the standard batting table for that player.
    '''
    player_soup = bs4.BeautifulSoup(player_text, parse_only=bs4.SoupStrainer("table", id="batting_standard")) 
    rows = player_soup.find_all("tr", {"class" : ["full" , "partial_table"]})
    if not rows: #if there are no values, there is no table
        return None
    years = ""
    teams = ""
    AVGs = ""
    OBPs = ""
    SLGs = ""
    valid_year = re.compile("^[12][0-9]{3}(?:\.\d{0,2})?$")
    team_str = re.compile("teams", re.IGNORECASE)
    for row in rows:
        year = None
        team = None
        year_ck = row.find("td",{"csk": valid_year})
        if year_ck:
            year = year_ck.get("csk")[:4]
        team_ck = row.find("a", {"href" : team_str, "title" : True})
        if team_ck:
            team = team_ck.get("title")
        if year and team:
            teams = "|".join([teams, team])
            years = "|".join([years, year])
            player_stats = get_player_batting_stats(row)
            AVGs = "|".join([AVGs,player_stats[0]])
            OBPs = "|".join([OBPs,player_stats[1]])
            SLGs = "|".join([SLGs,player_stats[2]])
            

    years_total_td = player_soup.find("tfoot").find("tr",{"class":"stat_total"}).find("td")
    years_total = ""
    if years_total_td:
        years_total = years_total_td.text[:-3].strip()
    year_span = ""
    if years != "":
        year_first = years[1:5]
        year_last = years[len(years)-4:]
        year_span = "-".join([year_first,year_last])
        
    return years[1:], teams[1:], years_total, year_span, AVGs[1:], OBPs[1:], SLGs[1:]

def get_player_info_from_standard_pitching(player_text):
    '''
    Takes the text for a player's webpage and gets a string that contains every team
    that a certain player has played for as well as the corresponding year for each team from
    the standard pitching table for that player.
    '''
    player_soup = bs4.BeautifulSoup(player_text, parse_only=bs4.SoupStrainer("table", id="pitching_standard")) 
    rows = player_soup.find_all("tr", {"class" : ["full" , "partial_table"]})
    if not rows: #if there are no values, there is no table
        return None
    years = ""
    teams = ""
    ERAs = ""
    IPs = ""
    GSs = ""
    FIPs = ""
    E_Fs = ""
    K_Pers = ""
    BB_Pers = ""
    valid_year = re.compile("^[12][0-9]{3}(?:\.\d{0,2})?$")
    team_str = re.compile("teams", re.IGNORECASE)
    for row in rows:
        year = None
        team = None
        year_ck = row.find("td",{"csk": valid_year})
        if year_ck:
            year = year_ck.get("csk")[:4]
        team_ck = row.find("a", {"href" : team_str, "title" : True})
        if team_ck:
            team = team_ck.get("title")
        if year and team:
            teams = "|".join([teams, team])
            years = "|".join([years, year])
            player_stats = get_player_pitching_stats(row)
            ERAs = "|".join([ERAs,player_stats[0]])
            IPs = "|".join([IPs,player_stats[1]])
            GSs = "|".join([GSs,player_stats[2]])
            FIPs = "|".join([FIPs,player_stats[3]])
            E_Fs = "|".join([E_Fs,player_stats[4]])
            K_Pers = "|".join([K_Pers,player_stats[5]])
            BB_Pers = "|".join([BB_Pers,player_stats[6]])
               
    years_total_td = player_soup.find("tfoot").find("tr",{"class":"stat_total"}).find("td")
    years_total = ""
    if years_total_td:
        years_total = years_total_td.text[:-3].strip()
    year_span = ""
    if years != "":
        year_first = years[1:5]
        year_last = years[len(years)-4:]
        year_span = "-".join([year_first,year_last])
        
    return years[1:], teams[1:], years_total, year_span, ERAs[1:], IPs[1:], GSs[1:], FIPs[1:], E_Fs[1:], K_Pers[1:], BB_Pers[1:]



def floatsub(a,b):
    try:
        return str(round(float(a) - float(b),3))
    except:
        return ""

def floatdiv(a,b):
    try:
        return str(round(float(a)/float(b),3))
    except:
        return ""

def get_player_pitching_stats(row):
    '''
    for that player from the standard pitching table.
    '''
    ERA = ""
    IP = ""
    GS = ""
    FIP = ""
    E_F = ""
    BB_Per = ""
    K_Per = ""
    td_ck = row.find_all('td')
    if td_ck:
        ERAck = td_ck[7]
        IPck = td_ck[14]
        GSck = td_ck[9]
        FIPck = td_ck[27]
        BBck = td_ck[19]
        SOck = td_ck[21]
        BFck = td_ck[25]
    if ERAck:
        ERA = ERAck.text
    if IPck:
        IP = IPck.text
    if GSck:
        GS = GSck.text
    if FIPck:
        FIP = FIPck.text
    if ERAck and FIPck:
        E_F = floatsub(ERA,FIP)
    if BBck:
        BB = BBck.text
    if SOck:
        SO = SOck.text
    if BFck:
        BF = BFck.text
    if SOck and BFck:
        K_Per = floatdiv(SO,BF)
    if BBck and BFck:
        BB_Per = floatdiv(BB,BF)


    return ERA, IP, GS, FIP, E_F, K_Per, BB_Per

def get_player_batting_stats(row):
    '''
    for that player from the standard batting table.
    '''
    AVG = ""
    OBP = ""
    SLG = ""
    td_ck = row.find_all('td')
    if td_ck:
        AVGck = td_ck[17]
        OBPck = td_ck[18]
        SLGck = td_ck[19]
    if AVGck:
        AVG = AVGck.text
    if OBPck:
        OBP = OBPck.text
    if SLGck:
        SLG = SLGck.text
    
    return AVG,OBP,SLG

def get_player_stats_from_fangraphs(player_name, year_first):
    '''
    navigate to fangraphs to get more player stats
    '''
    fangraph_stats = []
    fangraph_starting_url = "%s=%s" % ("http://www.fangraphs.com/players.aspx?lastname", player_name)
    if fangraph_starting_url:
        fangraph_request = requests.get(fangraph_starting_url)
        if fangraph_request:
            fangraph_text = fangraph_request.text
            fangraph_soup = bs4.BeautifulSoup(fangraph_text, parse_only=bs4.SoupStrainer("div", id="PlayerSearch1_panSearch"))
            res_table = fangraph_soup.find("table", {"cellspacing" :"0", "cellpadding" :"2px"})
            if not res_table:
                fangraph_stats = get_player_info_from_fangraphs(fangraph_text)
                return fangraph_stats
            rows = res_table.find_all("tr")
            if not rows: 
                return None
            for row in rows:
                td_ck = row.find_all("td")
                name_ck = td_ck[0]
                year_ck = td_ck[2]
                if name_ck:
                    name = name_ck.text
                    href = name_ck.find("a").get("href")
                if year_ck:
                    year = year_ck.text[:4]
                if name == player_name and year == year_first:
                    if href[-1:] == "P":
                        href += "B"
                    fangraph_player_url = "%s%s" % ("http://www.fangraphs.com/",href)
                    if fangraph_player_url:
                        fangraph_player_request = requests.get(fangraph_player_url)
                        if fangraph_player_request:
                            fangraph_player_text = fangraph_player_request.text
                            fangraph_stats = get_player_info_from_fangraphs(fangraph_player_text)
                            return fangraph_stats

    return fangraph_stats 
                    

def get_player_info_from_fangraphs(fangraph_player_text):
    years = ""
    ubrs = ""
    wrcs = ""
    w_years = ""
    wpas = ""
    clutchs = ""
    valid_year = re.compile("^[12][0-9]{3}")
    leaders = re.compile("^http://www.fangraphs.com/leaders.aspx")
    url_soup = bs4.BeautifulSoup(fangraph_player_text, parse_only=bs4.SoupStrainer("form"))
    url_form = url_soup.find("form").get("action")
    if url_form[-1:] == "P":
        url_bat = "%s%sB" % ("http://www.fangraphs.com",url_form[1:])
        fangraph_player_request = requests.get(url_bat)
        if fangraph_player_request:
            fangraph_player_text = fangraph_player_request.text

    fangraph_p_soup = bs4.BeautifulSoup(fangraph_player_text, parse_only=bs4.SoupStrainer("div", id="SeasonStats1_dgSeason2"))
    res_table = fangraph_p_soup.find("table")
    if res_table:
        rows = res_table.find_all("tr")
        for row in rows:
            year = ""
            ubr = ""
            wrc = ""
            td_ck = row.find_all("td")
            if td_ck:
                tag = td_ck[0].find("a", {"href" : leaders})
                if tag:
                    year_ck = td_ck[0]
                    ubr_ck = td_ck[12]
                    wrc_ck = td_ck[18]
                    if year_ck:
                        if valid_year.match(year_ck.text):
                            year = year_ck.text
                            if ubr_ck:
                                ubr = ubr_ck.text.replace(u'\xa0', u'') #remove nonbreaking spaces in fangraph tables
                            if wrc_ck:
                                wrc = wrc_ck.text.replace(u'\xa0', u'') #remove nonbreaking spaces in fangraph tables
                            years = "|".join([years,year])
                            ubrs = "|".join([ubrs,ubr])
                            wrcs = "|".join([wrcs,wrc])      

    fangraph_w_soup = bs4.BeautifulSoup(fangraph_player_text, parse_only=bs4.SoupStrainer("div", id="SeasonStats1_dgSeason5"))
    w_table = fangraph_w_soup.find("table")
    if w_table: #some players don't have the Win Probability table
        w_rows = w_table.find_all("tr")
        for wrow in w_rows:
            w_year = ""
            wpa = ""
            clutch = ""
            td_w_ck = wrow.find_all("td")
            if td_w_ck:
                tag_w = td_w_ck[0].find("a", {"href" : leaders})
                if tag_w:
                    w_year_ck = td_w_ck[0]
                    wpa_ck = td_w_ck[2]
                    clutch_ck = td_w_ck[11]
                    if w_year_ck:
                        if valid_year.match(w_year_ck.text):
                            w_year = w_year_ck.text
                            if wpa_ck:
                                wpa = wpa_ck.text.replace(u'\xa0', u'')
                            if clutch_ck:
                                clutch = clutch_ck.text.replace(u'\xa0', u'')
                            w_years = "|".join([w_years, w_year])
                            wpas = "|".join([wpas, wpa])
                            clutchs = "|".join([clutchs,clutch])

    
    return years[1:], ubrs[1:], wrcs[1:], w_years[1:], wpas[1:], clutchs[1:]

def get_player_info_from_main_player_page(player_text):
    '''
    Takes the text from the player's webpage and returns strings for the player's name and position(s)
    '''
    positions = ""
    player_soup = bs4.BeautifulSoup(player_text, parse_only=bs4.SoupStrainer("div", id="info_box")) 
    positions_info = player_soup.find("span", itemprop="role")
    if positions_info:
        positions_list = positions_info.text.replace(" and ",", ").split(", ")
        positions = "|".join(positions_list)

    return positions

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
    wars = [td.text for td in war_soup.select('tr.full > td:nth-of-type(19)')]
    WARs_pitcher = "|".join(wars)

    return WARs_pitcher


def get_player_info_from_postseason_batting(player_text):
    '''
    for that player from the postseason batting table.
    '''
    player_soup = bs4.BeautifulSoup(player_text, parse_only=bs4.SoupStrainer("table", id="batting_postseason")) 
    rows = player_soup.find_all("tr", {"class" : ""})
    if not rows: #if there are no values, there is no table
        return None
    playoffs = ""
    playoffs_won = ""
    worldseries = ""
    worldseries_won = ""
    playoff_str = re.compile("[N|A]LCS")
    worldseries_str = re.compile("WS\.shtml")
    for row in rows:
        year = ""
        win = None
        year_ck = row.find("td", {"csk" : True})
        if year_ck:
            year = year_ck.get("csk")[:4]
        td_ck = row.find_all('td')
        if td_ck:
            res = td_ck[6].text
            if "W" in res:
                win = year
        playoff_ck = row.find("a", {"href" : playoff_str})
        if playoff_ck:
            playoff = year
            playoffs = "|".join([playoffs,playoff])

            if win:
                playoff_won = win
                playoffs_won = "|".join([playoffs_won,playoff_won])
                
        worldseries_ck = row.find("a", {"href" : worldseries_str})
        if worldseries_ck:
            ws = year
            worldseries = "|".join([worldseries,ws])

            if win:
                ws_won = win
                worldseries_won = "|".join([worldseries_won,ws_won])

    return playoffs[1:], playoffs_won[1:], worldseries[1:], worldseries_won[1:]

def get_player_info_from_postseason_pitching(player_text):
    '''
    for that player from the postseason pitching table.
    '''
    player_soup = bs4.BeautifulSoup(player_text, parse_only=bs4.SoupStrainer("table", id="pitching_postseason")) 
    rows = player_soup.find_all("tr", {"class" : ""})
    if not rows: #if there are no values, there is no table
        return None
    playoffs = ""
    playoffs_won = ""
    worldseries = ""
    worldseries_won = ""
    playoff_str = re.compile("[N|A]LCS")
    worldseries_str = re.compile("WS\.shtml")
    for row in rows:
        year = ""
        win = None
        year_ck = row.find("td", {"csk" : True})
        if year_ck:
            year = year_ck.get("csk")[:4]
        td_ck = row.find_all('td')
        if td_ck:
            res = td_ck[6].text
            if "W" in res:
                win = year
        playoff_ck = row.find("a", {"href" : playoff_str})
        if playoff_ck:
            playoff = year
            playoffs = "|".join([playoffs,playoff])

            if win:
                playoff_won = win
                playoffs_won = "|".join([playoffs_won,playoff_won])
                
        worldseries_ck = row.find("a", {"href" : worldseries_str})
        if worldseries_ck:
            ws = year
            worldseries = "|".join([worldseries,ws])

            if win:
                ws_won = win
                worldseries_won = "|".join([worldseries_won,ws_won])

    return playoffs[1:], playoffs_won[1:], worldseries[1:], worldseries_won[1:]



alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "y", "z"]
for letter in alphabet:
    dict_response = make_br_alpha_player_dict(letter)
    str_file = "letter_" + letter
    make_player_employment_csv_file(dict_response, str_file)
    make_player_bio_csv_file(dict_response, str_file)
    make_player_stats_nonpitcher_csv_file(dict_response, str_file)
    make_player_stats_pitcher_csv_file(dict_response, str_file)
    make_player_full_csv_file(dict_response, str_file)          

        