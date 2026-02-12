from pydantic import BaseModel

class FlagCreate(BaseModel):
    name: str
    description: str | None = None

class SettingsCreate(BaseModel):
    status: bool
    environment: str
