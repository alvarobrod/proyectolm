from flask import Flask, render_template, request
import json
import requests
import os

app = Flask(__name__)

# URL_BASE_TMDB = 

tmdb_key = os.environ['tmdb_key']

@app.route('/')
def inicio():
	return render_template('index.html')

@app.route('/busqueda', methods = ['GET', 'POST'])
def busqueda():
	if request.method == 'GET':
		return render_template('busqueda.html')
	else:
		titulo = request.form['titulo']
		return render_template('busqueda.html', titulo = titulo)

app.run('0.0.0.0', 8080, debug = True)