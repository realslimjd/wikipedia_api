'''
Many thanks to https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
without which I would not have been able to complete this project (in Python)
'''
from flask import Flask

app = Flask(__name__)

from app import routes
