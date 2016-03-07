from django.shortcuts import render_to_response, render
from django.http import HttpResponse
from django.template import loader, Context, RequestContext
from datetime import datetime
from django.db import connection
import os
from findgames import forms
import traceback
import sys

DATA_DIR = os.path.dirname(__file__)
DATABASE_FILENAME = os.path.join(DATA_DIR, 'all_games.db')

GAME_DETAIL_ORDER = {'date_start': 1, 'date_end': 2, 'team1': 3, 'team2': 4,
                    'winner': 5, 'team1_hits': 6, 'team2_hits': 7, 'team1_hits': 8,
                    'team2_hits': 9, 'team1_hrs': 10, 'team2_hrs': 11, 'ps': 12,
                    'stadium': 13}

TEAM_ORDER = ['team1', 'team2', 'winner']

TEAM_STATS = ['hits', 'runs', 'hrs']

OPERATIONS_DICT = {'team1': '=', 'team2': '=', 'winner': '=', 'stats': "="} 

def index(request):
	c = {'name': 'Jessica Lu'}
	return render(request, 'findgames/index.html', c)

def findresults(request):
	return render(request, 'findgames/findresults.html', {})
	
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
			try: 
				res = find_games(args)
			except Exception as e:
				bt = traceback.format_exception(*sys.exc_info()[:3])
				res = None
	else:
		form = forms.FindGameForm()
	
	if res is None:
		context['result'] = None
	elif isinstance(res, str):
		context['result'] = None
		context['err'] = res
		result = None
		cols = None
	else:
		columns, result = res
		
		if result and isinstance(result[0], str):
			result = [(r,) for r in result]
		
		context['result'] = result
		context['num_results'] = len(result)
		context['columns'] = [COLUMN_NAMES.GET(col, col) for col in columns]
	
	context['form'] = form
	
	return render(request, 'findgames/findgames.html', context)
		
def players(request):
	return render(request, 'findgames/players.html', {})

def fantasy(request):
	context = {}
	res = None
	form = forms.FantasyForm(request.GET or None)
	if request.method == "GET":
		if form.is_valid():
			args = {}
			for key in form.cleaned_data:
				args[key] = form.cleaned_data[key]
			try: 
				res = find_games(args)
			except Exception as e:
				bt = traceback.format_exception(*sys.exc_info()[:3])
				res = None
	else:
		form = forms.FantasyForm()
	
	if res is None:
		context['result'] = None
	elif isinstance(res, str):
		context['result'] = None
		context['err'] = res
		result = None
		cols = None
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
	db = sqlite3.connect('regular_season_games.db')
	print("hi")
	cursor = db.cursor()
	print("hi")
	sql_query = create_query(args_from_ui)
	print(sql_query)
	args = create_db_arg(args_from_ui)
	r = cursor.execute(sql_query, args)
	results = r.fetchall()
	return format_results(results, cursor)

def format_results(results, cursor):
	results_list = []
	for i in results:
		if list(i) not in results_list:
			results_list.append(list(i))
	s = get_header(c)
	header = clean_header(s)
	return header, results_list

def create_query(args_from_ui):
	print("yo")
	if not args_from_ui:
		return([], [])
	else:
		sql_query = "SELECT game_date, team1, team2, stadium, ps, team1_runs, team2_runs, team1_hrs, team2_hrs, team1_hits, team2_hits, winner FROM rs"
		new_args = {}
		for key in args_from_ui:
			if not args_from_ui[key] == "":
				new_args[key] = args_from_ui[key]
		sql_query += determine_where(new_args)
		sql_query += " GROUP BY date ORDER BY DESC"
		args = create_db_arg(new_args)
		return sql_query, args
    

def determine_where(args_from_ui):
    where = get_date_input(args_from_ui)
    for t in TEAM_ORDER:
        if t in args_from_ui:
            where.append(t + OPERATIONS_DICT[t] + '?')
    for s in TEAM_STATS:
        if s in args_from_ui:
            statement = "(team1_" + s + "+" + "team2_" + s + ")" + OPERATIONS_DICT['stats'] + '?'
            where.append(statement)
    w = " AND ".join(where)
    return "WHERE " + w

def get_date_input(args_from_ui):
    where = []
    if "date_start" in args_from_ui:
        where.append("date>=?")
    if "date_end" in args_from_ui:
        where.append("date<=?")
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
    for s in TEAM_STATS:
        if s in args_from_ui:
            args.append(int(args_from_ui[s]))
    return args

