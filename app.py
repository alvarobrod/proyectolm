from flask import Flask, render_template, request, redirect, session
from requests_oauthlib import OAuth1
from requests_oauthlib import OAuth2Session
import json
import requests
import os
import funciones

app = Flask(__name__)
app.secret_key= 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

URL_BASE_TMDB = 'https://api.themoviedb.org/3/'
URL_BASE_SP = 'https://api.spotify.com/v1/search'
language = 'es-ES'

tmdb_key = os.environ['tmdb_key']
port = os.environ['PORT']

redirect_uri = 'https://beleflix.herokuapp.com/spotify_callback'
scope_sp = 'user-read-private user-read-email'
token_url_sp = 'https://accounts.spotify.com/api/token'

@app.route('/')
def inicio():
	return render_template('index.html')

# Spotify

def validtoken():
	try:
		token = json.loads(session['token_sp'])
	except:
		token = False
	if token:
		token_ok = True
		try:
			oauth2 = OAuth2Session(os.environ['client_id'], token=token)
			r = oauth2.get('https://api.spotify.com/v1/me')
		except TokenExpiredError as e:
			token_ok = False
	else:
		token_ok = False
	return token_ok

@app.route('/spotify')
def spotify():
	return render_template('spotify.html')

@app.route('/perfil_spotify')
def info_perfil_spotify():
	if validtoken():
		return redirect('/perfil_usuario_spotify')
	else:
		oauth2 = OAuth2Session(os.environ['client_id'], redirect_uri = redirect_uri, scope = scope_sp)
		authorization_url, state = oauth2.authorization_url('https://accounts.spotify.com/authorize')
		session.pop('token_sp', None)
		session['oauth_state_sp'] = state
		return redirect(authorization_url)

@app.route('/spotify_callback')
def get_token_spotify():
	oauth2 = OAuth2Session(os.environ['client_id'], state = session['oauth_state_sp'], redirect_uri = redirect_uri)
	token = oauth2.fetch_token(token_url_sp, client_secret = os.environ['client_secret'], authorization_response = request.url[:4] + 's' + request.url[4:])
	session['token_sp'] = json.dumps(token)
	return redirect('/perfil_usuario_spotify')

@app.route('/perfil_usuario_spotify')
def info_perfil_usuario_spotify():
	if validtoken():
		token = json.loads(session['token_sp'])
		oauth2 = OAuth2Session(os.environ['client_id'], token = token)
		r = oauth2.get('https://api.spotify.com/v1/me')
		doc = json.loads(r.content.decode('utf-8'))
		return render_template('perfil_spotify.html', datos = doc)
	else:
		return redirect('/perfil')

@app.route('/logout_spotify')
def salir_spotify():
	session.pop('token_sp', None)
	return redirect('/spotify')

# TMDB

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
					if js['total_results'] != 0:
						for i in js['results']:
							lista.append({'titulo': i['title'], 'id': i['id']})
						error = None	
					else:
						error = 'No hay resultados que mostrar. Por favor, busca de nuevo.'
					return render_template('busqueda.html', datos = lista, error = error, tipo = request.form['tipo'])
			else:
				payload = {'api_key': tmdb_key, 'language': language, 'query': titulo_form, 'page': '1'}
				r = requests.get(URL_BASE_TMDB + 'search/tv', params = payload)
				if r.status_code == 200:
					js = r.json()
					lista = []
					if js['total_results'] != 0:
						for i in js['results']:
							lista.append({'titulo': i['name'], 'id': i['id']})
						error = None
					else:
						error = 'No hay resultados que mostrar. Por favor, busca de nuevo.'
					return render_template('busqueda.html', datos = lista, error = error, tipo = request.form['tipo'])
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
			dic_res = {'titulo': js['title'], 'año': funciones.getaño(js['release_date']), 'rating': js['vote_average'], 'votos': js['vote_count'], 'sinopsis': js['overview'], \
																	  'generos': funciones.generos(js['genres']), 'poster': js['poster_path']}
			payload2 = {'api_key': tmdb_key}
			r2 = requests.get(URL_BASE_TMDB + 'movie/' + '{}/credits'.format(code), params = payload2)
			if r2.status_code == 200:
				js2 = r2.json()
				lis = []
				cast = js2['cast']
				datos_sp = {}
				if not cast:
					reparto = None
				else:
					for i in range(0, 3):
						lis.append(cast[i])
						reparto = funciones.generos(lis)
				if 'token_sp' in session:
					if validtoken():
						token = json.loads(session['token_sp'])
						oauth2 = OAuth2Session(os.environ['client_id'], token = token)
						headers = {'Accept': 'application/json', 'Content-Type': 'application-json', 'Authorization': 'Bearer ' + session['token_sp']}
						pl_sp = {'q': funciones.quitaespacios(dic_res['titulo']), 'type': 'playlist', 'limit': 1}
						r_sp = oauth2.get(URL_BASE_SP, params = pl_sp, headers = headers)
						if r_sp.status_code == 200:
							js_sp = r_sp.json()
							datos_sp = {'nombrepl': js_sp['playlists']['items'][0]['name'], 'url': js_sp['playlists']['items'][0]['external_urls']['spotify']}
				else:
					datos_sp = {'nombrepl': 'Debes iniciar sesión en Spotify para acceder a los resultados de la búsqueda', 'url': '/spotify'}
				return render_template('resultado.html', datos = dic_res, cast = reparto, tipo = tipo, datos_sp = datos_sp)
	else:
		payload = {'api_key': tmdb_key, 'language': language}
		r = requests.get(URL_BASE_TMDB + 'tv/' + code, params = payload)
		if r.status_code == 200:
			js = r.json()
			titulo = js['name']
			dic_res = {'titulo': js['name'], 'año': funciones.getaño(js['first_air_date']), 'rating': js['vote_average'], 'votos': js['vote_count'], 'sinopsis': js['overview'], \
																	 'generos': funciones.generos(js['genres']), 'poster': js['poster_path'], 'estado': js['status'], 'cadena': js['networks'][0]['name'], \
																	 'temporadas': funciones.temporadas(js['seasons'])}
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
				if 'token_sp' in session:
					if validtoken():
						token = json.loads(session['token_sp'])
						oauth2 = OAuth2Session(os.environ['client_id'], token = token)
						headers = {'Accept': 'application/json', 'Content-Type': 'application-json', 'Authorization': 'Bearer ' + session['token_sp']}
						pl_sp = {'q': funciones.quitaespacios(dic_res['titulo']), 'type': 'playlist', 'limit': 1}
						r_sp = oauth2.get(URL_BASE_SP, params = pl_sp, headers = headers)
						if r_sp.status_code == 200:
							js_sp = r_sp.json()
							datos_sp = {'nombrepl': js_sp['playlists']['items'][0]['name'], 'url': js_sp['playlists']['items'][0]['external_urls']['spotify']}
				else:
					datos_sp = {'nombrepl': 'Debes iniciar sesión en Spotify para acceder a los resultados de la búsqueda', 'url': '/spotify'}
				return render_template('resultado.html', datos = dic_res, cast = reparto, tipo = tipo, datos_sp = datos_sp)

app.run('0.0.0.0', int(port), debug = True)