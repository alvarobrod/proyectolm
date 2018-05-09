import requests
import os

URL_BASE_TMDB = 'https://api.themoviedb.org/3/genre/movie/list'

tmdb_key = os.environ['tmdb_key']

def formathora(hora):
	return '{}/{}/{}'.format(hora.split('-')[2], hora.split('-')[1], hora.split('-')[0])

def genero(lista):
	payload = {'api_key': tmdb_key, 'language': 'es-ES'}
	r = requests.get(URL_BASE_TMDB, params = payload)
	if r.status_code == 200:
		js = r.json()
		l = []
		generos = js['genres']
		for i in lista:
			for elem in generos:
				if i == elem['id']:
					l.append(elem['name'])
		return l
	else:
		return 0