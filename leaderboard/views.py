from django.http import HttpResponse, Http404
from .models import Team, Match
from django.template import loader
from django.shortcuts import render
from django.db import connection
from leaderboard.forms import TeamForm, MatchForm
from django.contrib import messages


def index(request):
    # template = loader.get_template('leaderboard/index.html')
    context = {}
    # return HttpResponse(template.render(context, request))
    return render(request, 'leaderboard/index.html', context)


def team_add_view(request):
    form = TeamForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = TeamForm()
        messages.success(request, "Team Registered Successfully")

    context = {
        'form': form
    }
    return render(request, 'leaderboard/registerteam.html', context)


def match_add_view(request):
    form = MatchForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = MatchForm()
        messages.success(request, "Match Details Saved Successfully")
    context = {
        'form': form
    }
    return render(request, 'leaderboard/creatematch.html', context)


def view_teams(request):
    # template = loader.get_template('leaderboard/teamlist.html')
    try:
        all_teams = Team.objects.all()
    except Team.DoesNotExist:
        raise Http404("No Teams Registered")
    context = {
        'all_teams': all_teams
    }
    # return HttpResponse(template.render(context, request))
    return render(request, 'leaderboard/teamlist.html', context)


def view_matches(request):
    try:
        all_matches = Match.objects.all()
    except Team.DoesNotExist:
        raise Http404("No Matches Played")
    context = {
        'all_matches': all_matches
    }
    return render(request, 'leaderboard/matchlist.html', context)


def top_teams(request):
    query = """select team_name,player1,player2,team_id,win,loose,Points, DENSE_RANK() OVER (order by points desc) Rank, matches
from (
select team_name, MAX(temp_tbl.player1) player1, MAX(temp_tbl.player2) player2, MAX(temp_tbl.team_id) team_id,
MAX(win) win, MAX(loose) loose, MAX(win*4 - loose*1) Points,MAX(coalesce(win+loose,0)) matches
from
(select name as team_name, MAX(player1) player1, MAX(player2) player2, MAX(leaderboard_team.id) team_id,
coalesce(SUM((case when (team1_id=leaderboard_team.id and team1score=10) OR (team2_id=leaderboard_team.id and team2score=10)then 1 end)),0) Win,
coalesce(SUM((case when (team1_id=leaderboard_team.id and team1score!=10) OR (team2_id=leaderboard_team.id and team2score!=10) then 1 end)),0) Loose
from leaderboard_team left join leaderboard_match on team1_id = leaderboard_team.id OR team2_id = leaderboard_team.id
group by name) as temp_tbl
group by team_name) as final_tbl
order by rank asc limit 10""";
    newcursor = connection.cursor()
    newcursor.execute(query)
    tournamentResults = newcursor.fetchall()
    tournamentResults = {
        'tournamentResults': tournamentResults
    }
    return render(request, 'leaderboard/topteams.html', tournamentResults)


def score_card(request):
    query = """select team_name, MAX(temp_tbl.player1) player1, MAX(temp_tbl.player2) player2, MAX(temp_tbl.team_id) team_id,
MAX(win) win, MAX(loose) loose, MAX(win*4 - loose*1) Points, MAX(total_goals) total_goals, MAX(coalesce(win+loose,0)) matches
from
(select name as team_name, MAX(player1) player1, MAX(player2) player2, MAX(leaderboard_team.id) team_id,
coalesce(SUM(case when team1_id=leaderboard_team.id then team1score else (case when team2_id=leaderboard_team.id then team2score end) end),0) total_goals,
coalesce(SUM((case when (team1_id=leaderboard_team.id and team1score=10) OR (team2_id=leaderboard_team.id and team2score=10)then 1 end)),0) Win,
coalesce(SUM((case when (team1_id=leaderboard_team.id and team1score!=10) OR (team2_id=leaderboard_team.id and team2score!=10) then 1 end)),0) Loose
from leaderboard_team left join leaderboard_match on team1_id = leaderboard_team.id OR team2_id = leaderboard_team.id
group by name) as temp_tbl
group by team_name
order by points desc, total_goals desc""";
    newcursor = connection.cursor()
    newcursor.execute(query)
    tournamentResults = newcursor.fetchall()
    tournamentResults = {
        'tournamentResults': tournamentResults
    }
    return render(request, 'leaderboard/scorecard.html', tournamentResults)
