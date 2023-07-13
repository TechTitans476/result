from flask import Flask, render_template, request, session, redirect
import pandas as pd
from database import engine, retrieve_result
import os, random
from flask_mail import Mail, Message

os.urandom(24)
app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'miniproject174@gmail.com'
app.config['MAIL_PASSWORD'] = "ddojjjrjdqjqogoz"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
app.secret_key = "mandy1458"


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
  res1.to_sql(name=k, con=engine, if_exists='replace', index=False)
  return render_template("admin2.html")


@app.route('/result', methods=['POST'])
def retrive_data():
  rollno = str(session['roll'])
  rollno = rollno.upper()
  year_sem = request.form.get('button')
  dictionary = {
    "05": "cse",
    "04": "ece",
    "03": "mech",
    "12": "it",
    "69": "iot"
  }
  table_name = dictionary[rollno[6:8]] + rollno[0:2] + year_sem
  print(table_name)
  res1 = retrieve_result(table_name, rollno)
  return render_template('retrieve.html', results=res1)


def generate_otp():
  return str(random.randint(100000, 999999))


@app.route('/send-otp', methods=['GET', 'POST'])
def check_rollno():
  gmail = str(request.form.get('rollno'))
  roll = gmail.upper()
  session['roll'] = roll
  gmail = gmail.lower() + '@gcet.edu.in'
  #print(gmail)
  session['otp1'] = generate_otp()
  msg = Message(
    "OTP to view Your result",
    sender="miniproject174@gmail.com",
    recipients=[gmail],
  )
  msg.body = f"Your OTP:{session['otp1']}"
  mail.send(msg)
  return render_template("resultmail1.html", roll=roll)


@app.route('/check-otp', methods=["POST"])
def check_otp():
  roll = session['roll']
  otp2 = str(request.form.get("otp"))
  if session['otp1'] == otp2:
    return render_template("showresults.html", roll=roll)
  return render_template("resultmail1.html", k="Invalid OTP")


if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0')
