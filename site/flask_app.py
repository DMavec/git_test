
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import render_template

app = Flask(__name__, static_url_path = '')

@app.route('/')
def hello_world():
    return render_template('index.html',
                            title='Home')