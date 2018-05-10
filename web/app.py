from flask import Flask, render_template, request
import json
import requests
import os
import funciones

app = Flask(__name__)

URL_BASE_TMDB = 'https://api.themoviedb.org/3/search/'

tmdb_key = os.environ['tmdb_key']

@app.route('/')
def inicio():
	return render_template('index.html')

@app.route('/busqueda2', methods = ['GET', 'POST'])
def busqueda2():
	if request.method == 'GET':
		return render_template('busqueda2.html')

@app.route('/busqueda', methods = ['GET', 'POST'])
def busqueda():
	if request.method == 'GET':
		return render_template('busqueda.html', datos = None, error = None)
	else:
		titulo_form = request.form['titulo']
		if titulo_form != '':
			payload = {'api_key': tmdb_key, 'language': 'es-ES', 'query': titulo_form}
			r = requests.get(URL_BASE_TMDB + 'movie', params = payload)
			if r.status_code == 200:
				js = r.json()
				dic_res = {'titulo': js['results'][0]['title'], 'fecha': funciones.formatfecha(js['results'][0]['release_date']), 'generos': funciones.genero(js['results'][0]['genre_ids']), 'sinopsis': js['results'][0]['overview'], 'rating': js['results'][0]['vote_average'], 'votos': js['results'][0]['vote_count']}
			return render_template('busqueda.html', datos = dic_res, error = None)
		else:
			error = '  Debes introducir un título en el cuadro de búsqueda'
			return render_template('busqueda.html', datos = None, error = error)

app.run('0.0.0.0', 8080, debug = True)