import requests, os
hostname= os.popen("hostname").read().strip()
disque=os.popen("df -h /").readlines()[1].split()[1]
exos=os.popen("lsb_release -d").read().strip().split()[1]
memory= os.popen("free -h").readlines()[1].split()[1]


requests.put('http://localhost:8000/pc/2', json={"hostname":hostname,"disque":disque,"os":exos,"memory":memory})
print("element envoyer")