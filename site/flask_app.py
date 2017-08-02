
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import render_template
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route('/')
def hello_world():
    data = (pd.read_csv('riot_project/data/summary-winrate.csv')
              .replace(np.nan, '')
            )


    return render_template('index.html',
                            titles=['Win Rate'],
                            tables=[data.to_html(classes='table table-hover',
                                                 float_format='{:.2%}'.format,
                                                 na_rep='',
                                                 index=False)]
                            )