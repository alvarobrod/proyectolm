from flask import Flask, render_template
import json
import requests
import os

app = Flask(__name__)

# URL_BASE_TMDB = 

tmdb_key = os.environ['tmdb_key']

@app.route('/')
def inicio():
	return render_template('index.html')

@app.route('/busqueda')
def busqueda():
	return render_template('busqueda.html')

app.run('0.0.0.0', 8080, debug = True)