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

def compile_sample_players():
    pos_list = ['C', 'P', '1B', '2B', '3B', 'SS', 'CF', 'LF', 'RF']
    name_list = ['Tommy', 'Dunn', 'Jess', 'Brianna', 'The', 'Poo', 'Baseball']
    player_list = []
    for i in range(50):
        first_name = name_list[((i ** 3) % len(name_list) + 2) % len(name_list)]
        last_name = name_list[((i ** 5) % len(name_list) + 7) % len(name_list)]
        position = pos_list[i % len(pos_list)]
        a = Classes.Players(first_name, last_name, position, (1988, 2014))
        a.add_war(i // 6)
        if a.position != 'P':
            a.add_stats('BA', .322)
            a.add_stats('OBP', .405)
        player_list += [a]
    return player_list

def other():
    pos_list = ['C', 'P', '1B', '2B', '3B', 'SS', 'CF', 'LF', 'RF']
    name_list = ['The', 'big', 'brown', 'dog', 'is', 'very', 'nice']
    player_list = []
    for i in range(50):
        first_name = name_list[((i ** 3) % len(name_list) + 2) % len(name_list)]
        last_name = name_list[((i ** 5) % len(name_list) + 7) % len(name_list)]
        position = pos_list[(i + 10) % len(pos_list)]
        a = Classes.Players(first_name, last_name, position, (1988, 2014))
        a.add_war(i // 4)
        player_list += [a]
    return player_list

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
    players = []
    for i in prefs_pos:
        players = grab_players(i, players, False, c)
        #create a list of top x player objects for a certain stat
        #if the player object already exists, make sure to use it instead of creating
        #an entirely new object
        #end result should just be a list of players for whom a certain number of stats is listed
    for i in prefs_pitch:
        players = grab_players(i, players, True, c)
        #add all the pitchers to the list
    db.close()
    for i in players:
        a = compute_power_index(i)
        i.incr_power_index(a)

    team = select_top_pos(pos)


def grab_players(pref, players, pitcher, cursor):
    if pitcher:
        query = """SELECT bios.name AND bios.span AND bios.positions AND stats_pitcher.? FROM bios
             JOIN stats_pitcher ON bios.player_id = stats_pitcher.player_id ORDER BY stats_pitcher.? DESC LIMIT 80;"""
    else:
        query = """SELECT bios.name AND bios.span AND bios.positions AND stats_nonpitcher.? FROM bios
             JOIN stats_nonpitcher ON bios.player_id = stats_nonpitcher.player_id ORDER BY stats_nonpitcher.? DESC LIMIT 80;"""
    params = [pref, pref]
    r = cursor.execute(query, params)
    results_pos = r.fetchall()
    for j in results_pos:
        name = j[0].split()
        new_player = Classes.Players(name[0], name[1], j[2])
        if new_player not in players:
            new_played.add_years(j[1])
            new_player.add_stats(pref, j[3])
            players += [new_player]
        else:
            a = players.index(new_player)
            players[a].add_stats(pref, j[3])
    return players

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
    for i in player.rankings:
        if i in prefs_pos:
            power_index += (100 - player.rankings[i]) * (49 - i ** 2)
        else:
            power_index += (100 - player.rankings[i]) * (49 - i ** 2)
    return power_index

def select_top_pos(pos):
    '''
    returns a dictionary 'roster' of the top players
    '''

    sorted_pos = sorted(pos, key = lambda player: player.power_index)
    team = Classes.Teams()
    x = 0
    loop = 0
    while team.team_size < team.max_size and loop < 4:
        team.add_player(sorted_pos[x])
        if x < len(sorted_pos) - 1:
            x += 1
        else:
            x = 0
            loop += 1
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