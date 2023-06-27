from sqlalchemy import create_engine, text
import os

database_str = os.environ['DB_CONNECTION_STRING']
engine = create_engine(database_str,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }})

with engine.connect() as conn:
  result = conn.execute(text("select * from res"))
  print(result.all())
