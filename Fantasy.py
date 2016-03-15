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
                                   'from_default': "FROM bios JOIN pitcher",
                                   'on_default': ' ON (bios.player_id = pitcher.player_id',
                                   'where_default_1': ") WHERE (bios.years_played > 2 AND pitcher.IPs > 200 AND ",
                                    'where_default_2': " != '' ",
                                    'order_by_base': ') ORDER BY ',
                                    'order_by_asc': 'ASC LIMIT 90;',
                                    'order_by_desc': 'DESC LIMIT 90;',
                                    'from_team': ' JOIN employment',
                                    'on_team': ' AND bios.player_id = employment.player_id',
                                    'where_team': 'AND employment.teams like ? ',
                                    'where_playoffs': "AND bios.Playoffs != '' ",
                                    'where_WS': "AND bios.World_Series != '' ",
                                    'where_name': "AND bios.name like ? ",
                                    'where_years': "AND (pitcher.Pitcher_Years like ? OR pitcher.Pitcher_Years like ?)"},
                        'NonPitcher': {'select_default': """SELECT bios.name, bios.span, bios.positions,
 bios.player_id, nonpitcher.WARs_nonpitcher, """,
                                   'from_default': "FROM bios JOIN nonpitcher",
                                   'on_default': ' ON (bios.player_id = nonpitcher.player_id',
                                   'where_default_1': ") WHERE (bios.years_played > 2 AND nonpitcher.SLGs < .8 AND nonpitcher.AVGs < .42 AND nonpitcher.OBPs < .5 AND ",
                                    'where_default_2': " != '' ",
                                    'order_by_base': ') ORDER BY ',
                                    'order_by_asc': 'ASC LIMIT 90;',
                                    'order_by_desc': 'DESC LIMIT 90;',
                                    'from_team': ' JOIN employment',
                                    'on_team': ' AND bios.player_id = employment.player_id',
                                    'where_team': 'AND employment.teams like ? ',
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
    Inputs:
    prefs_pos: stats from user for position players, ordered by preference
    prefs_pitch: stats from user for pitchers, ordered by preference
    params: limiting parameters (teams, years, names, whether a player played
        in the playoffs, whether a player played in the world series)
    team: a Teams object created by the go function
    Outputs: A team filled with player objects, and a dictionary of average_stats
    for each stat that the player input
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
    '''
    Inputs:
    players: the list of player objects that have been created from SQL searches
    team: the team object
    position: the position that we are trying to fill in
    Outputs:
    team with more players filled into the position the function tried to fill in
    if any were found
    '''
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
    '''
    Inputs:
    pref: the preference upon which the players will be ranked
    players: a list of players that have been pulled from previous searches
    pitcher: whether or not the preference we are dealing with is from prefs_pitch
    params: limiting parameters (teams, years, names, whether a player played
        in the playoffs, whether a player played in the world series)
    Outputs: a list of players with any new players added and stats for pref 
    added
    '''
    new_pref = convert_pref(pref, pitcher)
    query, search_params = construct_query(new_pref, pitcher, params)
    if len(search_params) > 0:
        r = cursor.execute(query, search_params)
    else:
        r = cursor.execute(query)
    results_pos = r.fetchall()
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
    '''
    Inputs:
    pref: the preference being selected for
    pitcher: whether or not the pref is from prefs_pitch
    Outputs:
    pref converted to be usable in a SQL query
    '''
    if pitcher:
        return 'pitcher.' + pref
    else:
        return 'nonpitcher.' + pref


def construct_query(pref, pitcher, params):
    '''
    Inputs:
    pref: preference being selected
    pitcher: whether or not pref is from prefs_pitch
    params: limiting parameters (teams, years, names, whether a player played
        in the playoffs, whether a player played in the world series)
    Outputs:
    a SQL query along with search_params, a list of parameterized terms,
    if any are needed
    '''
    if pitcher:
        pos = 'Pitcher'
    else:
        pos = 'NonPitcher'
        
    search_params = {}
    select_statement = QUERY_CONSTRUCTORS[pos]['select_default'] + pref + " "
    from_statement = QUERY_CONSTRUCTORS[pos]['from_default']
    on_statement = QUERY_CONSTRUCTORS[pos]['on_default']
    where_statement = QUERY_CONSTRUCTORS[pos]['where_default_1'] + pref + QUERY_CONSTRUCTORS[pos]['where_default_2']
    order_by_statement = QUERY_CONSTRUCTORS[pos]['order_by_base'] + pref + " "
    # search_params['order_by'] = [pref]

    if pref == "pitcher.ERAs" or pref == "pitcher.FIPs":
        order_by_statement += QUERY_CONSTRUCTORS[pos]['order_by_asc']
    else:
        order_by_statement += QUERY_CONSTRUCTORS[pos]['order_by_desc']

    if params['Team']:
        from_statement += QUERY_CONSTRUCTORS[pos]['from_team']
        on_statement += QUERY_CONSTRUCTORS[pos]['on_team']
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
        where_statement += QUERY_CONSTRUCTORS[pos]['where_name']
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
    '''
    Inputs:
    search_params: a dictionary with parameters listed for 
    'where', 'select', and 'order_by'
    Outputs:
    final_params, an ordered list of the params in the correct order
    to be used in a SQL query
    '''
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
    '''
    Inputs:
    player: a player object
    prefs_pos: the position player preferences
    prefs_pitch: the pitcher preferences
    Outputs:
    power_index, a number based on the rank the player has in each statistic,
    multiplied by the number of statistics he has to the 6th power--I wanted
    to give extra weight to players who appeared in the top 90 list multiple times
    or else a player who was #1` in one category and didn't appear in any others could
    beat out a person who was 70 in all categories listed
    '''
    power_index = 0
    for rank in player.ranks:
        if rank in prefs_pos:
            power_index += ((100 - player.ranks[rank]) * (len(prefs_pos) - prefs_pos.index(rank))) * len(player.ranks) ** 6
        else:
            power_index += ((100 - player.ranks[rank]) * (len(prefs_pitch) - prefs_pitch.index(rank))) * len(player.ranks) ** 6
    return power_index


def select_top_pos(players, team):
    '''
    Inputs:
    players: list of Players objects
    team: Teams object
    Calls the add_player function for team
    Outputs: 
    team filled in with the best possible players
    '''

    for key in players:
        team.add_player(players[key])
    return team


def calculate_team_stat(team, stat):
    '''
    Inputs:
    team: Teams object
    stat: stat for which we are calculating the average
    Outputs:
    returns the average for the team on a certain stat
    for all players who have that stat
    '''
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
    Inputs:
    team: a Teams object with players already filled in
    Outputs: a pergame run total based on a formula I derived using
    the definition of WRC and the average runs per PA for an average hitter
    (i.e. one with a WRC of 100)
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
                    print('WRCs')
                    wrc_ctr += 1
                    runs += player.stats['WRCs'] * AVG_R_PER_PA * AVG_AB_PER_YR / 100
    print(runs)
    runs = runs / 162 * player_ctr / wrc_ctr
    return round(runs, 2)


def compute_wins(WAR):
    '''
    Inputs:
    WAR: a team's WAR total
    Outputs: a win percentage and hypothetical win total for a 162-game season
    calculated using a formula that applies a baseline win percentage to a 0-win
    team
    In the case of a team that won over 130 games, I capped their win total at that 
    because anything higher than that would be extremely unrealistic 
    The reason that sometimes the formula shows teams as winning that many games 
    is there has never been a team even close to as good as some of the teams you
    can create using our algorithm, so the team WAR totals get a little unrealistic
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
    '''
    Inputs:
    stat: the stat for which the league average is being calculated
    cursor: a sqlite3 cursor object
    pitcher: whether or not the stat is a pitcher statistic
    Outputs:
    Average league stat

    '''
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
    Inputs:
    prefs_pos: position preferences input by user
    prefs_pitch: pitcher preferences input by user
    params: limiting parameters (teams, years, names, whether a player played
        in the playoffs, whether a player played in the world series)
    Outputs:
    a dictionary with entries including the team object, the average stats for
    all stats queried, and win percentage and games won for the team
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