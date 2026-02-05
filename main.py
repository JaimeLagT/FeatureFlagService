from fastapi import FastAPI, HTTPException, Depends
from database import engine, get_db
from models import Base, Flag
from schemas import FlagCreate
from sqlalchemy.orm import Session

#Create application instance
app = FastAPI()

#Define a route (the path to visit)
@app.get("/")
def health_check():
    #return a JSON response
    return {"status": "alive", "message": "Feature Flag Service is running"}

# Ensure all SQLAlchemy models have their tables created in the database
Base.metadata.create_all(bind=engine)

#Define create_flag function
#we give it our python class and transform it into an sql entry
@app.post("/flags")
def create_flag(flag : FlagCreate, db : Session = Depends(get_db)):
    #create new instance of the flag, with a name and description
    new_flag = Flag(name=flag.name, description = flag.description)
    #add the flag to the database,commit it, and refresh it to give it an ID
    db.add(new_flag)
    db.commit()
    db.refresh(new_flag)

    return new_flag

@app.get("/flags")
def read_flags(db : Session = Depends(get_db)):
    #ask data base for all flags
    flags = db.query(Flag).all()

    return flags

#TODO: dont forget