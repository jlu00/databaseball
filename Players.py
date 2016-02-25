#player class


class Players:

    def __init__(self, namefirst, namelast, position, years):
        self.firstname = namefirst
        self.lastname = namelast
        self.position = position
        self.years_played = years
        self.stats = []

    def add_stats(self, stats):
        '''
        stats should be a list of tuples in the form
        [('BA', .336)]
        '''
        for i in stats:
            self.stats.append((i))
    def __repr__(self):
        str_var = '{} {} -- {}'.format(self.firstname, self.lastname, self.position)
        return str_var

class Teams:

    def __init__(self, team_name):
        self.roster = {'C': [], '1B': [], '2B': [], '3B': [], 'SS': [], 'LF': [], 'CF': [], 'RF': [], 'P': []}
        self.pos_filled = 0
        self.team_size = 0
        self.max_size = 25
        self.pitchers_needed = 8
        self.name = team_name

    def add_player(self, player):
        '''
        player is a Player object
        '''
        if self.team_size < self.max_size:
            self.team_size += 1
            if not self.roster[player.position]:
                self.pos_filled += 1
            self.roster[player.position] += [player]


    def __repr__(self):
        str_var = self.name + ': \n'
        for i in self.roster:
            str_var += i + ': '
            for j in self.roster[i]:
                str_var += j.firstname + ' ' + j.lastname + ' \n'
        return str_var