from flask import Flask, render_template, request
import json
import requests
import os
import funciones

app = Flask(__name__)

URL_BASE_TMDB = 'https://api.themoviedb.org/3/'
language = 'es-ES'

tmdb_key = os.environ['tmdb_key']
port = os.environ["PORT"]

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
			dic_res = {'titulo': js['title'], 'año': funciones.getaño(js['release_date']), 'rating': js['vote_average'], 'votos': js['vote_count'], 'sinopsis': js['overview'], 'generos': funciones.generos(js['genres']), 'poster': js['poster_path']}
			payload2 = {'api_key': tmdb_key}
			r2 = requests.get(URL_BASE_TMDB + 'movie/' + '{}/credits'.format(code), params = payload2)
			if r2.status_code == 200:
				js2 = r2.json()
				lis = []
				cast = js2['cast']
				if not cast:
					reparto = None
				else:
					for i in range(0, 3):
						lis.append(cast[i])
						reparto = funciones.generos(lis)
				return render_template('resultado.html', datos = dic_res, cast = reparto, tipo = tipo)
	else:
		payload = {'api_key': tmdb_key, 'language': language}
		r = requests.get(URL_BASE_TMDB + 'tv/' + code, params = payload)
		if r.status_code == 200:
			js = r.json()
			titulo = js['name']
			dic_res = {'titulo': js['name'], 'año': funciones.getaño(js['first_air_date']), 'rating': js['vote_average'], 'votos': js['vote_count'], 'sinopsis': js['overview'], 'generos': funciones.generos(js['genres']), 'poster': js['poster_path'], 'estado': js['status'], 'cadena': js['networks'][0]['name']}
			payload2 = {'api_key': tmdb_key}
			r2 = requests.get(URL_BASE_TMDB + 'tv/' + '{}/credits'.format(code), params = payload2)
			if r2.status_code == 200:
				js2 = r2.json()
				lis = []
				cast = js2['cast']
				if not cast:
					reparto = None
				else:
					for i in range(0, 3):
						lis.append(cast[i])
						reparto = funciones.generos(lis)
				return render_template('resultado.html', datos = dic_res, cast = reparto, tipo = tipo)

app.run('0.0.0.0', int(port), debug=True)