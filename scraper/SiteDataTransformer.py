import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.plotly as py
import re


class SiteDataTransformer(object):
    def __init__(self, data, players):
        self.data = data
        self.players = players

    def build(self):
        game_history = self.data

        game_history = (game_history.drop_duplicates('game_id')
                        .drop(['main_player', 'game_id'], axis=1)
                        .assign(
            players=game_history['0'] + ',' + game_history['1'] + ',' + game_history['2'] + ',' + game_history[
                '3'] + ',' + game_history['4'] + ',' +
                    game_history['5'] + ',' + game_history['6'] + ',' + game_history['7'] + ',' + game_history[
                        '8'] + ',' + game_history['9'])
                        )
        game_history = game_history[['win_status', 'players']]

        stats = []
        [[stats.append({'player1': x,
                        'player2': y,
                        'n_wins': sum(game_history['win_status'][game_history['players'].str.contains(x) & game_history[
                            'players'].str.contains(y)]),
                        'n_games': len(game_history['win_status'][
                                           game_history['players'].str.contains(x) & game_history[
                                               'players'].str.contains(y)])
                        })
          for x in self.players]
         for y in self.players]
        stats = pd.DataFrame(stats)
        stats['pct_wins'] = stats['n_wins'] / stats['n_games']

        df_wins = (stats[['player1', 'player2', 'n_wins']]
                   .pivot(index='player1', columns='player2', values='n_wins')
                   )
        df_games = (stats[['player1', 'player2', 'n_games']]
                    .pivot(index='player1', columns='player2', values='n_games')
                    )
        df_winrate = (stats[['player1', 'player2', 'pct_wins']]
                      .pivot(index='player1', columns='player2', values='pct_wins')
                      )
        df_wins.to_csv('data/summary-wins.csv', mode='w')
        df_games.to_csv('data/summary-number.csv', mode='w')
        df_winrate.to_csv('data/summary-winrate.csv', mode='w')

        # xlabs = dfm.columns.values
        # xpos = np.arange(len(xlabs))
        # ylabs = dfm.index.values
        # ypos = np.arange(len(ylabs))
        # zval = dfm
        # print(zval)
        #
        # bubbles_mpl = plt.figure()
        #
        # # doubling the width of markers
        # plt.scatter(xpos, ypos, s=zval)
        #
        # py.plot_mpl(bubbles_mpl)

        # plt.show()
