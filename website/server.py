from flask_cors import CORS
from flask import Flask, request, make_response, jsonify, render_template
from pick import *
import time

app = Flask(__name__)
CORS(app, origins=["*"])

lines = get_lines("static/desala.txt")
last_updated = time.localtime()

def get_qotd():
    with open("static/qotd.txt", "r") as f:
        qotd = f.read().strip()
    return qotd

def update_qotd():
    global lines, last_updated
    now = time.localtime()
    if last_updated.tm_yday != now.tm_yday or last_updated.tm_year != now.tm_year:
    	qotd = get_quote(lines)
    	with open("static/qotd.txt", "w") as f:
        	f.write(qotd)
    last_updated = now

@app.route('/index')
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/about")
def about():
	return render_template("about.html")

@app.route('/lines')
def lines_route():
	global lines
	response = make_response(jsonify(lines))
	return response

@app.route('/qotd')
def qotd_route():
	update_qotd()
	response = make_response(get_qotd())
	return response

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
