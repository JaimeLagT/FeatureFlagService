from fastapi import FastAPI
from database import engine
from models import Base

#Create application instance
app = FastAPI()

#Define a route (the path to visit)
@app.get("/")
def health_check():
    #return a JSON response
    return {"status": "alive", "message": "Feature Flag Service is running"}

Base.metadata.create_all(bind=engine)