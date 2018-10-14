from django import forms

from leaderboard.models import Team, Match


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('player1', 'player2', 'name')
        labels = {'name': 'Enter a Name ', 'player1': 'Player1 Name', 'player2': 'Player2 Name'}

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ('team1', 'team2', 'team1score', 'team2score')
        labels = {'team1': 'Team 1 Name', 'team2': 'Team 2 Name', 'team1score': 'Team 1 Score', 'team2score': 'Team 2 Score'}
