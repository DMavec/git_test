from django.shortcuts import render, get_object_or_404
from django.http import Http404
import json

# Create your views here.
from .models import Player, WinRate


def index(request):
    context = {}
    return render(request, 'stats/index.html', context)


def player_stats(request, player_name):
    try:
        players = [player.player_name.lower() for player in Player.objects.all()]
    except Player.DoesNotExist:
        raise Http404("No Player matches the given query.")

    try:
        # player = player_name.lower()

        summary_stats = WinRate.objects.raw('''
                                SELECT
                                    player_name as id
                                    ,UPPER(SUBSTR(player_name, 1, 1)) || SUBSTR(player_name, 2) as player_name
                                    ,COUNT(*) as games
                                    ,SUM(CASE WHEN val = '1' THEN 1 ELSE 0 END) as wins
                                    ,(100 * SUM(CASE WHEN val = '1' THEN 1 ELSE 0 END) * 1.0) / (COUNT(*) * 1.0) as win_rate
                                FROM stats_Game games
                                INNER JOIN  stats_GamePlayerRelationship pg_lkup on
                                    pg_lkup.game_id = games.game_id and
                                    pg_lkup.player_name in({0}) and
                                    games.attr = 'game_outcome'
                                GROUP BY player_name
                                ;'''.format(','.join(['%s'] * len(players))),
                                            players)
    except WinRate.DoesNotExist:
        raise Http404("No WinRate matches the given query.")

    bar_data = json.dumps({'players': [str(summary_stat.player_name) for summary_stat in summary_stats],
                           'winrate': [str(summary_stat.win_rate) for summary_stat in summary_stats]})

    context = {'summary_stats': summary_stats, 'players': players, 'bar_data': bar_data}
    return render(request, 'stats/player_stats.html', context)
