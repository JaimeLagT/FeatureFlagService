#models.py is where we:
#use ORM as the translator to speak between our python classes and database
# we define our flags and flag settings

from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
#this is our flag class which inherits from our base class from database.py
class Flag(Base):
    #create a table named flags
    __tablename__ = "flags"

    # 1. The ID Column
    # primary_key=True: This is the unique ID for this row.
    # index=True:       Makes searching by ID super fast (like a book index).
    id = Column(Integer, primary_key= True, index = True)
    #2. The name Column
    #unique = True: Prevents dupes
    #index = True
    name = Column(String, unique= True, index = True)
    #3. The description column
    #nullable = True: it can be empty
    description = Column(String, nullable= True)

    #Here is where we define the relationship between flag and flag settings
    # It says: "Go find all FlagSettings where flag_id matches my id."
    settings = relationship("FlagSetting", back_populates="flag")

class FlagSetting(Base):
    #create table
    __tablename__ = "flagSettings"
    #1. The ID column
    #exactly the same as the one in Flag
    id = Column(Integer, primary_key=True, index=True)
    #2. Foreign key column
    #we add foreign key flag in order to tell the db that it must match an ID in Flags
    #nullable = False: it CANT be empty
    flagID = Column(Integer, ForeignKey("flags.id"), nullable= False)
    #3. Enable Column
    #Boolean type
    #default = false so it starts off safe
    isEnabled = Column(Boolean, default=False)
    #4 Environment column
    # nullable = false, We need to define what environment we are setting these flags for
    environment = Column(String, nullable= False)

    #Reverse relationship
    # Allows us to say: my_setting.flag -> gives us the parent Flag object
    flag = relationship("Flag", back_populates="settings")
