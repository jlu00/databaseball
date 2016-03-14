#The purpose of this file is to compare players given specific parameters.
#
#Created by Jessica Lu

import os
import sqlite3
from findgames import find_games
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


GAME_DATABASE = 'all_players.db'

PLAYER_STATS = ['nonpitcher.AVGs', 'nonpitcher.OBPs', 'nonpitcher.SLGs', 'nonpitcher.WARs_nonpitcher', 'nonpitcher.WRCs']

PITCHER_STATS = ['pitcher.WARs_pitcher', 'pitcher.ERAs', 'pitcher.FIPs', 'pitcher.K_Pers', 'pitcher.BB_Pers']


def compare_players(args_from_ui, pitcher): #Modified code from PA 3
    if not args_from_ui:
        return ([], [])

    db = sqlite3.connect(GAME_DATABASE)
    c = db.cursor()
              
    if pitcher:
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
    sql_query = "SELECT bios.name, "
    sql_query += ", ".join(stat_types)
    sql_query += " FROM bios JOIN " + table + " ON bios.player_id = " + table + ".player_id "
    sql_query += "WHERE bios.name LIKE ? OR bios.name LIKE ? LIMIT 2" 
    
    args = create_player_arg(args_from_ui)

    return sql_query, args

def create_player_arg(args_from_ui):
    args_list = []
    for key in args_from_ui:
        args_list.append('%' + args_from_ui[key] + '%')
    return args_list

def create_graphs(result, cols, pitcher):
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

def playergraph(data, players, labels, cursor, pitcher): #Inspired by code from Gustav 
    im = io.BytesIO()
    plt.figure(figsize=(6, 5))
    pos = (-.5, .5)
    xpos = np.linspace(0, round(max(data) + max(data)*.2, 2), 5)

    if data[0] > data[1]:
        colors = ("#00b34d", '#ff3232')
    else:
        colors = ('#ff3232', '#00b34d')

    #average = fantasy_team.calculate_league_average(stat, cursor, pitcher)

    print(labels)

    plt.barh(pos, data, color=colors, align="center")
    plt.yticks(pos, (players))
    plt.xticks(xpos, xpos)
    plt.title(labels)
    plt.ylim(-2, 2)
    plt.tight_layout(pad=0)

    #average = calculate_league_average()


    plt.show()
    
    plt.savefig(im, format='png', transparent=True)
    plt.close()
    im.seek(0)
    imagedata = base64.b64encode(im.getvalue())

    return base64.b64encode(im.getvalue())