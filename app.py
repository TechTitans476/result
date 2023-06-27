import os
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
  return render_template('frotend.html')


@app.route('/admissions')
def second_page():
  return render_template('admissions.html')


@app.route('/login')
def third_page():
  return render_template('login.html')


if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0')
