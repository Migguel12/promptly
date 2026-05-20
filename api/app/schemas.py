from pydantic import BaseModel
from typing import Optional

class CommandBase(BaseModel):
    name: str
    template: str
    description: Optional[str] = None
    tags: Optional[str] = None

class CommandCreate(CommandBase):
    pass

class Command(CommandBase):
    id: int

    class Config:
        from_attributes = True
