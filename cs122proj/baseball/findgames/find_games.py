#The purpose of this file is to find games given specific parameters.
#
#Created by Jessica Lu

import os
import sqlite3

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

GAME_DATABASE = "all_games.db"
TEAM_ORDER = ['team1', 'team2', 'winner']
TEAM_STATS = ['hits', 'runs', 'hrs']
STAT_INPUTS = ['hits_low', 'hits_high', 'runs_low', 'runs_high', 'hrs_low', 'hrs_high']
OPERATIONS_DICT = {'team1': '=', 'team2': '=', 'winner': '=', 'stats_low': ">=", 'stats_high': "<="} 

def find_games(args_from_ui): #Code inspired from PA 3
    '''
    Inputs: arguments from user
    Outputs: results from a parameterized SQL query
    '''
    if not args_from_ui:
        return ([], [])
    db = sqlite3.connect(GAME_DATABASE)
    c = db.cursor()
    sql_query, args = create_find_query(args_from_ui)
    if not args:
        return ([], [])
    r = c.execute(sql_query, args)
    results = r.fetchall()
    db.close()
    if results:
        return format_results(results, c, GAME_COLS)
    else:
        return []

def format_results(results, c, col_dictionary): #Function taken from PA 3 
    '''
    Inputs: the results from the query, the cursor object, the columns dictionary 
    Outputs: a header list and a results list
    '''
    results_list = []
    for i in results:
        if list(i) not in results_list:
            results_list.append(list(i))
    s = get_header(c)
    header = clean_header(s)
    header = [col_dictionary.get(col, col) for col in header]
    return header, results_list

def get_header(cursor): #Function taken from PA 3
    '''
    Inputs: the cursor object
    Outputs: the header
    '''
    desc = cursor.description
    header = ()
    for i in desc:
        header = header + (clean_header(i[0]),)
    return list(header)

def clean_header(s): #Function taken from PA 3
    '''
    Inputs: An item in the cursor description
    Outputs: a clean string 
    '''
    for i in range(len(s)):
        if s[i] == ".":
            s = s[i+1:]
            break
    return s

def create_find_query(args_from_ui):
    '''
    Inputs: arguments from the user
    Ouputs: a parameterized sql query and its arguments
    '''
    if not args_from_ui:
        return([], [])
    else:
        sql_query = "SELECT game_date, team1, team2, stadium, team1_runs, team2_runs, " 
        sql_query += " team1_hrs, team2_hrs, team1_hits, team2_hits, winner FROM all_games "
        new_args = {}
        for key in args_from_ui:
            if not args_from_ui[key] == "":
                new_args[key] = args_from_ui[key]
        sql_query += determine_find_where(new_args)
        sql_query += " GROUP BY game_date ORDER BY game_date"
        print(sql_query, "hie")
        args = create_db_arg(new_args)
        return sql_query, args

def determine_find_where(args_from_ui):
    '''
    Inputs: arguments from the user
    Outputs: a string with the WHERE statement
    '''
    where = get_date_input(args_from_ui)
    for t in TEAM_ORDER:
        if t in args_from_ui:
            where.append(t + OPERATIONS_DICT[t] + '?')
    for s in TEAM_STATS:
        where += (get_stat_boundaries(args_from_ui, s))
    w = " AND ".join(where)
    return "WHERE " + w

def get_date_input(args_from_ui):
    '''
    Inputs: arguments from the user
    Outputs: a date range for the WHERE statement
    '''
    where = []
    if "date_start" in args_from_ui:
        where.append("game_date>=?")
    if "date_end" in args_from_ui:
        where.append("game_date<=?")
    return where

def get_stat_boundaries(args_from_ui, stat):
    '''
    Inputs: arguments from the user, and the stat
    Outputs: the WHERE statement based on if the user
    had inputed high, low or both, as well as apply to home only or away only
    '''
    where = []
    stat_low = stat + "_low"
    stat_high = stat + "_high"
    if stat_low in args_from_ui:
        if args_from_ui['Apply_Box_Score_Items_to_Away_only']:
            where.append("team1_" + stat + OPERATIONS_DICT['stats_low'] + '?')
        elif args_from_ui['Apply_Box_Score_Items_to_Home_only']:
            where.append("team2_" + stat + OPERATIONS_DICT['stats_low'] + '?')
        else:
            where.append("(team1_" + stat + "+" + "team2_" + stat + ")" + 
                OPERATIONS_DICT['stats_low'] + '?')
    if stat_high in args_from_ui:
        if args_from_ui['Apply_Box_Score_Items_to_Home_only']:
            where.append("team2_" + stat + OPERATIONS_DICT['stats_high'] + '?')
        elif args_from_ui['Apply_Box_Score_Items_to_Away_only']:
            where.append("team1_" + stat + OPERATIONS_DICT['stats_low'] + '?')
        else:
            where.append("(team1_" + stat + "+" + "team2_" + stat + ")" + 
                OPERATIONS_DICT['stats_high'] + '?')
    return where

def create_db_arg(args_from_ui):
    '''
    Inputs: arguments user input
    Outputs: a list of user's arguments for the paramterized SQL query
    '''
    db_arg = []
    db_arg += create_date_range(args_from_ui)
    db_arg += add_teams(args_from_ui)
    db_arg += add_stats(args_from_ui)
    return db_arg

def create_date_range(args_from_ui):
    '''
    Inputs: arguments from the user
    Outputs: a list with the date range, if applicable 
    '''
    args = []
    if "date_start" in args_from_ui:
        args.append(args_from_ui["date_start"])
    if "date_end" in args_from_ui:
        args.append(args_from_ui["date_end"])
    return args

def add_teams(args_from_ui):
    '''
    Inputs: arguments from the user
    Outputs: a list with the team arguments, if applicable
    '''
    args = []
    for s in TEAM_ORDER:
        if s in args_from_ui:
            args.append(args_from_ui[s])
    return args

def add_stats(args_from_ui):
    '''
    Inputs: arguments from the user
    OUtputs: a list with the stat arguments, if applicable
    '''
    args = []
    for s in STAT_INPUTS:
        if s in args_from_ui:
            args.append(int(args_from_ui[s]))
    return args
