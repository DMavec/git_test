from django.shortcuts import render, get_object_or_404
from django.http import Http404

# Create your views here.
from .models import Player, WinRate

def index(request):
    player_list = Player.objects.all()
    context = {'player_list': player_list}
    return render(request, 'stats/index.html', context)

def player_stats(request, player_name):
    try:
        player = player_name.lower()

        win_rate = WinRate.objects.raw('''
                                SELECT
                                    player_name as id
                                    ,COUNT(*) as games
                                    ,SUM(CASE WHEN val = '1' THEN 1 ELSE 0 END) as wins
                                    ,(SUM(CASE WHEN val = '1' THEN 1 ELSE 0 END) * 1.0) / (COUNT(*) * 1.0) as win_rate
                                FROM stats_Game games
                                INNER JOIN  stats_GamePlayerRelationship pg_lkup on
                                    pg_lkup.game_id = games.game_id and
                                    pg_lkup.player_name = %s and
                                    games.attr = 'game_outcome'
                                GROUP BY player_name
                                ;''', [player])[0]

    except WinRate.DoesNotExist:
        raise Http404("No WinRate matches the given query.")

    context = {'win_rate': win_rate}
    return render(request, 'stats/player_stats.html', context)