from pydantic import BaseModel

class FlagCreate(BaseModel):
    name: str
    description: str | None = None

class SettingsCreate(BaseModel):
    isEnabled: bool
    environment: str

class SettingsUpdate(BaseModel):
    update:bool