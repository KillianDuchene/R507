from http.client import HTTPException
from fastapi import FastAPI
from model import PC,engine, Switch, Routeur
from sqlmodel import Session, select
from configsql import configure


app = FastAPI(on_startup=[configure])



@app.get("/routeurs")
def read_hosts() -> list[Routeur]:
    with Session(engine) as session:
        hosts = session.exec(select(Routeur)).all()
        return hosts
    
@app.post("/routeur")
def create_host(routeur: Routeur) -> Routeur:
    with Session(engine) as session:
        session.add(routeur)
        session.commit()
        session.refresh(routeur)
        return routeur
    


@app.delete("/routeur/{routeur_id}")
def delete_host(routeur_id: int) -> dict:
    with Session(engine) as session:
        host = session.get(Routeur, routeur_id)
        if not host: raise HTTPException(status_code=404, detail="Host not found")
        session.delete(host)
        session.commit()
        return {"ok": True}
    




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
    
@app.get("/name/{pc_hostname}")
def read_host_by_name(pc_hostname: str) -> list[PC]:
    with Session(engine) as session:
        hosts = session.exec(select(PC).where(PC.hostname == pc_hostname)).all()
        if not hosts: raise HTTPException(status_code=404, detail="Host not found")
        return hosts

@app.delete("/pc/{pc_id}")
def delete_host(pc_id: int) -> dict:
    with Session(engine) as session:
        host = session.get(PC, pc_id)
        if not host: raise HTTPException(status_code=404, detail="Host not found")
        session.delete(host)
        session.commit()
        return {"ok": True}
    
@app.put("/pc/{pc_id}")
def update_host(pc_id: int, updated_pc: PC) -> PC:
    with Session(engine) as session:
        host = session.get(PC, pc_id)
        if not host: raise HTTPException(status_code=404, detail="Host not found")
        host.hostname = updated_pc.hostname
        host.disque = updated_pc.disque
        host.os = updated_pc.os
        host.memory = updated_pc.memory
        session.add(host)
        session.commit()
        session.refresh(host)
        return host
    

    