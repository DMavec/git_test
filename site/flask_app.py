
# A very simple Flask Hello World app for you to get started with...

from flask import Flask

app = Flask(__name__, static_url_path = '')

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

