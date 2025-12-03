
from model import PC
from model import PC,engine
import os
from sqlmodel import Session, SQLModel
def pchote() :
    pcs = [
        PC(
            hostname= os.popen("hostname").read().strip(),
            disque=os.popen("df -h /").readlines()[1].split()[1],
            ip = os.popen("hostname -I").read().strip().split()[0],
            os=os.popen("lsb_release -d").read().strip().split()[1],
            memory= os.popen("free -h").readlines()[1].split()[1],
            memory_used= os.popen("free -h").readlines()[1].split()[2]
        )
        ]

    with Session(engine) as session:
        for pc in pcs:
            session.add(pc)
            session.commit()

def configure():
    if not os.path.exists("base_equipement.db"):
        SQLModel.metadata.create_all(bind=engine)
        pchote()