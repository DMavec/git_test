from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.db.models import Count, Q
import json

# Create your views here.
from .models import Player, PlayerSummary, GameAttribute


def index(request):
    context = {}
    return render(request, 'stats/index.html', context)


def player_stats(request, player_name):
    try:
        players = [player.player_name.lower() for player in Player.objects.all()]
        player = Player.objects.filter(player_name__iexact=player_name).values()[0]['player_name']
    except Player.DoesNotExist:
        raise Http404("No Player matches the given query.")

    try:
        q = Player.objects.annotate(n_games=Count('gameplayerrelationship__game',
                                                 filter=Q(gameplayerrelationship__game__gameattribute__attr='game_outcome')),
                                    n_wins=Count('gameplayerrelationship__game__gameattribute',
                                                 filter=Q(gameplayerrelationship__game__gameattribute__attr='game_outcome')&
                                                        Q(gameplayerrelationship__game__gameattribute__val='1'))).\
            order_by('n_wins')
        # q = GameAttribute.objects.filter(game__gameplayerrelationship__player__player_name='diggs')
        q = json.dumps({'player': [str(qi.player_name) for qi in q],
                        'n_games': [str(qi.n_games) for qi in q],
                        'n_wins': [str(qi.n_wins) for qi in q],
                        'pct_wins': [str(round(qi.n_wins / qi.n_games, 4)) for qi in q]})

        summary_stats = PlayerSummary.objects.raw('''
                                SELECT
                                    player_name as id
                                    ,UPPER(SUBSTR(player_name, 1, 1)) || SUBSTR(player_name, 2) as player_name
                                    ,COUNT(*) as games
                                    ,SUM(CASE WHEN val = '1' THEN 1 ELSE 0 END) as wins
                                    ,(100 * SUM(CASE WHEN val = '1' THEN 1 ELSE 0 END) * 1.0) / (COUNT(*) * 1.0) as win_rate
                                FROM stats_GameAttribute games
                                INNER JOIN  stats_GamePlayerRelationship pg_lkup on
                                    pg_lkup.game_id = games.game_id and
                                    games.attr = 'game_outcome'
                                INNER JOIN stats_Player player_lkup on
                                    pg_lkup.player_id = player_lkup.id and
                                    player_lkup.player_name in({0})
                                GROUP BY player_name
                                ORDER BY win_rate DESC
                                ;'''.format(','.join(['%s'] * len(players))),
                                                  players)
    except PlayerSummary.DoesNotExist:
        raise Http404("No WinRate matches the given query.")

    bar_data = json.dumps({'players': [str(summary_stat.player_name) for summary_stat in summary_stats],
                           'winrate': [str(summary_stat.win_rate) for summary_stat in summary_stats]})

    context = {'summary_stats': summary_stats, 'players': players, 'bar_data': bar_data, 'player': player, 'q': q}
    return render(request, 'stats/player_stats.html', context)
