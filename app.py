from flask import Flask, render_template, request, flash, session, redirect, url_for, Response

import pandas as pd
from database import *
import os, random
from flask_mail import Mail, Message
import matplotlib.pyplot as plt
import matplotlib
import base64
from io import BytesIO
from analysis import bargraph, analysis
#from flask_weasyprint import HTML, CSS

secretkey = os.urandom(24)
app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'miniproject174@gmail.com'
app.config['MAIL_PASSWORD'] = "ddojjjrjdqjqogoz"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
app.secret_key = secretkey

#dict_global = {}


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


@app.route('/adminpage')
def adminpage():
  return render_template("adminfrontend.html")


@app.route('/adminn')
def adminn():
  return render_template("admin2.html")


@app.route('/admin4')
def admin4():
  render_template("admin4.html")


@app.route('/validate_user', methods=['POST'])
def check_user():
  user = request.form.get("email")
  password = request.form.get("password")
  #print(user, password)
  if user == "admin@gmail.com" and password == "admin@1234":
    session['logged_in'] = True
    if 'logged_in' in session and session['logged_in']:
      return render_template('adminfrontend.html')
    else:
      return render_template('login.html')
  else:
    return render_template("login.html", k=True, user=user, password=password)


@app.route('/showresult')
def showresult():
  roll = session['roll']
  return render_template("showresults.html", roll=roll)


@app.route('/insert_db', methods=['POST'])
def insertintodb():
  csv_file = request.files['file']
  csv_data = pd.read_csv(csv_file)
  z = request.form.get('acyear')
  q = request.form.get('branch')
  q = q.lower()
  m = request.form.get('year')
  n = request.form.get('sem')
  res1 = pd.DataFrame(csv_data)
  session['file'] = res1
  k = q + z + m + n
  data_list = res1.to_dict(orient='records')
  session['file'] = data_list
  res1.to_sql(name=k, con=engine, if_exists='replace', index=False)
  return '''
    <script>
      alert('File uploaded successfully!');
      window.location.href = "{0}";
    </script>
     '''.format(url_for('adminpage'))


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
    "69": "iot",
    "62": "cs",
    "67": "ds"
  }
  table_name = dictionary[rollno[6:8]] + rollno[0:2] + year_sem
  print(table_name)
  res1 = retrieve_result(table_name, rollno)
  print(type(res1))
  print(res1)
  session['dict_global'] = res1
  print(session['dict_global'])
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


@app.route('/admissionpage')
def admissionpage():
  return render_template("admissions.html")


@app.route('/admission', methods=['POST'])
def add_details():
  # Retrieve form data
  first_name = request.form.get('firstname')
  last_name = request.form.get('lastname')
  f_name = request.form.get('fname')
  email = request.form.get('email')
  add = request.form.get('address')
  branch = request.form.get('branch')
  year = request.form.get('year')
  ph_num = request.form.get('phnum')

  # Create the SQL query to insert data into the admissions table
  sql_query = text(
    "INSERT INTO admissions (first_name, last_name, f_name, email, address, branch, year, ph_num) "
    "VALUES (:first_name, :last_name, :f_name, :email, :address, :branch, :year, :ph_num)"
  )

  # Create a connection to the database
  conn = engine.connect()

  # Execute the query with the form data as parameters
  conn.execute(sql_query,
               first_name=first_name,
               last_name=last_name,
               f_name=f_name,
               email=email,
               address=add,
               branch=branch,
               year=year,
               ph_num=ph_num)

  # Close the database connection
  conn.close()
  return ''' 
        <script>
        alert('Application Submitted Successfully');
         window.location.href = "{0}";
    </script>
    '''.format(url_for('admissionpage'))


@app.route('/data')
def data():
  return render_template('dataanalysis.html')


def showanalysis(df):
  matplotlib.use('agg')


def generate_pie_chart(fail_percent):
  labels = ['Fail Percentage', 'Pass Percentage']
  pass_percent = 100 - fail_percent
  sizes = [fail_percent, pass_percent]
  colors = ['green', 'orange']
  explode = (0.1, 0
             )  # To create some separation for the 'Fail Percentage' slice

  plt.pie(sizes,
          explode=explode,
          labels=labels,
          colors=colors,
          autopct='%1.4f%%',
          shadow=True,
          startangle=140)
  # Equal aspect ratio ensures that pie is drawn as a circle.
  plt.title('Data Analysis')

  # Save the plot as an image
  buffer = BytesIO()
  plt.savefig(buffer, format='png')
  buffer.seek(0)
  plot_data = base64.b64encode(buffer.getvalue()).decode()

  # Close the plot to release resources
  plt.close()

  return plot_data


@app.route('/submitform', methods=['POST'])
def submitform():
  year = request.form.get('year')
  branch = request.form.get('branch')
  acyear = request.form.get('acyear')
  sem = request.form.get('sem')
  print(year, branch, acyear, sem)
  # Check if any of the values is None
  if None in [year, branch, acyear, sem]:
    return '''
            <script>
            alert('Please select all values!');
            window.location.href = "{0}";
            </script>
            '''.format(url_for('data'))

  results = show_tables()
  table = branch + acyear + year + sem

  if table not in results:
    return '''
            <script>
            alert('Table doesn't exist!');
            window.location.href = "{0}";
            </script>
            '''.format(url_for('data'))

  df = retrievetable(table)
  if df is not None:
    fail_percentage = analysis(df)
    print(fail_percentage)
  else:
    print('Error fetching data.')

  plot_data = generate_pie_chart(fail_percentage)
  print(df)
  bargraph1 = bargraph(df)
  return render_template('chart.html', plot_data=plot_data, bar=bargraph1)


@app.route('/data1')
def data1():
  return render_template('dataanalysis1.html')


@app.route('/send_email', methods=['POST'])
def send_email():
  recipient_email = "miniproject174@gmail.com"

  # Create a message with subject and recipients
  subject = 'Data Analysis  '
  recipients = [recipient_email]
  message = Message(subject=subject, recipients=recipients)

  # Add HTML content to the email
  message.html = render_template('chart.html')

  try:
    # Send the email
    mail.send("hi")
    msg = "msg sent successfully"
    return render_template('chart.html', msg=msg)
  except Exception as e:
    flash(f'Email could not be sent. Error: {str(e)}', 'danger')

  return render_template('chart.html')


if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0')
