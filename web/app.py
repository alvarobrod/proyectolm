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

@app.route('/busqueda', methods = ['GET', 'POST'])
def busqueda():
	if request.method == 'GET':
		return render_template('busqueda.html', error = None)
	else:
		titulo_form = request.form['titulo']
		if titulo_form != '':
			if request.form['tipo'] == 'pelis':
				payload = {'api_key': tmdb_key, 'language': 'es-ES', 'query': titulo_form, 'page': '1'}
				r = requests.get(URL_BASE_TMDB + 'movie', params = payload)
				if r.status_code == 200:
					js = r.json()
					lista = []
					for i in js['results']:
						lista.append({'titulo': i['title'], 'id': i['id']})
					return render_template('busqueda.html', datos = lista, error = None)
			else:
				payload = {'api_key': tmdb_key, 'language': 'es-ES', 'query': titulo_form, 'page': '1'}
				r = requests.get(URL_BASE_TMDB + 'tv', params = payload)
				if r.status_code == 200:
					js = r.json()
					lista = []
					for i in js['results']:
						lista.append({'titulo': i['name'], 'id': i['id']})
					return render_template('busqueda.html', datos = lista, error = None)
		else:
			error = '  Debes introducir un título en el cuadro de búsqueda'
			return render_template('busqueda.html', error = error)


app.run('0.0.0.0', 8080, debug = True)