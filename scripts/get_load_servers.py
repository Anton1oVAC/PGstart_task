import paramiko
from create_ssh import create_ssh_client

# Получение загрузки сервера
def get_load(server_ip, port):
    client = create_ssh_client(server_ip, port)

    try:
        stdin, stdout, stderr = client.exec_command("uptime")
        load = stdout.read().decode().strip()
        load_avg = float(load.split()[-3].rstrip(','))
        print(f"Load on {server_ip}: '{load_avg}'")
        return load_avg
    
    except Exception as e:
        print(f"Не удалось подключиться к {server_ip}: {e}")
        return None
    
    finally:
        client.close()