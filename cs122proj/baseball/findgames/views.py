#The purpose of this file is to generate the views from user input.
#
#Created by Jessica Lu & Thomas Dunn.

from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponse
from django.template import loader, Context, RequestContext
from django.db import connection
import os
from findgames import forms
from findgames import find_games
from findgames import compareplayers
from findgames import fantasy_team
import sys

import sqlite3
import operator


def index(request):
    #baseball news?
    return render(request, 'findgames/index.html', {})

def stats(request):
    return render(request, 'findgames/stats.html', {})
    
def findgames(request):
    context = {}
    res = None
    form = forms.FindGameForm(request.GET or None)
    if request.method == "GET":
        form = forms.FindGameForm(request.GET) #modified from Django tutorial
        if form.is_valid():
            args = {}
            for key in form.cleaned_data:
                args[key] = form.cleaned_data[key]
            res = find_games.find_games(args) #conducts the SQL search query
        else:
            form = forms.FindGameForm()
            context['message'] = "Check your parameters!"
    else:
        form = forms.FindGameForm()
    
    if res is None:
        context['result'] = None
    else:
        columns, result = res
        context['result'] = result
        context['message'] = None
        context['num_results'] = len(result)
        context['columns'] = columns
    context['form'] = form
    
    return render(request, 'findgames/findgames.html', context)
        
def players(request):
    context = {}
    res = None
    context['message'] = None
    if request.method == "GET":
        form = forms.PlayerForm(request.GET)
        if form.is_valid():
            args = {}
            for key in form.cleaned_data:
                try:
                    args[key] = (form.cleaned_data[key]).title()
                except AttributeError:
                    continue
            res = compareplayers.compare_players(args, form.cleaned_data['pitcher'])
    else:
        form = forms.PlayerForm()
    if res is None:
        context['result'] = None
        context['message'] = None
    else:
        columns, result = res
        if len(result) <= 1:
            context['message'] = "Could not find any matches. Did you compare a player to himself?"
        else:
            context['message'] = None
            context['result'] = result
            context['columns'] = columns
            context['graphs'] = compareplayers.create_graphs(result, columns, 
                                    form.cleaned_data['pitcher'])
    context['form'] = form
    return render(request, 'findgames/players.html', context)

def fantasy(request):
    context = {}
    res = None
    roster = None
    form = forms.FantasyForm(request.GET or None)
    if request.method == "GET":
        if form.is_valid():
            args = {}
            for key in form.cleaned_data:
                args[key] = form.cleaned_data[key]
            res = fantasy_team.get_team(args, form.cleaned_data)
            roster_results = fantasy_team.get_roster(res)
    else:
        form = forms.FantasyForm()
    
    if not res:
        context['result'] = None
        context['FantTeamName'] = ""
    else:
        context['result'] = res
        context['roster_results'] = roster_results
        context['stats'] = res['team'].team_stats
        context['FantTeamName'] = form.cleaned_data['teamname']
    context['form'] = form
    return render(request, 'findgames/fantasy.html', context)