#player class


class Players:

    def __init__(self, namefirst, namelast, position):
        self.firstname = namefirst
        self.lastname = namelast
        self.position = position
        self.years_played = None
        self.stats = {}
        self.ranks = {}
        self.power_index = 0
        self.war = 0


    def add_stats(self, stat, value):
        '''
        stats should be a list of tuples in the form
        '''
        self.stats[stat] = value

    def add_war(self, war):
        self.war += war

    def add_years(self, years):
        self.years_played = years

    def add_rank(self, category, ranking):
        self.ranks[category] = ranking

    def incr_power_index(self, num):
        self.power_index += num

    def __repr__(self):
        str_var = '{} {} -- {}: {}'.format(self.firstname, self.lastname, self.position, self.power_index)
        return str_var

class Teams:

    def __init__(self):
        self.roster = {'Catcher': [], 'First Baseman': [], 'Second Baseman': 
        [], 'Designated Hitter': [], 'Third Baseman': [], 'Shortstop': [], 'Leftfielder': [], 'Centerfielder': [], 'Rightfielder': [], 'Pitcher': []}
        self.pos_filled = 0
        self.team_size = 0
        self.max_size = 25
        self.pitchers_needed = 8
        self.team_war = 0
        self.team_stats = {}
        self.total_pos = 10

    def add_player(self, player):
        '''
        player is a Player object
        '''
        if self.team_size < self.max_size:
            if player.position != 'Pitcher':
                if (self.pitchers_needed - len(self.roster['Pitcher'])) < (self.max_size - self.team_size):
                    if not self.roster[player.position]:
                        self.pos_filled += 1
                    if len(self.roster[player.position]) == 2 and self.pos_filled < self.total_pos:
                        pass
                    else:
                        self.roster[player.position] += [player]
                        self.team_size += 1
                        self.team_war += player.war
            else:
                if not self.roster['Pitcher']:
                    self.pos_filled += 1
                if len(self.roster['Pitcher']) < self.pitchers_needed:
                    self.roster['Pitcher'] += [player]
                    self.team_size += 1

    def add_stat(self, statname, value):
        self.team_stats[statname] = value

    def __repr__(self):
        str_var = ''
        for i in self.roster:
            str_var += i + ': '
            for j in self.roster[i]:
                str_var += j.firstname + ' ' + j.lastname + ' \n'
        return str_var

class PlayerContainer:

    def __init__(self):
        self.num_players = 0
        self.roster = {'C': [], '1B': [], '2B': [], '3B': [], 'SS': [], 'LF': [], 'CF': [], 'RF': [], 'P': []}

    def add_player(self, player):
        self.roster[player.position] += [player]
        self.num_players += 1

