from fastapi import FastAPI

#Create application instance
app = FastAPI()

#Define a route (the path to visit)
@app.get("/")
def health_check():
    #return a JSON response
    return {"status": "alive", "message": "Feature Flag Service is running"}
    