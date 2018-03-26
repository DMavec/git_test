from django.shortcuts import render, get_object_or_404
from django.http import Http404
import json

# Create your views here.
from .models import Player, Game


def index(request):
    context = {}
    return render(request, 'stats/index.html', context)


def player_stats(request, player_name):
    try:
        player = Player.objects.\
            filter(player_name__iexact=player_name).\
            add_n_ranked().\
            add_n_unranked().\
            add_player_tidy()

        q = Player.objects.\
            add_n_wins().\
            add_n_games().\
            add_pct_win().\
            add_n_ranked().\
            order_by('-pct_win').\
            add_player_tidy()

        player_summary_test = q.all()

        players = [str(qi.player_tidy) for qi in q]
        players_summary = {'player': players,
                           'n_games': [qi.n_games for qi in q],
                           'n_wins': [qi.n_wins for qi in q],
                           'n_ranked': [qi.n_ranked for qi in q],
                           'pct_wins': [float(qi.pct_win) for qi in q]}
    except Player.DoesNotExist:
        raise Http404("No Player matches the given query.")

    try:
        q = Game.objects.filter(gameplayerrelationship__player__player_name__iexact=player_name).\
            add_n_wins()

        games_summary = json.dumps({'game_id': [qi.game_id for qi in q],
                                    'n_wins': [qi.n_wins for qi in q]})

    except Game.DoesNotExist:
        raise Http404("No Game matches the given query.")

    context = {'players_summary': players_summary, 'player': player, 'players': players, 'games_summary': games_summary,
               'player_summary_test': player_summary_test}
    return render(request, 'stats/player_stats.html', context)
