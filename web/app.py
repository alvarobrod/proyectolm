from Flask import Flask
import json

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('index.html')