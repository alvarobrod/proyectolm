from flask import Flask, render_template, request
import json
import requests
import os
import funciones

app = Flask(__name__)

URL_BASE_TMDB = 'https://api.themoviedb.org/3/'
language = 'es-ES'

tmdb_key = os.environ['tmdb_key']

@app.route('/')
def inicio():
	return render_template('index.html')

@app.route('/busqueda', methods = ['GET', 'POST'])
def busqueda():
	if request.method == 'GET':
		return render_template('busqueda.html', error = None)
	else:
		titulo_form = request.form['titulo']
		if titulo_form != '':
			if request.form['tipo'] == 'pelis':
				payload = {'api_key': tmdb_key, 'language': language, 'query': titulo_form, 'page': '1'}
				r = requests.get(URL_BASE_TMDB + 'search/movie', params = payload)
				if r.status_code == 200:
					js = r.json()
					lista = []
					for i in js['results']:
						lista.append({'titulo': i['title'], 'id': i['id']})
					return render_template('busqueda.html', datos = lista, error = None, tipo = request.form['tipo'])
			else:
				payload = {'api_key': tmdb_key, 'language': language, 'query': titulo_form, 'page': '1'}
				r = requests.get(URL_BASE_TMDB + 'search/tv', params = payload)
				if r.status_code == 200:
					js = r.json()
					lista = []
					for i in js['results']:
						lista.append({'titulo': i['name'], 'id': i['id']})
					return render_template('busqueda.html', datos = lista, error = None, tipo = request.form['tipo'])
		else:
			error = 'Debes introducir un título en el cuadro de búsqueda.'
			return render_template('busqueda.html', error = error)

@app.route('/busqueda/<tipo>/<code>')
def resultado(tipo, code):
	if tipo == 'pelis':
		payload = {'api_key': tmdb_key, 'language': language}
		r = requests.get(URL_BASE_TMDB + 'movie/' + code, params = payload)
		if r.status_code == 200:
			js = r.json()
			titulo = js['title']
		return render_template('resultado.html', titulo = titulo)
	else:
		payload = {'api_key': tmdb_key, 'language': language, 'movie_id': code}
		r = requests.get(URL_BASE_TMDB + 'movie/' + code, params = payload)
		if r.status_code == 200:
			js = r.json()
			titulo = js['title']
		return render_template('resultado.html', titulo = titulo)

app.run('0.0.0.0', 8080, debug = True)