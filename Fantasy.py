#jessbritommy

#Generates a fantasy team

Stat_defs = {'ERAs': '''Earned runs allowed (per 9 innings); derived by taking
            the number of earned runs allowed, normalizing to per game by multiplying
            by 9, and then dividing by number of innings pitched''',
            'AVGs': '''Batting average: calculated by taking total number of 
            hits divided by total number of plate appearances''',
            'OBPs': '''On Base Percentage: total times reaching base divided by
            total plate appearances ''',
            'WRCs': '''Weighted Runs Created--kind of like wOBA in which
            it attempts to quantify runs created, except that this
            stat normalizes the league average to 100''',
            'FIPs': '''Fielding Independent Pitching: estimates a pitcher's
            abilities normalized for the defense playing behind him
            Takes into account home runs, walks, strikeouts, and hit by pitch
            Formula: ((13*HR)+(3*(BB+HBP))-(2*K))/IP + constant
            The constant normalizes FIP to ERA so the two can be compared
            and is usually around 3.10''',
            'SLGs': '''Slugging Percentage--derived by dividing the total number
            of bases gained (e.g. a double is 2 bases) by the total number of PAs;
            a decent proxy for power hitting ability''',
            'GSs': '''Games Started--the number of games a pitcher has started in his career''',
            'IPs': '''Innings Pitched--the number of innings a pitcher has thrown in his career''',
            'K_Pers': '''Strikeouts per 9 innings--a way to measure team-independent pitching ability''',
            'BB_Pers': '''Walks per 9 innings--a way to measure control and overall pitching ability''',
            'E_Fs': '''ERA to FIP spread--a way to measure how good or bad the team behind a pitcher
            was at fielding''',
            'UBRs': '''Measures baserunning ability--an average baserunner has an UBR of zero''',
            'WPAs': '''Measures win probability added--basically like WRC but weighted for the importance
            of each at bat in terms of how it changed its team's win probability''',
            'WARs_pitcher': '''Wins above replacement by a pitcher--derived using FIP 
            adjusted for park and innings pitched to create an estimate of how many runs better
            the pitcher has been than a replacement level minor leaguer''',
            'WARs_nonpitcher': '''Wins above replacement by a position player: take offensive,
            baserunning, and fielding runs created by a pitcher and converts them into total runs
            created above a replacement player. Converts this into a win total''',
            'Clutchs': '''Measures how much better or worse a player's performance in high stress
            environments is than his overall performance'''}

QUERY_CONSTRUCTORS = {'Pitcher': {'select_default': """SELECT bios.name, bios.span, bios.positions,
 bios.player_id, pitcher.WARs_pitcher, """,
                                   'from_default': "FROM bios JOIN pitcher ",
                                   'on_default': 'ON (bios.player_id = pitcher.player_id',
                                   'where_default': ") WHERE (bios.years_played > 2 AND pitcher.IPs > 200 AND ? != '' ",
                                    'order_by_base': ') ORDER BY ',
                                    'order_by_asc': 'ASC LIMIT 90;',
                                    'order_by_desc': 'DESC LIMIT 90;',
                                    'from_team': 'JOIN employment ',
                                    'on_team': ' AND bios.player_id = employment.player_id',
                                    'where_team': 'AND employment.team like ? ',
                                    'where_playoffs': "AND bios.Playoffs != '' ",
                                    'where_WS': "AND bios.World_Series != '' ",
                                    'where_name': "AND bios.name like ? ",
                                    'where_years': "AND (pitcher.Pitcher_Years like ? OR pitcher.Pitcher_Years like ?)"},
                        'NonPitcher': {'select_default': """SELECT bios.name, bios.span, bios.positions,
 bios.player_id, nonpitcher.WARs_nonpitcher, """,
                                   'from_default': "FROM bios JOIN nonpitcher ",
                                   'on_default': 'ON (bios.player_id = nonpitcher.player_id',
                                   'where_default': ") WHERE (bios.years_played > 2 AND nonpitcher.SLGs < .8 AND nonpitcher.AVGs < .42 AND nonpitcher.OBPs < .5 AND ? != '' ",
                                    'order_by_base': ') ORDER BY ',
                                    'order_by_asc': 'ASC LIMIT 90;',
                                    'order_by_desc': 'DESC LIMIT 90;',
                                    'from_team': 'JOIN employment ',
                                    'on_team': ' AND bios.player_id = employment.player_id',
                                    'where_team': 'AND employment.team like ? ',
                                    'where_playoffs': "AND bios.Playoffs != '' ",
                                    'where_WS': "AND bios.World_Series != '' ",
                                    'where_name': "AND bios.name like ? ",
                                    'where_years': "AND (nonpitcher.years like ? OR nonpitcher.years like ?)"}}

# CALCULATION_TYPE_DICT = {'IPs': 'Average', GS}

import operator
import Classes
import search_code_generator
import sqlite3

DATABASE_FILENAME = 'all_players.db'


def create_team(prefs_pos, prefs_pitch, params, team):

    '''
    Sample prefs:
    ['wOBA', 'OBP']
    Sample params:
    {'date': (1980, 2015), 'playoffs': True, 'all_star': True, 'current_player': False}
    '''
    db = sqlite3.connect(DATABASE_FILENAME)
    c = db.cursor()
    players = {}
    average_stats = {}
    for pref in prefs_pos:
        players = grab_players(pref, players, False, c, params)
        average_stats[pref] = calculate_league_average(pref, c, False)

    for pref in prefs_pitch:
        players = grab_players(pref, players, True, c, params)
        average_stats[pref] = calculate_league_average(pref, c, True)
    db.close()

    for key in players:
        power_index = compute_power_index(players[key], prefs_pos, prefs_pitch)
        players[key].incr_power_index(power_index)

    team = select_top_pos(players, team)
    if team.team_size < team.max_size:
        new_params = params
        if params['years']:
            new_params['years'] = ((params['years'][0] - 5), (params['years'][1] + 5))
        if params['Name']:
            new_params['Name'] = params['Name'][:-1]
        else:
            if params['Playoffs']:
                new_params['Playoffs'] = False
            if params['World_Series']:
                new_params['World_Series'] = False
            else:
                for position in team.roster:
                    team = fill_out_team(players, team, position)
                return team, average_stats
        return create_team(prefs_pos, prefs_pitch, new_params, team)
    return team, average_stats

def fill_out_team(players, team, position):
    if len(team.roster[position]) < 2 and position != 'Pitcher':
        for player in players:
            if players[player].position == position and len(team.roster[position]) == 0:
                team.roster[position] += [players[player]]
                return team
            elif players[player].position == position and team.roster[position][0].player_id != players[player].player_id:
                team.roster[position] += [players[player]]
                return team
            else:
                continue
    return team

def grab_players(pref, players, pitcher, cursor, params):
    new_pref = convert_pref(pref, pitcher)
    query, search_params = construct_query(new_pref, pitcher, params)
    if not pitcher:
        print(query, search_params)
    if len(search_params) > 0:
        print('USING PARAMS')
        r = cursor.execute(query, search_params)
    else:
        print('NOT USING')
        r = cursor.execute(query)
    results_pos = r.fetchall()
    print('LENGTH OF RESULTS', len(results_pos))
    rank = 0
    for res in results_pos:
        if 'name' in res:
            continue
        name = res[0].split()
        pos = res[2]
        first_pos = res[2]
        if len(pos.split('|')) > 1:
            first_pos = pos.split('|')[0]
            other_pos = pos.split('|')[1]
        if first_pos == 'Outfielder':
            first_pos = 'Centerfielder'
        if first_pos == 'Pinch Hitter' or first_pos == 'Pinch Runner' or first_pos == 'Designated Hitter':
            continue
        new_player = Classes.Players(name[0], name[1], first_pos, res[3])
        if new_player.player_id not in players:
            years = res[1].split('-')
            new_player.add_years(years)
            new_player.add_stats(pref, res[5])
            new_player.add_rank(pref, rank)
            new_player.add_war(res[4])
            players[new_player.player_id] = new_player
        else:
            players[new_player.player_id].add_stats(pref, res[5])
            players[new_player.player_id].add_rank(pref, rank)
        rank += 1
    return players


def convert_pref(pref, pitcher):
    if pitcher:
        return 'pitcher.' + pref
    else:
        return 'nonpitcher.' + pref


def construct_query(pref, pitcher, params):
    '''
    Structure of Params:
    {'date': (1975, 2015), 'Playoffs': True,
    'Name': 'Bob', 'Team': 'Kansas City Royals'}
    '''
    if pitcher:
        pos = 'Pitcher'
    else:
        pos = 'NonPitcher'
        
    search_params = {}
    select_statement = QUERY_CONSTRUCTORS[pos]['select_default'] + pref + " "
    from_statement = QUERY_CONSTRUCTORS[pos]['from_default']
    on_statement = QUERY_CONSTRUCTORS[pos]['on_default']
    where_statement = QUERY_CONSTRUCTORS[pos]['where_default']
    search_params['where'] = [pref]
    order_by_statement = QUERY_CONSTRUCTORS[pos]['order_by_base'] + pref + " "
    # search_params['order_by'] = [pref]

    if pref == "pitcher.ERAs" or pref == "pitcher.FIPs":
        order_by_statement += QUERY_CONSTRUCTORS[pos]['order_by_asc']
    else:
        order_by_statement += QUERY_CONSTRUCTORS[pos]['order_by_desc']

    if params['Team']:
        from_statement += QUERY_CONSTRUCTORS[pos]['from_team']
        on_statement = QUERY_CONSTRUCTORS[pos]['on_team']
        where_statement += QUERY_CONSTRUCTORS[pos]['where_team']
        if 'where' in search_params:
            search_params['where'] += ["%" + params['Team'] + "%"]
        else:
            search_params['where'] = ["%" + params['Team'] + "%"]

    if params['Playoffs']:
        where_statement += QUERY_CONSTRUCTORS[pos]['where_playoffs']

    if params['World_Series']:
        where_statement += QUERY_CONSTRUCTORS[pos]['where_WS']

    if params['Name']:
        where_statement += QUERY_CONSTRUCTORS[pos]['where_WS']
        if 'where' in search_params:
            search_params['where'] += ["%" + params['Name'] + "%"]
        else:
            search_params['where'] = ["%" + params['Name'] + "%"]

    if params['years']:
        where_statement += QUERY_CONSTRUCTORS[pos]['where_years']
        if 'where' in search_params:
            search_params['where'] += ["%" + str(params['years'][0]) + "%"]
        else:
            search_params['where'] = ["%" + str(params['years'][0]) + "%"]
        search_params['where'] += ["%" + str(params['years'][1]) + "%"]

    query = select_statement + from_statement + on_statement + where_statement + order_by_statement
    search_params = order_params(search_params)
    return query, search_params

def order_params(search_params):
    final_params = []
    if 'select' in search_params:
        for param in search_params['select']:
            final_params += [param]
    if 'where' in search_params:
        for param in search_params['where']:
            final_params += [param]
    if 'order_by' in search_params:
        for param in search_params['order_by']:
            final_params += [param]

    return final_params

def compute_power_index(player, prefs_pos, prefs_pitch):
    power_index = 0
    for rank in player.ranks:
        if rank in prefs_pos:
            power_index += ((100 - player.ranks[rank]) * (len(prefs_pos) - prefs_pos.index(rank))) * len(player.ranks) ** 6
        else:
            power_index += ((100 - player.ranks[rank]) * (len(prefs_pitch) - prefs_pitch.index(rank))) * len(player.ranks) ** 6
    return power_index


def select_top_pos(players, team):
    '''
    returns a dictionary 'roster' of the top players
    '''
    for key in players:
        team.add_player(players[key])
    return team


def calculate_team_stat(team, stat):
    rv = 0
    counter = 0
    for position in team.roster:
        for player in team.roster[position]:
            if stat in player.stats and type(player.stats[stat]) != str:
                rv += player.stats[stat]
                counter += 1
    if counter != 0:
        return round(rv / counter,3)
    else:
        return None


def calculate_pergame_runs(team):
    '''
    '''
    AVG_R_PER_PA = .11
    AVG_AB_PER_YR = 600
    player_ctr = 0
    wrc_ctr = 0
    runs = 0
    for position in team.roster:
        if position != 'Pitcher':
            for player in team.roster[position]:
                player_ctr += 1
                if 'WRCs' in player.stats:
                    wrc_ctr += 1
                    runs += player.stats['WRCs'] * AVG_R_PER_PA * AVG_AB_PER_YR / 100
    runs = runs / 162 * player_ctr / wrc_ctr
    return round(runs, 2)


def compute_wins(WAR):
    '''
    According to baseballreference.com, a zero-WAR team would be expected
    to win 32 percent of its games
    '''
    zero_win_constant = .320
    games = 162
    total_wins = zero_win_constant * games + WAR
    win_rate = total_wins / games
    games_won = win_rate * games
    win_percentage = win_rate * 100
    if games_won > 130:
        games_won = 130
        win_percentage = 13000/162
    return win_percentage, games_won

def calculate_league_average(stat, cursor, pitcher):
    results = []
    if pitcher:
        query = "SELECT SUM(pitcher." + stat + ") / COUNT(pitcher." + stat + ") FROM pitcher JOIN bios ON bios.player_id = pitcher.player_id WHERE (bios.years_played > 2 AND pitcher." + stat + " != '');"
    else:
        query = "SELECT SUM(nonpitcher." + stat + ") / COUNT(nonpitcher." + stat + ") FROM nonpitcher JOIN bios ON bios.player_id = nonpitcher.player_id WHERE (bios.years_played > 2 AND nonpitcher." + stat + " != '');"
    r = cursor.execute(query)
    for num in r.fetchall():
        results = num[0]

    return results
def go(prefs_pos, prefs_pitch, params):
    '''
    '''
    team = Classes.Teams()
    return_dict = {}
    return_dict['team'], return_dict['average_stats'] = create_team(prefs_pos, prefs_pitch, params, team)
    return_dict['win_percentage'], return_dict['games_won'] = compute_wins(team.team_war)
    if 'WRCs' in prefs_pos:
        team.add_stat('Runs per Game', calculate_pergame_runs(team))
        return_dict['runs_per'] = calculate_pergame_runs(team)
    for pref in prefs_pos:
        if 'WARs' not in pref:
            stat = calculate_team_stat(team, pref)
            team.add_stat(pref, stat)
    for pref in prefs_pitch:
        if 'WARs' not in pref:
            stat = calculate_team_stat(team, pref)
            if pref == 'BB_Pers' or pref == 'K_Pers':
                stat = str(stat) + '%'
            team.add_stat(pref, stat)
    return return_dict