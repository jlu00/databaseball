#The purpose of this file is to compare players given specific parameters.
#
#Created by Jessica Lu

import os
import sqlite3
from findgames import find_games
from findgames import fantasy_team
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import io
import urllib, base64

PLAYER_COLS = dict(
        player1 = 'player 1',
        player2 = 'player 2',
        name = 'Name',
        AVGs = "Batting Averages",
        OBPs = "On Base Percentage",
        SLGs = "Slugging Percentage",
        WARs_nonpitcher = "Wins Above Replacement",
        WRCs = "Weighted Runs Created",
)

PITCHER_COLS = dict(
        player1 = 'player 1',
        player2 = 'player 2',
        name = 'Name',
        WARS_pitcher = "Wins Above Replacement",
        ERAs = "Earned Run Average",
        FIPs = "Fielding Independent Pitching",
        K_Pers = "Strike out rate",
        BB_Pers = "Walk rate",

)

PLAYER_DICT = {'Wins Above Replacement': 'WARs_nonpitcher', 'On Base Percentage': 'OBPs',
                'Batting Averages': 'AVGs', 'Slugging Percentage': 'SLGs', 'Runs created by base running': 'UBR_WRC_Years',
                "Base Running ability": "UBRs", "Weighted Runs Created": "WRCs", "Win Probability Added": "WPAs",
                "Clutch Hitting Ability": "Clutchs"}
  
PITCHER_DICT = {'WARs_pitcher': 'WARs_pitcher', "Earned Run Average": 'ERAs', 'Innings Pitched': 'IPs',
                "Games Started": "GSs", "Fielding Independent Pitching":"FIPs", "ERA-FIP Spreads": "E_Fs",
                "Strike out rate": "K_Pers", "Walk rate": "BB_Pers"}

GAME_DATABASE = 'all_players.db'
PLAYER_STATS = ['nonpitcher.AVGs', 'nonpitcher.OBPs', 'nonpitcher.SLGs', 'nonpitcher.WARs_nonpitcher', 'nonpitcher.WRCs']
PITCHER_STATS = ['pitcher.WARs_pitcher', 'pitcher.ERAs', 'pitcher.FIPs', 'pitcher.K_Pers', 'pitcher.BB_Pers']

def compare_players(args_from_ui, pitcher): #Modified code from PA 3
    '''
    Inputs: arguments from user, pitcher boolean (True if pitcher)
    Outputs: SQL results of stats from the two players.
    '''
    if not args_from_ui:
        return ([], [])
    db = sqlite3.connect(GAME_DATABASE)
    c = db.cursor() 
    if pitcher: #selects the proper table and stats
        table = "pitcher"
        stat_type = PITCHER_STATS
        column_dict = PITCHER_COLS
    else:
        table = "nonpitcher"
        stat_type = PLAYER_STATS
        column_dict = PLAYER_COLS
    sql_query, args = create_player_query(args_from_ui, stat_type, table)
    if not args:
        return ([], [])
    r = c.execute(sql_query, args)
    results = r.fetchall()
    db.close()
    if results:
        return find_games.format_results(results, c, column_dict)
    else:
        return([], [])

def create_player_query(args_from_ui, stat_types, table):
    '''
    Inputs: arguments from user, list of stats to grab, which table to use
    Outputs: the parameterized sql query and arguments list 
    '''
    sql_query = "SELECT bios.name, "
    sql_query += ", ".join(stat_types)
    sql_query += " FROM bios JOIN " + table + " ON bios.player_id = " + table + ".player_id "
    sql_query += "WHERE bios.name LIKE ? OR bios.name LIKE ? LIMIT 2" 
    args = create_player_arg(args_from_ui)
    return sql_query, args

def create_player_arg(args_from_ui):
    '''
    Inputs: arguments from the user
    Outputs: a list of arguments for the parameterized SQL query
    '''
    args_list = []
    for key in args_from_ui:
        args_list.append('%' + args_from_ui[key] + '%')
    return args_list

def create_graphs(result, cols, pitcher):
    '''
    Inputs: the result list from the player query,
    the list of names describing the columns, and the pitcher boolean
    Outputs: A list of graphs from matplotlib based on player results 
    '''
    db = sqlite3.connect(GAME_DATABASE)
    c = db.cursor()
    graph_objects = []
    players = (result[0][0], result[1][0])
    data_tuples = []
    for r in range(1, len(result[0])):
        data_tuples.append((round(result[0][r], 3), round(result[1][r], 3)))
    for stat in range(len(data_tuples)):
        graph_objects.append(playergraph(data_tuples[stat], players, cols[stat + 1], c, pitcher))
    return graph_objects

def playergraph(data, players, labels, cursor, pitcher): #Inspired by code from Gustav in Office Hours
    '''
    Inputs: the stats to plot, the name of players, the label of the
    stat, the cursor object and the pitcher boolean
    Outputs: An encoded matplotlib graph 

    Calls the calculate_league_average function in fantasy_team
    to draw a blue horizontal line for the league average. 
    ''' 
    im = io.BytesIO()
    plt.figure(figsize=(7, 5))
    pos = (-.5, .5)
    xpos = np.linspace(0, round(max(data) + max(data)*.2, 2), 5)
    if data[0] > data[1]:
        colors = ("#00b34d", '#ff3232')
    else:
        colors = ('#ff3232', '#00b34d')

    if pitcher:
        stat_dict = PITCHER_DICT
    else:
        stat_dict = PLAYER_DICT
    
    avg = fantasy_team.calculate_league_average(stat_dict[labels], cursor, pitcher)

    plt.axvline(avg)
    plt.barh(pos, data, color=colors, align="center")
    plt.yticks(pos, (players))
    plt.xticks(xpos, xpos)
    plt.title(labels)
    plt.ylim(-2, 2)
    plt.tight_layout(pad=0)
    plt.savefig(im, format='png', transparent=True)
    plt.close()
    im.seek(0)
    imagedata = base64.b64encode(im.getvalue())

    return base64.b64encode(im.getvalue())