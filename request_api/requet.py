from sshconnect import SSHConnection
import requests
import time

MY_HOST_IP = "http://172.25.0.100:8000"

def deployer_agent(ip, port_ssh):
    #requests.post(f'http://localhost:8000/pc', json={"id": id_pc,"hostname":"hostname","disque":"disque","os":"exos","memory":0,"memory_used":0,"ip":"ip"})
    ssh = SSHConnection(hostname=ip, username="root", password="kil", port=port_ssh)
    print(ssh.upload_file("agent.py", "agent.py"))
    commande = f"nohup python3 agent.py {MY_HOST_IP} > /tmp/agent.log 2>&1 &"
    #https://stackoverflow.com/questions/73259440/nohup-python3-ends-once-i-disconnect-from-a-server
    print(ssh.execute_command(commande))

deployer_agent("172.25.0.11", 22)
deployer_agent("172.25.0.12", 22)
deployer_agent("172.25.0.13", 22)

def requet_routeur(ip, port):
    interfaces_up = {}
    interfaces_down = {}
    ssh = SSHConnection(hostname=ip, username="root", password="routerpass123", port=port)
    #lister les inerfaces cisco
    print(ssh.execute_command("vtysh -c 'show interface brief'")[0])
    a  = ssh.execute_command("vtysh -c 'show interface brief'")[0]
    for i in a.split("\n")[2:]:
        print(i)
        i.split()
        if not i : 
            continue
        interface = i.split()[0]
        status = i.split()[1]
        if len(i.split()) >3:
            ip = i.split()[3]
        else:
            ip = "pas IP"
        if status == "up":
            interfaces_up[interface] = ip
        else:
            interfaces_down[interface] = ip
    os = ssh.execute_command("vtysh -c 'show version'")[0].split()[0]
    print(os)
    memory = ssh.execute_command("free -h")[0].split()["\n"][1].split()[1]
    print(memory)
    timea = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(timea)
    print(interfaces_up)
    data = {
        "os": os,
        "memory": memory,
        "time": timea,
        "interfaces_up": interfaces_up,
        "interfaces_down": interfaces_down
    }
    requests.post(f"{MY_HOST_IP}/routeur", json=data)


while True:
    requet_routeur("172.25.0.250", 22)
    requet_routeur("172.25.0.251", 22)
    time.sleep(600)




    

