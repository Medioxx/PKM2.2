from flask import Flask, render_template,jsonify, Response
import subprocess
import time
import flask

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/logs')
def logs():
    return render_template('logs.html')


if __name__ == "__main__":
    app.run(debug=True)
