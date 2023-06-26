from sqlalchemy import create_engine, text

db_connection_string="mysql+pymysql://ed5q3vbg2vif2mrtojmv:pscale_pw_rU4taBBLna4n9FWtgxVHxPjGMLhCIczEiMMghDhHn5n@aws.connect.psdb.cloud/miniproject?charset=utf8mb4"
engine = create_engine(db_connection_string,connect_args={
        "ssl": {
            "ssl_ca": "/etc/ssl/cert.pem"
        }
    })
with engine.connect() as conn:
  result=conn.execute(text("select * from res"))
  print(result.all())
