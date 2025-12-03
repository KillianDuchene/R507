from sshconnect import SSHConnection

def request_pc() : 
    ssh = SSHConnection(hostname="192.168.174.55", username="kil", password="kil")
    ssh.upload_file("agent.py", "agent.py")
    print("file envoyer")
    print(ssh.execute_command("ls"))
    print(ssh.execute_command("python3 agent.py"))

request_pc()
        

