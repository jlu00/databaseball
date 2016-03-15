#Brianna Pinder

import os
import csv

#data scraped from text files from retrosheet.org
#game files can be found on http://www.retrosheet.org/gamelogs/index.html

def create_park_dict():
    '''
    Creates a dictionary of the park abbreviations and their full current names 
    '''
    filename = 'parkcode.txt'
    with open(filename, mode='r') as parkfile:
        reader = csv.reader(parkfile)
        myparkdict = {rows[0]:rows[1] for rows in reader if rows}
    return myparkdict

#create team list
def rearrange_data(rows):
    '''
    Creates a list for a team, including its id, name, start date, end date, and cid
    '''
    fdate = ""
    edate = ""
    cid = rows[0]
    tid = rows[1]
    tname = "%s %s" % (rows[4],rows[5])
    if rows[7] != "":
        holdf = []
        holdf = rows[7].split("/")
        month = holdf[0].rjust(2, "0")
        day = holdf[1].rjust(2, "0")
        year = holdf[2].rjust(2, "0")
        fdate = "%s%s%s" % (year, month, day)
    if rows[8] != "":
        holde = []
        holde = rows[8].split("/")
        month = holde[0].rjust(2, "0")
        day = holde[1].rjust(2, "0")
        year = holde[2].rjust(2, "0")
        edate = "%s%s%s" % (year, month, day)
    return [tid,tname, fdate, edate, cid]

def create_team_list():
    '''
    Creates a list of all current team names
    ''' 
    filename = 'CurrentNames.csv'
    with open(filename, mode='r') as teamfile:
        reader = csv.reader(teamfile)
        myteamlist = [rearrange_data(rows) for rows in reader if rows]
    return myteamlist

def create_team_codes_historic():
    '''
    Creates a list of all historic team names
    '''
    filename = 'TeamCodes.txt'
    with open(filename, mode='r') as teamfile:
        reader = csv.reader(teamfile)
        historicteamdict = {rows[0]:rows[4]+" "+rows[5] for rows in reader if rows}
    return historicteamdict

def find_teams(val, myteamlist):
    '''
    Finds all matches for team abbr in the myteamlist, loops through and at each index, gets the dates,
    determines if the game date is in the range, returns the team name if it does
    '''

    t1id = val[1]
    t2id = val[2]
    gdate = val[0]
    team1name = None
    matches = [x for x in myteamlist if x[0] == t1id]
    for match in matches:
        m_startdate = match[2]
        m_enddate = match[3]
        if m_enddate != "":
            if m_startdate <= gdate <= m_enddate:
                team1name = match[1]
        elif gdate >= m_startdate:
            team1name = match[1]
    team2name = None
    matches = [x for x in myteamlist if x[0] == t2id]
    for match in matches:
        m_startdate = match[2]        
        m_enddate = match[3]
        if m_enddate != "":
            if m_startdate <= gdate <= m_enddate:
                team2name = match[1]
        elif gdate >= m_startdate:
            team2name = match[1]
    return team1name, team2name

def transform(strFilename, parkdict, teamlist, teamdict, strWriteFile):
    '''
    Converts a text file of games into rows of data in a csv file in strWriteFile
    '''
    fileNameOnly = strFile[-10:-4]
    fileDir = strFile[:-10]
    game_year = fileNameOnly[-4:]
    strReadFile = strFilename

    with open(strReadFile, mode='r') as infile:
        reader = csv.reader(infile)
        with open(strWriteFile, mode='a') as outfile:
            writer = csv.writer(outfile)
            mylist = [[rows[0],rows[3],rows[6],rows[9],rows[10],rows[16],rows[22],rows[25],rows[50],rows[53]] for rows in reader if rows]
            inc = 0
            for val in mylist:
                key = "%s%s" % (game_year,inc)
                game_date = val[0][:4] + "-" + val[0][4:6] + "-" + val[0][6:]
                teamnames = find_teams(val,teamlist)
                team1 = teamnames[0]
                team2 = teamnames[1]
                if not team1:
                    team1 = teamdict.get(val[1])
                if not team2:
                    team2 = teamdict.get(val[2])
                if team1 is None:
                    print("missing team1",val[1],key)
                if team2 is None:
                    print("missing team2",val[2],key)
                team1_runs = val[3]
                team2_runs = val[4]
                team1_hits = val[6]
                team1_hrs = val[7]
                team2_hits = val[8]    
                team2_hrs = val[9]
                if int(team1_runs) > int(team2_runs):
                    winner = team1
                elif int(team2_runs) > int(team1_runs):
                    winner = team2
                else:
                    winner = "tie"
                stadium = parkdict.get(val[5])
                postseason = False
                inc += 1
                writer.writerow([key, game_date, stadium, team1, team2, team1_runs, team2_runs, team1_hits, team2_hits, team1_hrs, team2_hrs, winner, postseason])

    return "finished"
        


for subdir, dirs, files in os.walk('game_files/'):
    parkdict = create_park_dict()
    teamlist = create_team_list()
    teamdict = create_team_codes_historic()
    strWriteFile = "games_output/regularseason_done.txt"
    with open(strWriteFile, mode='w') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(["game_id","game_date","stadium","team1","team2","team1_runs","team2_runs","team1_hits","team2_hits","team1_hrs","team2_hrs","winner","postseason"])
    for f in files:
        strFile = os.path.join(subdir, f)
        fileNameOnly = strFile[-10:-4]
        result = transform(strFile, parkdict, teamlist, teamdict, strWriteFile)