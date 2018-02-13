from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Players

def index(request):
    player_list = Players.objects.all()
    context = {'player_list': player_list}
    return render(request, 'stats/index.html', context)

def player_stats(request, player_name):
    player = get_object_or_404(Players, pk=player_name)

    context = {'player':player}
    return render(request, 'stats/player_stats.html', context)