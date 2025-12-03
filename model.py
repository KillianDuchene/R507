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
    disque: int
    os: str
    disque_physique: str
    memory: str

class Switch(Equipement,SQLModel, table=True) : 
    id: Optional[int] = Field(default=None, primary_key=True)
    type : str = "switch"
    memory: str
    port : int


    



    