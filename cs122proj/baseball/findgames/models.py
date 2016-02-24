from django.db import models
from django.forms import ModelForm
from django.core.validators import MaxValueValidator, MinValueValidator

class Game(models.Model):
	year = models.DateField(help_text="Enter in a year")
	winner = models.CharField(max_length=50, blank=True)
	
class Team1(models.Model):
	team1_name = models.CharField(max_length=50, blank=True, verbose_name="Team 1")
	team1_runs = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Team 1 Runs")
	team1_hits = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Team 1 Hits")
	team1_hrs = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Team 2 Homeruns")
	
	def __unicode__(self):
		return self.team1_name, self.team1_runs, self.team1_hits, self.team1_hrs
	
class Team2(models.Model):	
	team2_name = models.CharField(max_length=50, blank=True, verbose_name="Team 2")
	team2_runs = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Team 2 Runs")
	team2_hits = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Team 2 Hits")
	team2_hrs = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Team 2 Homeruns")

	def __unicode__(self):
		return self.team2_name, self.team2_runs, self.team2_hits, self.team2_hrs
		
class GameForm(ModelForm):
	class Meta:
		model = Game
		fields = ['year', 'winner']

class Team1Form(ModelForm):
	class Meta:
		model = Team1
		fields = ['team1_name', 'team1_runs', 'team1_hits', 'team1_hrs']

class Team2Form(ModelForm):
	class Meta:
		model = Team2
		fields = ['team2_name', 'team2_runs', 'team2_hits', 'team2_hrs']