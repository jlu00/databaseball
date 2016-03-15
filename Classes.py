#player class


class Players:
    '''
    Players creates an object for a given player uniquely identified by 
    his player_id which was assigned when the player's stats were input
    into our SQL database. It contains attributes to carry the player's
    name, position, player_id, years_played, as well as his stats,
    ranks, and power_index and WAR. It contains methods to increment these
    attributes as well.
    '''

    def __init__(self, namefirst, namelast, position, player_id):
        self.firstname = namefirst
        self.lastname = namelast
        self.position = position
        self.player_id = player_id
        self.years_played = None
        self.stats = {}
        self.ranks = {}
        self.power_index = 0
        self.war = 0


    def add_stats(self, stat, value):
        '''
        stats should be a list of tuples in the form
        '''
        if type(value) != str:
            self.stats[stat] = value

    def add_war(self, war):
        if type(war) != str:
            self.war += war

    def add_years(self, years):
        self.years_played = years

    def add_rank(self, category, ranking):
        self.ranks[category] = ranking

    def incr_power_index(self, num):
        self.power_index += num

    def __repr__(self):
        str_var = '{} {} -- ({}, {})'.format(self.firstname, self.lastname, self.years_played[0], self.years_played[1])
        return str_var

class Teams:
    '''
    Teams is an object that contains attributes for the roster (a dict),
    the number of positions filled (out of 9), the number of people on the
    team, a max_size of 24, the number of pitchers_needed (hardcoded at 8
        because this is typical for a baseball team), a team_war statistic
    because this statistic is very important to computing some team stats,
    a team_stats attribute in dictionary form and a total_pos attribute 
    hardcoded at 9 because there are 9 total positions.
    The roster is organized as a dictionary of lists; for all positions except
    pitcher, the max number of players in a list is two to ensure that all
    positions end up with at least a player.

    '''

    def __init__(self):
        self.roster = {'Catcher': [], 'First Baseman': [], 'Second Baseman': 
        [], 'Third Baseman': [], 'Shortstop': [], 'Leftfielder': [], 'Centerfielder': [], 'Rightfielder': [], 'Pitcher': []}
        self.pos_filled = 0
        self.team_size = 0
        self.max_size = 24
        self.pitchers_needed = 8
        self.team_war = 0
        self.team_stats = {}
        self.total_pos = 9

    def add_player(self, player):
        '''
        add_player will add the inputted player to the roster assuming the
        team_size is less than max_size and there are fewer than 2 players
        for the given position. If either of these conditions is not true,
        the function instead calls look_for_player_to_replace
        '''
        if self.team_size < self.max_size:
            if player.position != 'Pitcher':
                if len(self.roster[player.position]) == 0:
                    self.incr_team(player, True)
                elif len(self.roster[player.position]) < 2:
                    if self.roster[player.position][0].player_id != player.player_id:
                        self.incr_team(player, False)
                else:
                    self.look_for_player_to_replace(player)
            else:
                if len(self.roster['Pitcher']) == 0:
                    self.incr_team(player, True)
                elif len(self.roster['Pitcher']) < self.pitchers_needed:
                    if self.player_not_added(player):
                        self.incr_team(player, False)
                    else:
                        return None
                else:
                    self.look_for_player_to_replace(player)
        else:
            self.look_for_player_to_replace(player)

    def incr_team(self, player, new_position):

        self.roster[player.position] += [player]
        self.team_war += player.war
        self.team_size += 1
        if new_position:
            self.pos_filled += 1
            

    def look_for_player_to_replace(self, player):
        '''
        look_for_player_to_replace takes in a player object and looks for
        any players that are worse than the inputted player. If it finds any,
        it replaces the found player with the inputted player, and changes the 
        team stats accordingly
        '''
        for current in self.roster[player.position]:
            if current.player_id == player.player_id:
                return None
        for current in self.roster[player.position]:
            if player.power_index > current.power_index:
                self.roster[player.position].remove(current)
                self.team_war -= current.war
                self.roster[player.position].append(player)
                self.team_war += player.war
                break

    def player_not_added(self, player):
        '''
        player_not_added ensures that the player that is being added is not
        already on the roster to avoid duplicates
        '''
        for person in self.roster[player.position]:
            if person.player_id == player.player_id:
                return False
        return True

    def add_stat(self, statname, value):
        self.team_stats[statname] = value

    def __repr__(self):
        str_var = ''
        for i in self.roster:
            str_var += " " +  str(i) + ': '
            for j in self.roster[i]:
                str_var += ' ' + str(j) + ','
        return str_var
