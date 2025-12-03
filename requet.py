from sshconnect import SSHConnection
import requests

def request_pc(id,ip) : 
    requests.post(f'http://localhost:8000/pc', json={"id": id,"hostname":"hostname","disque":"disque","os":"exos","memory":0,"memory_used":0,"ip":ip})
    ssh = SSHConnection(hostname="192.168.174.55", username="kil", password="kil")
    ssh.upload_file("agent.py", "agent.py")
    ssh.execute_command("python3 agent.py &")

request_pc(2,"192.168.174.55")
        

