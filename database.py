from sqlalchemy import create_engine, text
import os

database_str = os.environ['DB_CONNECTION_STRING']
engine = create_engine(database_str,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }})
with engine.connect() as conn:
  query = text("select * from cse2031 where `HT No`= '20R11A0574';")
  result = conn.execute(query)
  #print(type(result))
  #print(result.all())
