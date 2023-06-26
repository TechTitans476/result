from sqlalchemy import create_engine, text

database_str="mysql+pymysql://diq9icmkwg6984se3o5q:pscale_pw_rQo8Irx4oMyD4SzfrsX3DT9fYZcr1CKiTuc1Z26dzzl@aws.connect.psdb.cloud/miniproject?charset=utf8mb4"
engine = create_engine(database_str,
                      connect_args={
        "ssl": {
           "ssl_ca": "/etc/ssl/cert.pem"
        }
    })

with engine.connect() as conn:
  result=conn.execute(text("select * from res"))
  print(result.all())
