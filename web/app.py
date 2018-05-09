from flask import Flask, render_template, request
import json
import requests
import os

app = Flask(__name__)

URL_BASE_TMDB = 'https://api.themoviedb.org/3/search/'

tmdb_key = os.environ['tmdb_key']

@app.route('/')
def inicio():
	return render_template('index.html')

@app.route('/busqueda', methods = ['GET', 'POST'])
def busqueda():
	if request.method == 'GET':
		return render_template('busqueda.html')
	else:
		titulo_form = request.form['titulo']
		payload = {'api_key': tmdb_key, 'language': 'es-ES', 'query': titulo_form}
		r = requests.get(URL_BASE_TMDB + 'movie', params = payload)
		if r.status_code == 200:
			js = r.json()
			titulo = js['results'][0]['title']
		return render_template('busqueda.html', titulo = titulo)

app.run('0.0.0.0', 8080, debug = True)