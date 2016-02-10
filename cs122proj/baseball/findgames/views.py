from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def index(request):
	return HttpResponse("Find any baseball game with a stat.")

def findgames(request):
	return render(request, 'findgames/findgames.html', {})

def players(request):
	return render(request, 'findgames/players.html', {})

def fantasy(request):
	return render(request, 'findgames/fantasy.html', {})


