from flask import Flask, render_template, request
import pandas as pd
from database import engine

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


@app.route('/validate_user', methods=['POST'])
def check_user():
  user = request.form.get("email")
  password = request.form.get("password")
  #print(user, password)
  if user == "admin@gmail.com" and password == "admin@1234":
    return render_template("admin2.html")
  else:
    return render_template("login.html", k=True, user=user, password=password)


@app.route('/insert_db', methods=['POST'])
def insertintodb():
  csv_file = request.files['file']
  csv_data = pd.read_csv(csv_file)
  z = request.form.get('acyear')
  q = request.form.get('branch')
  m = request.form.get('year')
  n = request.form.get('sem')
  res1 = pd.DataFrame(csv_data)
  k = q + z + m + n
  res1.to_sql(k, engine, if_exists='replace', index=False)
  return render_template("admin2.html")


if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0')
