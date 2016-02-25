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