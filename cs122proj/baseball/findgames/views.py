from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponse
from django.template import loader, Context, RequestContext
from datetime import datetime
from django.db import connection
import os
from findgames import forms
import traceback
import sys
import sqlite3

COLUMNS = dict(
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

STAT_COLS = dict(
		player1 = 'player 1',
		player2 = 'player 2',
		name = 'Name',
		AVGs = "Batting Averages",
		OBPs = "On Base Percentage",
		SLGs = "Slugging Percentage",
		WARS_nonpitcher = "Wins Above Replacement",
		WRCs = "Weighted Runs Created",

)

DATA_DIR = os.path.dirname(__file__)
DATABASE_FILENAME = os.path.join(DATA_DIR, 'all_games.db')

GAME_DETAIL_ORDER = {'date_start': 1, 'date_end': 2, 'team1': 3, 'team2': 4,
                    'winner': 5, 'team1_hits': 6, 'team2_hits': 7, 'team1_hits': 8,
                    'team2_hits': 9, 'team1_hrs': 10, 'team2_hrs': 11, 'postseason': 12,
                    'stadium': 13}

TEAM_ORDER = ['team1', 'team2', 'winner']

TEAM_STATS = ['hits', 'runs', 'hrs']

STAT_INPUTS = ['hits_low', 'hits_high', 'runs_low', 'runs_high', 'hrs_low', 'hrs_high']

OPERATIONS_DICT = {'team1': '=', 'team2': '=', 'winner': '=', 'stats_low': ">=", 'stats_high': "<="} 

def index(request):
	c = {'name': 'Jessica Lu'}
	return render(request, 'findgames/index.html', c)
	
def findgames(request):
	context = {}
	res = None
	form = forms.FindGameForm(request.GET or None)
	if request.method == "GET":
		form = forms.FindGameForm(request.GET)
		if form.is_valid():
			args = {}
			for key in form.cleaned_data:
				args[key] = form.cleaned_data[key]
			res = find_games(args)
		else:
			form = forms.FindGameForm()
	else:
		form = forms.FindGameForm()
	
	if res is None:
		context['result'] = "There were no results found."
	else:
		columns, result = res
		
		if result and isinstance(result[0], str):
			result = [(r,) for r in result]
		
		context['result'] = result
		context['num_results'] = len(result)
		context['columns'] = [COLUMNS.get(col, col) for col in columns]
	
	context['form'] = form
	
	return render(request, 'findgames/findgames.html', context)
		
def players(request):
	context = {}
	res = None
	if request.method == "GET":
		form1 = forms.PlayerForm(request.GET)
		if form1.is_valid():
			args = {}
			print(form1.cleaned_data)
			for key in form1.cleaned_data:
				args[key] = (form1.cleaned_data[key]).title()
			res = compare_players(args)
	else:
		form1 = forms.PlayerForm()
	if request.method == "GET" and not form1.is_valid():
		form2 = forms.PitcherForm(request.GET)
		form1 = forms.PlayerForm()
		if form2.is_valid():
			args = {}
			for key in form2.cleaned_data:
				key = key.title()
				args[key] = form2.cleaned_data[key]
			res = compare_players(args)
	else:
		form2 = forms.PitcherForm()
	
	if res is None:
		context['result'] = None
	else:
		columns, result = res
		
		if result and isinstance(result[0], str):
			result = [(r,) for r in result]
		context['result'] = result
		context['columns'] = [STAT_COLS.get(col, col) for col in columns]
	
	context['form1'] = form1
	context['form2'] = form2
	return render(request, 'findgames/players.html', context)
				

def fantasy(request):
	context = {}
	res = None
	form = forms.FantasyForm(request.GET or None)
	if request.method == "GET":
		if form.is_valid():
			args = {}
			for key in form.cleaned_data:
				args[key] = form.cleaned_data[key] 
			res = find_games(args)
			
	else:
		form = forms.FantasyForm()
	
	if res is None:
		context['result'] = None
	else:
		columns, result = res
		
		if result and isinstance(result[0], str):
			result = [(r,) for r in result]
		
		context['result'] = result
		context['num_results'] = len(result)
		context['columns'] = [COLUMN_NAMES.GET(col, col) for col in columns]
	
	context['form'] = form
	return render(request, 'findgames/fantasy.html', {'form': form})
            
def find_games(args_from_ui):
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
		return('There were no results found.', [])

def format_results(results, c):
	results_list = []
	for i in results:
		if list(i) not in results_list:
			results_list.append(list(i))
	s = get_header(c)
	header = clean_header(s)
	return header, results_list

def get_header(cursor):
    desc = cursor.description
    header = ()
    for i in desc:
        header = header + (clean_header(i[0]),)
    return list(header)

def clean_header(s):
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
	where = []
	stat_low = stat + "_low"
	stat_high = stat + "_high"
	
	if stat_low in args_from_ui:
		where.append("(team1_" + stat + "+" + "team2_" + stat + ")" + OPERATIONS_DICT['stats_low'] + '?')
	if stat_high in args_from_ui:
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

def compare_players(args_from_ui):
    if not args_from_ui:
        return ([], [])

    db = sqlite3.connect('all_players.db')
    c = db.cursor()
    sql_query, args = create_player_query(args_from_ui)
    if not args:
        return ([], [])
    r = c.execute(sql_query, args)
    results = r.fetchall()
    db.close()

    if results:
        return format_results(results, c)
    else:
        return("There were no results found.", [])

def create_player_query(args_from_ui):
    sql_query = "SELECT bios.name, stats_nonpitcher.AVGs, stats_nonpitcher.OBPs, stats_nonpitcher.SLGs, stats_nonpitcher.WARS_nonpitcher, stats_nonpitcher.WRCs "
    sql_query += "FROM bios JOIN stats_nonpitcher ON bios.player_id = stats_nonpitcher.player_id "
    sql_query += "WHERE bios.name = ? OR bios.name = ?" 
    
    args = create_player_arg(args_from_ui)

    return sql_query, args

def create_player_arg(args_from_ui):
    args_list = []
    for key in args_from_ui:
        args_list.append(args_from_ui[key])
    return args_list

