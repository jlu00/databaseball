#jessbritommy

#Functions to get SQL Code

import operator
import Players
import search_code_generator

def compile_sample_players():
    pos_list = ['C', 'P', '1B', '2B', '3B', 'SS', 'CF', 'LF', 'RF']
    name_list = ['Tommy', 'Dunn', 'Jess', 'Brianna', 'The', 'Poo', 'Baseball']
    player_list = []
    for i in range(50):
        first_name = name_list[((i ** 3) % len(name_list) + 2) % len(name_list)]
        last_name = name_list[((i ** 5) % len(name_list) + 7) % len(name_list)]
        position = pos_list[i % len(pos_list)]
        player_list += [Players.Players(first_name, last_name, position, (1988, 2014))]
    return player_list
def compute_team_win_percentage(teams):
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
            
def create_team(prefs_pos, prefs_pitch, params):

    '''
    Sample prefs:
    ['wOBA', 'OBP']
    Sample params:
    {'date': (1980, 2015), 'playoffs': True, 'all_star': True, 'current_player': False}
    '''


    top_pos_list = grab_top_pos(prefs_pos, params)

    top_pitch_list = grab_top_pos(prefs_pitch, params)


def grab_top_pos(stats, time_period):
    '''
    returns the 50 historical leaders for a certain statistic
    '''
    pos_dict = {}
    for i in stats:
        #generate SQL query
        #stats_list = 
        for j in stats_list:
            if j not in rv:
                rv[j] = 0
            rv[j] += 1

    top_14_pos = select_top_pos(pos_dict)

    return top_14_pos

def grab_top_pitch(stats, params):
    '''
    returns the 50 historical leaders for a certain statistic
    '''

    rv = {}
    count = 0
    for i in stats:
        count += 1
        #generate SQL query
        for j in stats_list:
            if j not in rv:
                rv[j] = 0
            rv[j] += 50 - count
    return rv

def select_top_pos(sorted_pos):
    '''
    returns a dictionary 'roster' of the top players
    '''

    #sorted_pos = sorted(pos_dict.items(), key=operator.itemgetter(1))
    team = Players.Teams('Team')
    for i in sorted_pos:
        if not team.roster[i.position]:
            team.add_player(i)
        else:
            if decide_if_too_full(i, team):
                team.add_player(i)
    return team


def decide_if_too_full(player, team):
    slots_remaining = team.max_size - team.team_size
    positions_remaining = len(team.roster) - team.pos_filled
    return slots_remaining >= positions_remaining

