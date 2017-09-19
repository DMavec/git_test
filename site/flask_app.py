
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import render_template
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route('/')
def hello_world():
    wins = (pd.read_csv('riot_project/data/summary-winrate.csv')
              .replace(np.nan, '')
            )

    games = (pd.read_csv('riot_project/data/summary-number.csv')
               .replace(np.nan, '')
            )



    def highlight_max(s):
        #is_max = s == max(s)
        #return ['background-color: yellow' if v else '' for v in is_max]
        return ['background-colour: yellow' for x in s]

    s = (games.style
              .background_gradient())


    return render_template('index.html',
                            titles=['Win Rate', 'Number of Games'],
                            tables=[wins.to_html(classes='table table-hover',
                                                 float_format='{:.2%}'.format,
                                                 index=False),
                                    games.to_html(classes='table table-hover',
                                                 index=False)]
                                    #s.render()]
                            )