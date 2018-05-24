import requests
import os

URL_BASE_TMDB = 'https://api.themoviedb.org/3/genre/movie/list'

tmdb_key = os.environ['tmdb_key']

def formatfecha(fecha):
	return '{}/{}/{}'.format(fecha.split('-')[2], fecha.split('-')[1], fecha.split('-')[0])

def getaño(fecha):
	return fecha.split('-')[0]

def generos(lista):
	l = []
	for i in lista:
		l.append(i['name'])
	return ', '.join(l)

def temporadas(lista):
	l = []
	for i in lista:
		l.append('{} ({}), {} episodios'.format(i['name'], getaño(i['air_date']), i['episode_count']))
	return l

def quitaespacios(cadena):
	cad = cadena.replace(' ', '+')
	return cad

def tratarsinopsis(cadena):
	cad = ''
	if cadena == '':
		cad = 'No hay una sinopsis disponible.'
	else:
		cad = cadena
	return cad