#import sys
import paramiko

ssh = '/Users/anton1ovakhnin/.ssh/id_ed25519_test-task'
user = 'root'

servers = {
	'AlmaLinux': {'ip': '192.168.64.77', 'port': '22'},
	'Debian': {'ip': '192.168.64.78', 'port': '3344'}
}

# Получение загрузки серверов
def get_load(server_ip, port):
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	try:
		client.connect(server_ip, username=user, key_filename=ssh, port=port)
		stdin, stdout, stderr = client.exec_command("uptime")
		load = stdout.read().decode().strip()
		print(f"Load on {server_ip}: '{load}'")
		return load
	
	except Exception as e:
		print(f"Falied on {server_ip}: {e}")
		return None
	
	finally:
		client.close()


		
# Выполнение команды на сервере (в качестве теста)
def command(server_ip, port):
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	try:
		client.connect(server_ip, username=user, key_filename=ssh, port=port)
		stdin, stdout, stderr = client.exec_command("ls -la")
		print(stdout.read().decode())
	
	except Exception as e:
		print(f"Failed to command on {server_ip}: {e}")
	finally:
		client.close()


# Установка PostgreSQL
def install_psql(server_ip, port):
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	try:
		client.connect(server_ip, username=user, key_filename=ssh, port=port)
		stdin, stdout, stderr = client.exec_command("cat /etc/os-release")
		os_info = stdout.read().decode().strip()

		if 'Debian' in os_info:
			stdin, stdout, stderr = client.exec_command("apt update && apt install -y postgresql")
			print(stdout.read().decode())
			print(stderr.read().decode())
	
		elif 'AlmaLinux' in os_info:
			stdin, stdout, stderr = client.exec_command("yum install -y postgresql-server postgresql-contrib")
			print(stdout.read().decode())
			print(stderr.read().decode())
		
		else:
			print(f"Unsupported OS on {server_ip}")
			return False


		client.exec_command("systemctl start postgresql")
		client.exec_command("systemctl enable postgresql")
		return True
		
	except Exception as e:
		print(f"Failed to install PostgreSQL on {server_ip}: {e}")
		return False
	
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

	if install_psql(selected_server_info['ip'], selected_server_info['port']):
		print(f"PostgreSQL installation and configuration completed. {selected_server_info['ip']}")
	else:
		print(f"Error installing PostgreSQL. {selected_server_info['ip']}")



if __name__ == '__main__':
	main()