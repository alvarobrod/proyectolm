from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/')
def inicio():
	return render_template('index.html')

@app.route('/busqueda')
def busqueda():
	return render_template('busqueda.html')

app.run('0.0.0.0', 8080, debug = True)