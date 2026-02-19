from fastapi import FastAPI, HTTPException, Depends
from database import engine, get_db
from models import Base, Flag, FlagSetting
from schemas import FlagCreate, SettingsCreate, SettingsUpdate
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

@app.post("/flags/{flagID}/settings")
def create_setting(setting: SettingsCreate ,flagID: int , db : Session = Depends(get_db)):
    #create a new instance of the setting, with a name and description
    new_setting = FlagSetting( isEnabled=setting.isEnabled, environment = setting.environment, flagID = flagID)
    #add the setting to the database, commit it, and refresh it to give it an ID
    db.add(new_setting)
    db.commit()
    db.refresh(new_setting)

    return new_setting


#Here we check if a certain flag is enabled in the provided environment
@app.get("/check/{name}")
def read_environment(name: str,  environment : str = "prod", db : Session = Depends(get_db)):
    #query data base for flag with matching name
    flag = db.query(Flag).filter(Flag.name == name).first()
    #exception for when we dont find that flag
    if flag is None:
        raise HTTPException(status_code=404, detail=f"Flag '{name}' not found")
    #query data base for setting with matching environment
    setting = db.query(FlagSetting).filter(FlagSetting.flagID == flag.id).filter(FlagSetting.environment == environment).first()
    #exception for when we dont find that environment
    if setting is None:
        return {
            "isEnabled": False,
            "message": f"Setting for environment '{environment}' not found"
        }
    #return the boolean for enabled
    return {"Flag named" : name, "environment": environment, "isEnabled": setting.isEnabled}

@app.put("/settings/{setting_id}")
def update_setting(setting_id: int, settings_data: SettingsUpdate, db : Session = Depends(get_db)):
    #fetch the setting we are looking for and update the is Enabled
    result = db.query(FlagSetting).filter(FlagSetting.id == setting_id).update({"isEnabled": settings_data.update})
    #exception for when we dont find that setting
    if result == 0:
        raise HTTPException(status_code = 404, detail= f"Flag '{setting_id}' not found")
    db.commit()

    return{
        "setting_id" : setting_id, 
        "isEnabled": settings_data.update
        }

@app.delete("/settings/{setting_id}")
def delete_setting(setting_id: int, db : Session = Depends(get_db)):
    #fetch the setting we want to delete
    result = db.query(FlagSetting).filter(FlagSetting.id == setting_id).delete()
    if result == 0:
        raise HTTPException(status_code = 404, detail= f"Flag '{setting_id}' not found")
    db.commit()
    return{
        "setting_id" : setting_id, 
        }


#add more endpoints later