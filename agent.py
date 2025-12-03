import requests, os, time
while True :
    hostname= os.popen("hostname").read().strip()
    disque=os.popen("df -h /").readlines()[1].split()[1]
    exos=os.popen("lsb_release -d").read().strip().split()[1]
    memory= os.popen("free -h").readlines()[1].split()[1]
    memory_used= os.popen("free -h").readlines()[1].split()[2]
    ip = os.popen("hostname -I").read().strip().split()[0]
    print(ip)

    requests.put('http://localhost:8000/pc/2', json={"hostname":hostname,"disque":disque,"ip":ip,"os":exos,"memory":memory,"memory_used":memory_used})
    time.sleep(60)
