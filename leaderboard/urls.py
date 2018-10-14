from django.conf.urls import url
from . import views

app_name = 'leaderboard'

urlpatterns = [
    # home page
    url(r'^$', views.index, name='index'),

    # teams page
    url(r'^teams/$', views.view_teams, name='viewteams'),

    # matches page
    url(r'^matches/$', views.view_matches, name='viewmatches'),

    # leaderboard page
    url(r'^topteams/$', views.top_teams, name='topteams'),

    url(r'^registerteam/$', views.team_add_view, name='team_add'),

    url(r'^creatematch/$', views.match_add_view, name='match_add'),

    url(r'^scorecard/$', views.score_card, name='scorecard'),
]
