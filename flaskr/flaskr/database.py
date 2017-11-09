#from sqlalchemy import create_engine
#from sqlalchemy.orm import scoped_session, sessionmaker
#from sqlalchemy.ext.declarative import declarative_base

#engine = create_engine('postgresql://gyf:123456@127.0.0.1:5432/weibodb')
#db_session = scoped_session(sessionmaker(autocommit=False,
                                         #autoflush=False,
                                         #bind=engine))

#Base = declarative_base()
#Base.query = db_session.query_property()


#def init_db():
    #import models
    #Base.metadata.create_all(bind=engine)


import psycopg2
import psycopg2.extras

try:
	conn = psycopg2.connect(host='127.0.0.1', port=5432, user='gyf',
     password='123456', database='weibodb')
except Exception as e:
	conn = psycopg2.connect(host='127.0.0.1', port=5433, user='gyf',
     password='123456', database='weibodb')

cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

