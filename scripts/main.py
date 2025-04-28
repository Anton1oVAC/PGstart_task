import paramiko
import sys
from get_load_servers import get_load

def main():
    if len(sys.argv) != 3:
        print("Ввод: python3 script.py <server_ip1,server_ip2,...> <port1,port2,...>")
        sys.exit(1)
    
    server_ips = sys.argv[1].split(',')
    ports = sys.argv[2].split(',')
    
    if len(server_ips) != len(ports):
        print("Ошибка: Количество серверов и портов должно совпадать!")
        sys.exit(1)
    
    load_values = {}  # Словарь для хранения загрузки серверов
    for ip, port in zip(server_ips, ports):
        ip = ip.strip()
        port = int(port.strip())
        load_avg = get_load(ip, port)
        if load_avg is not None:
            load_values[ip] = load_avg  # Сохраняем загрузку сервера

    # Выбор сервера с наименьшей загрузкой
    if load_values:
        least_loaded_server = min(load_values, key=load_values.get)
        print(f"Наименее загруженный сервер: {least_loaded_server} с загрузкой {load_values[least_loaded_server]}")
    else:
        print("Не удалось получить данные о загрузке серверов.")


if __name__ == '__main__':
    main()
