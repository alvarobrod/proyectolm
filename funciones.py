import requests
import os

URL_BASE_TMDB = 'https://api.themoviedb.org/3/genre/movie/list'

tmdb_key = os.environ['tmdb_key']

def formatfecha(fecha):
	return '{}/{}/{}'.format(fecha.split('-')[2], fecha.split('-')[1], fecha.split('-')[0])

def getaño(fecha):
	cad = ''
	if fecha == None:
		cad = '0'
	else:
		cad = fecha.split('-')[0]
	return cad

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

def estado(cadena):
	cad = ''
	if cadena == 'Returning Series':
		cad = 'En activo'
	elif cadena == 'Planned':
		cad = 'Planeada'
	elif cadena == 'In Production':
		cad = 'En producción'
	elif cadena == 'Ended':
		cad = 'Finalizada'
	elif cadena == 'Pilot':
		cad = 'Piloto'
	return cad