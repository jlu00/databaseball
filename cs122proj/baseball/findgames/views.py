from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponse
from django.template import loader, Context, RequestContext
from datetime import datetime
from django.db import connection
import os
from findgames import forms
import traceback
import sys
from findgames import playerteamobjects as Classes
import sqlite3
import operator


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
		WARs_nonpitcher = "Wins Above Replacement",
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
	roster = None
	form = forms.FantasyForm(request.GET or None)
	if request.method == "GET":
		if form.is_valid():
			args = {}
			prefs_pos = []
			prefs_pitch = []
			params = {}
			for key in form.cleaned_data:
				args[key] = form.cleaned_data[key] 
			
			for i in range(1, 4):
				s = 'stat' + str(i)
				if s in args and args[s]:
					prefs_pos.append(args[s])
			for i in range(4, 9):
				s = 'stat' + str(i)
				if s in args and args[s]:
					prefs_pitch.append(args[s])
				
			res = go(prefs_pos, prefs_pitch, params)
			roster = res.roster
			
	else:
		form = forms.FantasyForm()
	
	if roster is None:
		context['result'] = None
	else:
		result = roster
		context['result'] = roster
	
	context['form'] = form
	return render(request, 'findgames/fantasy.html', context)
            
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
    sql_query = "SELECT bios.name, nonpitcher.AVGs, nonpitcher.OBPs, nonpitcher.SLGs, nonpitcher.WARS_nonpitcher, nonpitcher.WRCs "
    sql_query += "FROM bios JOIN nonpitcher ON bios.player_id = nonpitcher.player_id "
    sql_query += "WHERE bios.name = ? OR bios.name = ?" 
    
    args = create_player_arg(args_from_ui)

    return sql_query, args

def create_player_arg(args_from_ui):
    args_list = []
    for key in args_from_ui:
        args_list.append(args_from_ui[key])
    return args_list

def compute_team_win_percentage(team):
    '''
    Computes the expected win percentage for a team of players created by the user
    Based on wins above replacement which is then converted into pythagorean wins
    '''
    WARs = {}
    for i in teams:
        WARS[i] = 0
        for j in teams[i]:
            years = compute_years_played(i)
            WARS[i] += grab_stat(j, ["WAR"], [years])

def compute_wins(WAR):
    '''
    According to baseballreference.com, a zero-WAR team would be expected
    to win 32 percent of its games
    '''
    zero_win_constant = .320
    games = 162
    total_wins = zero_win_constant * games + WAR
    win_percentage = total_wins / games
    return win_percentage
            
def create_team(prefs_pos, prefs_pitch, params):

    '''
    Sample prefs:
    ['wOBA', 'OBP']
    Sample params:
    {'date': (1980, 2015), 'playoffs': True, 'all_star': True, 'current_player': False}
    '''
    db = sqlite3.connect('all_players.db')
    c = db.cursor()
    players = {}
    for i in prefs_pos:
        players = grab_players(i, players, False, c)

    for i in prefs_pitch:
        players = grab_players(i, players, True, c)

    db.close()
    players = apply_params(players, params)
    for i in players:
        a = compute_power_index(players[i], prefs_pos, prefs_pitch)
        players[i].incr_power_index(a)


    team = select_top_pos(players)
    return team


def grab_players(pref, players, pitcher, cursor):
	print('WORKING')
	new_pref = convert_pref(pref, pitcher)
	if pitcher:
		query = """SELECT bios.name, bios.span, bios.positions, """ + new_pref + """, bios.player_id FROM bios
			JOIN pitcher ON bios.player_id = pitcher.player_id WHERE(bios.years_played > 2 AND """ + pref + """ != '') ORDER BY """ + pref + """ DESC LIMIT 80;"""
	else:
		query = """SELECT bios.name, bios.span, bios.positions, """ + new_pref + """, bios.player_id FROM bios
             JOIN nonpitcher ON bios.player_id = nonpitcher.player_id WHERE (bios.positions != 'Pitcher' AND bios.years_played > 2 AND  """ + pref + """ != '') ORDER BY """ + pref + """ DESC LIMIT 80;"""
    r = cursor.execute(query)
    results_pos = r.fetchall()
    rank = 0
    for j in results_pos:
        if 'name' in j:
            continue
        name = j[0].split()
        pos = j[2]
        first_pos = j[2]
        if len(pos.split('|')) > 1:
            first_pos = pos.split('|')[0]
            other_pos = pos.split('|')[1]
        if first_pos == 'Outfielder':
            first_pos = 'Centerfielder'
        if first_pos == 'Pinch Hitter' or first_pos == 'Pinch Runner':
            continue
        new_player = Classes.Players(name[0], name[1], first_pos, j[4])
        if new_player.player_id not in players:
            years = j[1].split('-')
            new_player.add_years(years)
            new_player.add_stats(pref, j[3])
            new_player.add_rank(pref, rank)
            players[new_player.player_id] = new_player
        else:
            players[new_player.player_id].add_stats(pref, j[3])
            players[new_player.player_id].add_rank(pref, rank)
        rank += 1
    return players

def convert_pref(pref, pitcher):
    if pitcher:
        return 'pitcher.' + pref
    else:
        return 'nonpitcher.' + pref

def apply_params(players, params):
    '''
    Sample Params:
    'Years': (1988, 2000)
    'Playoffs': True
    'All Star': False
    '''
    new_players = {}
    if 'years' in params:
    	if len(params['years']) > 0:
    		for i in players:
    			if params['years']:
    				player_stays = ((int(players[i].years_played[0]) > params['years'][0] and 
    					int(players[i].years_played[0]) < params['years'][1]) or (int(players[i].years_played[1]) 
    						> params['years'][0] and int(players[i].years_played[1]) < params['years'][1]))
    				if  player_stays: 
    					new_players[i] = players[i]
    			if params['Playoffs']:
    				pass
    return new_players

def compute_power_index(player, prefs_pos, prefs_pitch):
    power_index = 0
    for i in player.ranks:
        if i in prefs_pos:
            power_index += (100 - player.ranks[i]) * (len(prefs_pos) - prefs_pos.index(i)) ** 2
        else:
            power_index += (100 - player.ranks[i]) * (len(prefs_pitch) - prefs_pitch.index(i)) ** 2
    return power_index

def select_top_pos(players):
    '''
    returns a dictionary 'roster' of the top players
    '''

    team = Classes.Teams()
    for i in players:
        team.add_player(players[i])
    return team

def compare_teams(teams, stats):
    for i in stats:
        for j in teams:
            calculate_team_stat(j, i)

def calculate_team_stat(team, stat):
    rv = 0
    counter = 0
    for position in team.roster:
        for player in team.roster[position]:
            if stat in player.stats:
                rv += player.stats[stat]
                counter += 1
    if counter != 0:
        return rv / counter
    else:
        return None

def calculate_pergame_runs(team):
    '''
    '''
    runs = 0
    for position in team.roster:
        if position != 'Pitcher':
            for player in team.roster[position]:
                runs += player.war
    return runs * 10 / 162


def go(prefs_pos, prefs_pitch, params):
    '''
    '''
    team = create_team(prefs_pos, prefs_pitch, params)
    #team.add_stat('Win Percentage', compute_wins(team.team_war))
    #team.add_stat('Team Batting Average', calculate_team_stat(team, 'AVGs'))
    #team.add_stat('Team OBP', calculate_team_stat(team, 'OBPs'))
    #team.add_stat('Team ERA', calculate_team_stat(team, 'ERAs'))
    #team.add_stat('Runs per Game', calculate_pergame_runs(team))
    #team.add_stat('Team Slugging', calculate_team_stat(team, 'SLGs'))
    return team

