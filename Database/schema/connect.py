from sqlalchemy import create_engine,text

## for returning the SQL statements we have to define the echo is true
engine=create_engine("sqlite:///Henessy-auto.db",echo=True)

with engine.connect() as connection:
    result=connection.execute(text('select "hello"'))
    print(result.all())