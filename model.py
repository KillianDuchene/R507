from sqlmodel import Session, select
from sqlmodel import Field, SQLModel
from sqlmodel import SQLModel, create_engine
import os
from typing import Optional

sqlite_file_name = "base_equipement.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)


class Equipement(SQLModel, table=False) :
    id: Optional[int] = Field(default=None, primary_key=True)
    type : str


class PC(Equipement,SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hostname: str = Field(index=True)
    type : str = "PC"
    disque: str
    ip : str
    os: str
    memory: str
    memory_used: Optional[str] = None

class Switch(Equipement,SQLModel, table=True) : 
    id: Optional[int] = Field(default=None, primary_key=True)
    type : str = "Switch"
    memory: str
    port : int


    
class Routeur(Equipement,SQLModel, table=True) : 
    id: Optional[int] = Field(default=None, primary_key=True)
    type : str = "Routeur"
    memory: str


    