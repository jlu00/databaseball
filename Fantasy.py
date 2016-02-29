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

import operator
import Classes
import search_code_generator

def compile_sample_players():
    pos_list = ['C', 'P', '1B', '2B', '3B', 'SS', 'CF', 'LF', 'RF']
    name_list = ['Tommy', 'Dunn', 'Jess', 'Brianna', 'The', 'Poo', 'Baseball']
    player_list = []
    for i in range(50):
        first_name = name_list[((i ** 3) % len(name_list) + 2) % len(name_list)]
        last_name = name_list[((i ** 5) % len(name_list) + 7) % len(name_list)]
        position = pos_list[i % len(pos_list)]
        player_list += [Classes.Players(first_name, last_name, position, (1988, 2014))]
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

def compute_pythag_wins(WAR):
    '''
    According to baseballreference.com, a zero-WAR team would be expected
    to win 32 percent of its games
    '''
    zero_win_constant = .320
    games = 162
    total_wins = zero_win_constant * games + WAR
    win_percentage = total_wins / games
    return win_percentage
            
def create_team(prefs_pos, prefs_pitch, params, database_filename):

    '''
    Sample prefs:
    ['wOBA', 'OBP']
    Sample params:
    {'date': (1980, 2015), 'playoffs': True, 'all_star': True, 'current_player': False}
    '''
    db = sqlite3.connect(database_filename)
    team = Classes.Teams()
    possible_players = Classes.PlayerContainer()
    for i in prefs_pos:

def select_top_pos(sorted_pos):
    '''
    returns a dictionary 'roster' of the top players
    '''

    #sorted_pos = sorted(pos_dict.items(), key=operator.itemgetter(1))
    team = Classes.Teams('Team')
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

def compare_teams(teams, stats):
    for i in stats:
        for j in teams:
            compare(j, i)

def compare(team, stat):
    for position in team.roster:
        for player in position:
            
