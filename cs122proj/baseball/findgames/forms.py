from django import forms


PLAYER_STATS = [('WARS_nonpitcher', 'Wins Above Replacement'), ('OBPs', 'On Base Percentage'), 
			('AVGs', 'Batting Average'), ('SLGs', 'Slugging percentages'),
			('UBR_WRC_Years', 'Runs created by base running'), ('UBRs', 'Base Running ability'),
			('WRCs', 'Weighted runs created'), ('WPA', 'Win probability added'),
			('Clutchs', 'Clutch hitting ability'), ('', '') 
			]
			
PITCHER_STATS = [('WARS_pitcher', 'Wins Above Replacement'), ('ERA', 'Earned Run Average'),
				('IPs', 'Innings pitched'), ('GSs', 'Games Started'), ('FIPs', 'Fielding Independent Pitching'),
				('E_Fs', 'ERA-FIP Spreads'), ('K_Pers', 'Strike outs per 9 innings'), 
				('BB_Pers', 'Walks per 9 innings'), ('', '')]


class FindGameForm(forms.Form):
    date_start = forms.CharField(label='Date start',
    							 help_text='e.g. 2010-11-09',
    							 required=False)
    date_end = forms.CharField(label='Date end',
    							 help_text='e.g. 2012-12-09',
    							 required=False)
    team1 = forms.CharField(label='Home Team',
    							 help_text='e.g. New York Yankees',
    							 required=False)
    team2 = forms.CharField(label='Away Team',
    							 help_text='e.g. Kansas City Royals',
    							 required=False)
    winner = forms.CharField(label='Winner',
    							 help_text='e.g. New York Yankees',
    							 required=False)
    runs_low = forms.CharField(label='Min  number of runs',
    							 required=False)
    runs_high = forms.CharField(label='Max number of runs',
    							 required=False)
    hits_low = forms.CharField(label='Min number of hits',
    							 required=False)
    hits_high = forms.CharField(label='Max number of hits',
    							 required=False)
    hrs_low = forms.CharField(label='Min number of home runs',
    							 required=False)
    hrs_high = forms.CharField(label='Max number of home runs',
    							 required=False)
    							 
def clean(self, value):
	date_start = self.cleaned_data.get("data_start")
	date_end = self.cleaned_data.get("data_end")
	if end_date < start_date:
		raise forms.ValidationError(_("Date end must be after date start."))
	
	return date_end
		
	


class FantasyForm(forms.Form):
	stat1 = forms.ChoiceField(label="Rank 1", choices=PLAYER_STATS, required=True, help_text="Player Stat 1")
	stat2 = forms.ChoiceField(label="Rank 2", choices=PLAYER_STATS, required=False)
	stat3 = forms.ChoiceField(label="Rank 3", choices=PLAYER_STATS, required=False)
	stat4 = forms.ChoiceField(label="Rank 4", choices=PLAYER_STATS, required=False)
	stat5 = forms.ChoiceField(label="Rank 1", choices=PITCHER_STATS, required=True)
	stat6 = forms.ChoiceField(label="Rank 2", choices=PITCHER_STATS, required=False)
	stat7 = forms.ChoiceField(label="Rank 3", choices=PITCHER_STATS, required=False)
	stat8 = forms.ChoiceField(label="Rank 4", choices=PITCHER_STATS, required=False)

class PlayerForm(forms.Form):
	player1 = forms.CharField(label="Player 1", required=True, help_text="e.g. Lorenzo Cain") 
	player2 = forms.CharField(label="Player 2", required=True, help_text="e.g. Babe Ruth")

class PitcherForm(forms.Form):
	pitcher1 = forms.CharField(label="Pitcher 1", required=True, help_text="e.g. Kevin Brown")
	pitcher2 = forms.CharField(label="Pitcher 2", required=True, help_text="e.g. Jake Arrieta")
	
