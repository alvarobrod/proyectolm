from flask import Flask, render_template, request
import json
import requests
import os
import funciones

app = Flask(__name__)

URL_BASE_TMDB = 'https://api.themoviedb.org/3/'
URL_BASE_IMAGE = 'https://image.tmdb.org/t/p/w300'
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
		if titulo_form != '' and :
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
			error = 'Por favor, introduce un texto en el cuadro de búsqueda y selecciona películas o series.'
			return render_template('busqueda.html', error = error)

@app.route('/busqueda/<tipo>/<code>')
def resultado(tipo, code):
	if tipo == 'pelis':
		payload = {'api_key': tmdb_key, 'language': language}
		r = requests.get(URL_BASE_TMDB + 'movie/' + code, params = payload)
		if r.status_code == 200:
			js = r.json()
			dic_res = {'titulo': js['title'], 'año': funciones.getaño(js['release_date']), 'rating': js['vote_average'], 'votos': js['vote_count'], 'sinopsis': js['overview'], 'generos': js['genres'], 'poster': js['poster_path']}
		return render_template('resultado.html', datos = dic_res)
	else:
		payload = {'api_key': tmdb_key, 'language': language}
		r = requests.get(URL_BASE_TMDB + 'tv/' + code, params = payload)
		if r.status_code == 200:
			js = r.json()
			titulo = js['name']
			dic_res = {'titulo': js['name'], 'año': funciones.getaño(js['first_air_date']), 'rating': js['vote_average'], 'votos': js['vote_count'], 'sinopsis': js['overview'], 'generos': js['genres'], 'poster': js['poster_path']}
		return render_template('resultado.html', datos = dic_res)

app.run('0.0.0.0', 8080, debug = True)