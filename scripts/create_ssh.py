import paramiko
from config import ssh_key, user

# Подключение к серверам по ssh
def create_ssh_client(server_ip, port):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server_ip, username=user, key_filename=ssh_key, port=port)
    
    return client