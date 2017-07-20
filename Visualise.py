import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.plotly as py

class Visualise(object):
    def __init__(self, data, players):
        self.data = data
        self.players = players

    def build(self):
        print(self.data)
        df = self.data

        df = (df.drop('game_id', axis=1)
                .melt(id_vars=['main_player', 'win_status'])
                .rename(columns={'value': 'player'})
                .drop('variable', axis=1)
              )



        df = df[df['player'].isin(self.players)]

        df = (df.groupby(['main_player', 'player'])
                 .agg({'win_status' : ['sum', 'count', 'mean']})
                 .reset_index()
              )

        dfs = (pd.concat([df['player'], df['main_player'], df['win_status']['sum']], axis=1)
                .pivot(index='main_player', columns='player', values='sum')
               )
        dfc = (pd.concat([df['player'], df['main_player'], df['win_status']['count']], axis=1)
                .pivot(index='main_player', columns='player', values='count')
               )
        dfm = (pd.concat([df['player'], df['main_player'], df['win_status']['mean']], axis=1)
                .pivot(index='main_player', columns='player', values='mean')
               )

        xlabs = dfm.columns.values
        xpos = np.arange(len(xlabs))
        ylabs = dfm.index.values
        ypos = np.arange(len(ylabs))
        zval = dfm

        #f = open('data/summary.csv', mode='w')
        #f.write('# of Wins\n')
        dfs.to_csv('data/summary.csv', mode='w')
        #f.write('\n\n# of Games\n')
        dfc.to_csv('data/summary.csv', mode='a')
        #f.write('\n\nWin Rate\n')
        dfm.to_csv('data/summary.csv', mode='a')

        # print(zval)
        #
        # bubbles_mpl = plt.figure()
        #
        # # doubling the width of markers
        # plt.scatter(xpos, ypos, s=zval)
        #
        # py.plot_mpl(bubbles_mpl)

        #plt.show()