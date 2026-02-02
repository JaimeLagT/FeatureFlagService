from sqlalchemy import create_engine
from sqlalchemy.orm import session, sessionmaker
from os import getenv
from sqlalchemy.ext.declarative import declarative_base

#create the database variable
#this grabs the postgreSQL username and password, host and database name
#becuase we want this to work in my mac and docker container we use os.getenv
#if it doesnt find the variable it uses the default one (2nd argument)
DATABASE_URL = getenv("DATABASE_URL","postgresql://user:password@localhost/db_name")

#here we created the connection pool
#this is done in order to not have a db handshake with every request
engine = create_engine(DATABASE_URL, echo = True)

#now that we have the engine we need a way to grab one connection
#use it for a specific request and put it back
sessionLocal = sessionmaker(autocommit = False, autoflush=False, bind = engine)

#We will create a parent class for the table object which is a python class
# these classes are special database models

base = declarative_base()

#getDb function
# Creates a new session
# yields it (hands it to the route)
# closes it when the route is done

def getDb():
    #We create a new local session
    db = sessionLocal()
    try:
        #then we hand it to the route
        yield db
    finally:
        #finally we close it
        db.close()
