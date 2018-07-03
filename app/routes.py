from app import app
import requests

@app.route('/')
@app.route('/index')



def index():
    return 'Hello world'
