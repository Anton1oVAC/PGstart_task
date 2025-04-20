#import sys
import paramiko

servers = {
	'alma': {'ip': '192.168.64.77', 'port': '22'},
	'debian': {'ip': '192.168.64.78', 'port': '3344'}
}

# Получение загрузки серверов
def get_load(server_ip, port):
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	try:
		client.connect(server_ip, username='root', key_filename='/Users/anton1ovakhnin/.ssh/id_ed25519_test-task', port=port)
		stdin, stdout, stderr = client.exec_command("uptime")
		load = stdout.read().decode().strip()
		print(f"Load on {server_ip}: '{load}'")
		
		return load
	
	except Exception as e:
		print(f"Falied on {server_ip}: {e}")
		
		return None
	
	finally:
		client.close()
    		
		
# Выполнение команды
def command(server_ip, port):
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	try:
		client.connect(server_ip, username='root', key_filename='/Users/anton1ovakhnin/.ssh/id_ed25519_test-task', port=port)
		stdin, stdout, stderr = client.exec_command("ls -la")
		print(stdout.read().decode())
	except Exception as e:
		print(f"Failed to command on {server_ip}: {e}")
	finally:
		client.close()


def main():
	load_values = {}

	for name, info in servers.items():
		load = get_load(info['ip'], info['port'])
		if load:
			load_avg = load.split()[-1].strip().split(",") # посл. зн. загрузки
			load_values[name] = [float(x.strip()) for x in load_avg]
	
	# выбираю нагрузку и выб. наим.серв.
	least_loaded_server = min(load_values, key=lambda k: sum(load_values[k]))
	print(f"Least loaded server: {least_loaded_server} with load {load_values[least_loaded_server]}")

	selected_server_info = servers[least_loaded_server]
	command(selected_server_info['ip'], selected_server_info['port'])


if __name__ == '__main__':
	main()