#jessbritommy

#Functions to get SQL Code

'''
Issues to work out:
Writing all of the code to compare the teams
How exactly to handle roster construction; specifically:
How many pitchers should I have?
How to handle the fact that for every other position you just need 1,
but for pitchers you need X > 1
Still need to get all the SQL coding done

'''

Stat_defs = {'ERA': '''Earned runs allowed (per 9 innings); derived by taking
            the number of earned runs allowed, normalizing to per game by multiplying
            by 9, and then dividing by number of innings pitched''',
            'BA': '''Batting average: calculated by taking total number of 
            hits divided by total number of plate appearances''',
            'OBP': '''On Base Percentage: total times reaching base divided by
            total plate appearances ''',
            'wOBA': '''Weighted on Base Average: a formula meant to calculate the
            overall offensive impact of a player. Formula:
            (0.690×uBB + 0.722×HBP + 0.888×1B + 1.271×2B + 1.616×3B +
            2.101×HR) / (AB + BB – IBB + SF + HBP) (HBP = Hit by pitch
            uBB = unintentional Base on Balls, AB = At Bats
            IBB = Intentional Bases on Balls, SF = Sacrifice Fly''',
            'WRC+': '''Weighted Runs Created--kind of like wOBA in which
            it attempts to quantify runs created, except that this
            stat normalizes the league average to 100''',
            'FIP': '''Fielding Independent Pitching: estimates a pitcher's
            abilities normalized for the defense playing behind him
            Takes into account home runs, walks, strikeouts, and hit by pitch
            Formula: ((13*HR)+(3*(BB+HBP))-(2*K))/IP + constant
            The constant normalizes FIP to ERA so the two can be compared
            and is usually around 3.10
             '''}

import operator
import Classes
import search_code_generator
import sqlite3

database_filename = 'all_players.db'



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
    db = sqlite3.connect(database_filename)
    c = db.cursor()
    players = {}
    for i in prefs_pos:
        players = grab_players(i, players, False, c)

    for i in prefs_pitch:
        players = grab_players(i, players, True, c)

    db.close()
    for i in players:
        a = compute_power_index(players[i], prefs_pos, prefs_pitch)
        players[i].incr_power_index(a)

    team = select_top_pos(players)
    return team


def grab_players(pref, players, pitcher, cursor):
    pref = convert_pref(pref, pitcher)
    if pitcher:
        query = """SELECT bios.name, bios.span, bios.positions, """ + pref + """, bios.player_id FROM bios
             JOIN stats_pitcher ON bios.player_id = stats_pitcher.player_id ORDER BY """ + pref + """ DESC LIMIT 80;"""
    else:
        query = """SELECT bios.name, bios.span, bios.positions, """ + pref + """, bios.player_id FROM bios
             JOIN stats_nonpitcher ON bios.player_id = stats_nonpitcher.player_id WHERE bios.positions != 'Pitcher' ORDER BY """ + pref + """ DESC LIMIT 80;"""
    r = cursor.execute(query)
    results_pos = r.fetchall()
    rank = 0
    for j in results_pos:
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
            new_player.add_years(j[1])
            new_player.add_stats(pref, j[3])
            new_player.add_rank(pref, rank)
            players[new_player.player_id] = new_player
        else:
            players[new_player.player_id].add_stats(pref, j[3])
            players[new_player.player_id].add_rank(pref, rank)
        rank += 1
    if not pitcher:
        print(players)
    return players

def convert_pref(pref, pitcher):
    if pitcher:
        return 'stats_pitcher.' + pref
    else:
        return 'stats_nonpitcher.' + pref

def apply_params(players, params):
    '''
    Sample Params:
    'Years': (1988, 2000)
    'Playoffs': True
    'All Star': False
    '''

    if params['years'] or params['Playoffs'] or params['All Star']:
        for i in players:
            if params['years']:
                player_stays = ((i.years_played[0] > params['years'][0] and 
                    i.years_played[0] < params['years'][1]) or (i.years_played[1] 
                    > params['years'][0] and i.years_played[1] < params['years'][1]))
                if not player_stays: 
                    players.remove(i)
            if params['playoffs']:
                pass

def compute_power_index(player, prefs_pos, prefs_pitch):
    power_index = 0
    for i in player.ranks:
        if i in prefs_pos:
            power_index += (100 - player.ranks[i])
        else:
            power_index += (100 - player.ranks[i])
    return power_index

def select_top_pos(pos):
    '''
    returns a dictionary 'roster' of the top players
    '''

    team = Classes.Teams()
    x = 0
    loop = 0
    print(len(pos))
    for i in pos:
        print(pos[i])
        team.add_player(pos[i])
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
    return rv / counter

def calculate_pergame_runs(team):
    '''
    '''
    runs = 0
    for position in team.roster:
        if position != 'P':
            for player in position:
                runs += player.war
    return runs * 10 / 162


def go(prefs_pos, prefs_pitch, params):
    '''
    '''
    team = create_team(prefs_pos, prefs_pitch, params)
    team.add_stat('Win Percentage', compute_wins(team.team_war))
    team.add_stat('Team Batting Average', calculate_team_stat(team, 'BA'))
    team.add_stat('Team OBP', calculate_team_stat(team, 'OBP'))
    team.add_stat('Team ERA', calculate_team_stat(team, 'ERA'))
    team.add_stat('Runs per Game', calculate_per_game_runs(team))
    return team