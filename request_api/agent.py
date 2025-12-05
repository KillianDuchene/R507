import requests
import os
import time
import sys
import time

if len(sys.argv) < 2:
    print("Erreur: Il faut l'ID et l'URL API en arguments")
    sys.exit(1)

api_url = sys.argv[1]

print(f"Demarrage de l'agent vers {api_url}")

while True:
    try:
        hostname = os.popen("hostname").read().strip()
        os_info = os.popen("lsb_release -d").read().strip().split()[1]
        disque = os.popen("df -h /").readlines()[1].split()[1]
        memory = os.popen("free -h").readlines()[1].split()[1]
        memory_used = os.popen("free -h").readlines()[1].split()[2]
        ip = os.popen("hostname -I").read().strip()
        data = {
            "hostname": hostname,
            "disque": disque,
            "ip": ip,
            "os": os_info,
            "memory": memory,
            "memory_used": memory_used,
            "time": str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        }

        requests.post(f"{api_url}/pc", json=data)




    except Exception as e:
        print(f"Erreur de connexion : {e}")
    time.sleep(60)