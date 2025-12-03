from http.client import HTTPException
from fastapi import FastAPI
from model import PC,engine, Switch
import os
from sqlmodel import Session, select
from configsql import configure

app = FastAPI(on_startup=[configure])


@app.get("/switchs")
def read_hosts() -> list[Switch]:
    with Session(engine) as session:
        hosts = session.exec(select(Switch)).all()
        return hosts
    
@app.post("/switch")
def create_host(switch: Switch) -> Switch:
    with Session(engine) as session:
        session.add(switch)
        session.commit()
        session.refresh(switch)
        return switch
    
@app.delete("/switch/{switch_id}")
def delete_host(switch_id: int) -> dict:
    with Session(engine) as session:
        host = session.get(Switch, switch_id)
        if not host: raise HTTPException(status_code=404, detail="Host not found")
        session.delete(host)
        session.commit()
        return {"ok": True}

@app.get("/pcs")
def read_hosts() -> list[PC]:
    with Session(engine) as session:
        hosts = session.exec(select(PC)).all()
        return hosts
    
@app.get("/pc/{pc_id}")
def read_host(pc_id: int) -> PC:
    with Session(engine) as session:
        host = session.get(PC, pc_id)
        if not host: raise HTTPException(status_code=404, detail="Host not found")
        return host
    
@app.post("/pc")
def create_host(pc: PC) -> PC:
    with Session(engine) as session:
        session.add(pc)
        session.commit()
        session.refresh(pc)
        return pc
    
@app.delete("/pc/{pc_id}")
def delete_host(pc_id: int) -> dict:
    with Session(engine) as session:
        host = session.get(PC, pc_id)
        if not host: raise HTTPException(status_code=404, detail="Host not found")
        session.delete(host)
        session.commit()
        return {"ok": True}