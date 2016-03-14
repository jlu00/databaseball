#The purpose of this file is to find games given specific parameters.
#
#Created by Jessica Lu

import os

GAME_COLS = dict(
        game_date='Date',
        team1='Away Team',
        team2='Home Team',
        winner='Winner',
        team1_hits='Away Team Hits',
        team2_hits='Home Team Hits',
        team1_runs='Away Team Runs',
        team2_runs='Home Team Runs',
        team1_hrs='Away Team Home Runs',
        team2_hrs='Home Team Home Runs',
        stadium="Stadium",
)

DATA_DIR = os.path.dirname(__file__)
GAME_DATABASE = os.path.join(DATA_DIR, 'all_games.db')

TEAM_ORDER = ['team1', 'team2', 'winner']

TEAM_STATS = ['hits', 'runs', 'hrs']

STAT_INPUTS = ['hits_low', 'hits_high', 'runs_low', 'runs_high', 'hrs_low', 'hrs_high']

OPERATIONS_DICT = {'team1': '=', 'team2': '=', 'winner': '=', 'stats_low': ">=", 'stats_high': "<="} 

def find_games(args_from_ui): #Code inspired from PA 3
    if not args_from_ui:
        return ([], [])
    db = sqlite3.connect('all_games.db')
    c = db.cursor()
    sql_query, args = create_find_query(args_from_ui)
    if not args:
        return ([], [])
    r = c.execute(sql_query, args)
    results = r.fetchall()
    db.close()
    if results:
        return format_results(results, c)
    else:
        return([], [])

def format_results(results, c): #Function taken from PA 3 
    results_list = []
    for i in results:
        if list(i) not in results_list:
            results_list.append(list(i))
    s = get_header(c)
    header = clean_header(s)
    return header, results_list

def get_header(cursor): #Function taken from PA 3
    desc = cursor.description
    header = ()
    for i in desc:
        header = header + (clean_header(i[0]),)
    return list(header)

def clean_header(s): #Function taken from PA 3
    for i in range(len(s)):
        if s[i] == ".":
            s = s[i+1:]
            break
    return s

def create_find_query(args_from_ui):
    if not args_from_ui:
        return([], [])
    else:
        sql_query = "SELECT game_date, team1, team2, stadium, team1_runs, team2_runs, team1_hrs, team2_hrs, team1_hits, team2_hits, winner FROM all_games "
        new_args = {}
        for key in args_from_ui:
            if not args_from_ui[key] == "":
                new_args[key] = args_from_ui[key]
        sql_query += determine_find_where(new_args)
        sql_query += " GROUP BY game_date ORDER BY game_date"
        args = create_db_arg(new_args)
        return sql_query, args

def determine_find_where(args_from_ui):
    where = get_date_input(args_from_ui)
    for t in TEAM_ORDER:
        if t in args_from_ui:
            where.append(t + OPERATIONS_DICT[t] + '?')
    for s in TEAM_STATS:
        where += (get_stat_boundaries(args_from_ui, s))
    w = " AND ".join(where)
    return "WHERE " + w

def get_date_input(args_from_ui):
    where = []
    if "date_start" in args_from_ui:
        where.append("game_date>=?")
    if "date_end" in args_from_ui:
        where.append("game_date<=?")
    return where

def get_stat_boundaries(args_from_ui, stat):
    print(args_from_ui)
    where = []
    stat_low = stat + "_low"
    stat_high = stat + "_high"
    
    if stat_low in args_from_ui:
        if args_from_ui['Apply_Box_Score_Items_to_Away_only']:
            where.append("team1_" + stat + OPERATIONS_DICT['stats_low'] + '?')
        else:
            where.append("(team1_" + stat + "+" + "team2_" + stat + ")" + OPERATIONS_DICT['stats_low'] + '?')
    if stat_high in args_from_ui:
        if args_from_ui['Apply_Box_Score_Items_to_Home_only']:
            where.append("team2_" + stat + OPERATIONS_DICT['stats_high'] + '?')
        else:
            where.append("(team1_" + stat + "+" + "team2_" + stat + ")" + OPERATIONS_DICT['stats_high'] + '?')
    
    return where

def create_db_arg(args_from_ui):
    db_arg = []
    db_arg += create_date_range(args_from_ui)
    db_arg += add_teams(args_from_ui)
    db_arg += add_stats(args_from_ui)
    return db_arg


def create_date_range(args_from_ui):
    args = []
    if "date_start" in args_from_ui:
        args.append(args_from_ui["date_start"])
    if "date_end" in args_from_ui:
        args.append(args_from_ui["date_end"])
    return args


def add_teams(args_from_ui):
    args = []
    for s in TEAM_ORDER:
        if s in args_from_ui:
            args.append(args_from_ui[s])
    return args

def add_stats(args_from_ui):
    args = []
    for s in STAT_INPUTS:
        if s in args_from_ui:
            args.append(int(args_from_ui[s]))
    return args
