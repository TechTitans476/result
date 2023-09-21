import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import matplotlib
import seaborn as sb

matplotlib.use('agg')


def analysis(df):
  total_fail_count = 0
  total_students = len(df) - 1
  for i in range(0, len(df)):
    fail_count = 0

    # Loop through each column (start from index 1 to skip the first column)
    for j in range(0, len(df.columns)):
      element = df.iloc[i, j]
      if element == "F":
        fail_count += 1
        break

    # Accumulate the fail count for each student to the total fail count
    total_fail_count += fail_count

  # Calculate the total number of subjects (excluding the first column)
  # Exclude the first column (student name)
  print('total_no_of_students=', len(df))
  print('total_fail_count=', total_fail_count)
  '''for i in df.iloc[0,1:len(df)-2]:
    print(i)'''
  # Calculate the fail percentage for the entire branch
  fail_percentage = (total_fail_count / (total_students)) * 100
  return (fail_percentage)


def bargraph(df):
  lst = list(df.columns)
  count_of_value1 = 0
  dict0 = {}
  genres = []

  for i in range(1, len(lst) - 1):
    count_of_value1 = 0
    count_of_value2 = 0
    if 'F' in df[lst[i]].values:
      count_of_value1 = df[lst[i]].value_counts()['F']
    if '    -' in df[lst[i]].values:
        count_of_value2 = df[lst[i]].value_counts()['    -']
    dict0[lst[i]] = {
            'tstudents': len(df) - count_of_value2,
            'fstudents': count_of_value1,
            'fail%': ((count_of_value1) / (len(df) - count_of_value2)) * 100
        }
    dict0[lst[i]]['pass%'] = 100 - dict0[lst[i]]['fail%']
    genres.append(dict0[lst[i]]['pass%'])

  subjects = list(dict0.keys())
  data = {'Subjects': subjects, 'Pass_Percentage': genres}

  plt.figure(figsize=(10, 6))
  plt.bar(subjects, genres, width=0.5)
  plt.xlabel('Subjects')
  plt.ylabel('Pass Percentage')

    # Save the plot to a BytesIO object
  buffer = BytesIO()
  plt.savefig(buffer, format='png')
  buffer.seek(0)
  plot_data = base64.b64encode(buffer.getvalue()).decode()
  plt.close()
  return plot_data
