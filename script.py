#import sys
import paramiko

server_ip_alma='192.168.64.77'

def test(server_ip_alma):
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	client.connect(server_ip_alma, username='root', key_filename='/Users/anton1ovakhnin/.ssh/id_ed25519_test-task')
	stdin, stdout, stderr = client.exec_command("touch test2.txt")
	print(stdout.read().decode())

	client.close()


def main():
	test(server_ip_alma)


if __name__ == '__main__':
	main()