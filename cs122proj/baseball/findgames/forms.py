from django import forms

STATS = [('WRC', 'Weighted Runs Created'), ('OBP', 'On Base Percentage'), 
			('BA', 'Batting Average'), ('ERA', 'Earned Run Average'), 
			('FIP', 'Fielding Independent Pitching')]


class FindGameForm(forms.Form):
    date_start = forms.CharField(label='Date start',
    							 help_text='e.g. 2010-11-09',
    							 required=False)
    date_end = forms.CharField(label='Date end',
    							 help_text='e.g. 2012-12-09',
    							 required=False)
    team1 = forms.CharField(label='Home Team',
    							 help_text='eg New York Yankees',
    							 required=False)
    team2 = forms.CharField(label='Away Team',
    							 help_text='eg Kansas City Royals',
    							 required=False)
    winner = forms.CharField(label='Winner',
    							 help_text='eg "New York Yankees',
    							 required=False)
    runs = forms.CharField(label='Runs',
    							 required=False)
    hits = forms.CharField(label='Hits',
    							 required=False)
    hrs = forms.CharField(label='Home runs',
    							 required=False)


class FantasyForm(forms.Form):
	stat1 = forms.ChoiceField(label="Stat 1", choices=STATS, required=True)
	stat2 = forms.ChoiceField(label="Stat 2", choices=STATS, required=True)
	stat3 = forms.ChoiceField(label="Stat 3", choices=STATS, required=True)
	stat4 = forms.ChoiceField(label="Stat 4", choices=STATS, required=True)
	stat5 = forms.ChoiceField(label="Stat 5", choices=STATS, required=True)
