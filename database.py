from sqlalchemy import create_engine, text
import os
import pandas as pd

database_str = os.environ['DB_CONNECTION_STRING']
engine = create_engine(database_str,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }})


#def retrieve_result(tablename,roll):
#table_name = "cse2031"
#rollno = "20R11A0574"
def retrieve_result(table_name, rollno):
  with engine.connect() as conn:
    query = text(f"select * from {table_name} where `HT No`= :rollno;")
    result = conn.execute(query, {"rollno": rollno})
    row = result.fetchone()  # Fetch the first row
    column_names = result.keys()  # Get the column names
    res1 = dict(zip(column_names, row))
    #print(res1)  # Create a dictionary from column names and row values
    return res1


def retrievetable(table):
  query = text(f'select * from {table} ')
  try:
    df = pd.read_sql_query(query, engine)
    return df
  except Exception as e:
    print(f'Error fetching data: {str(e)}')
    return None


def show_tables():
  with engine.connect() as conn:
    query = text("show tables")
    result = conn.execute(query)
    table_list = [row[0] for row in result]
    return (table_list[1:])
