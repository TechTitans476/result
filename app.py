from flask import Flask, render_template, request, session, redirect
import pandas as pd
from database import engine, text
import os

os.urandom(24)

app = Flask(__name__)
app.secret_key = "mandy1458"


def redirect_on_reload():
  if request.endpoint != '/':
    return redirect('/')


@app.route('/')
def index():
  return render_template('frotend.html')


@app.route('/logout', methods=["GET"])
def logout():
  session.clear()  # Clear the session data
  session['logged_in'] = False
  return redirect('/')


@app.route('/result')
def resultmail():
  return render_template('resultmail.html')


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
    session['logged_in'] = True
    if 'logged_in' in session and session['logged_in']:
      return render_template('admin2.html')
    else:
      return render_template('login.html')
  else:
    return render_template("login.html", k=True, user=user, password=password)


@app.route('/showresult')
def showresult():
  return render_template("showresults.html")


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


@app.route('/result', methods=['POST'])
def retrive_data():
  rollno = request.form.get('rollno')
  rollno = rollno.toupper()
  year = request.form.get('year1')
  sem = request.form.get('sem1')
  academic_year = rollno[0:2]
  dict = {
    "05": "cse",
    "04": "ece",
    "03": "mech",
    "12": "it",
  }
  table_name = dict[rollno[6:8]] + academic_year + year + sem
  with engine.conn() as conn:
    query = text(f"select * from {table_name} where `HT No`= :val")
    result = conn.execute(query, val=rollno)
    res = dict(result.all())
  return render_template("result.html", result=res)


if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0')
