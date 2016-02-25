#jessbritommy

#Functions to get SQL Code

import operator
import Players
import search_code_generator


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
        stats_list = 
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

def select_top_pos(pos_dict):
    '''
    returns a dictionary 'roster' of the top players
    '''
    return_dict = {'C': [], '1B': [], '2B': [], '3B': [], 'SS': [], 'LF': [], 'CF': [], 'RF': []}

    sorted_pos = sorted(pos_dict.items(), key=operator.itemgetter(1))

    for i in sorted_pos:
