import os
import PySimpleGUI as sg
import socket


def findIp():
    import subprocess
    try:
        arp_output = subprocess.check_output(['arp', '-a'], universal_newlines=True)
    except subprocess.CalledProcessError as e:
        arp_output = ''
    lines = arp_output.strip().split('\n')
    ip_addresses = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) == 3 and parts[2].lower() == "dynamic":
            ip_address = parts[0]
            ip_addresses.append(ip_address)
    return ip_addresses


# Funkcja tworząca folder na komputerze
def createFolder(folderName):
    try:
        os.mkdir(folderName)
    except FileExistsError:
        pass
    except Exception as e:
        sg.popup_error(e)


# Połączenie socket
class Connection:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.clientSocket = None

    def connect(self):
        try:
            self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.clientSocket.connect((self.ip, self.port))
            return True
        except Exception as e:
            sg.popup_error(f"Błąd połączenia {e}")


# Działanie na sockecie
class Sending(Connection):
    def __init__(self, ip, port):
        super().__init__(ip, port)

    def sendData(self, data, which):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
                clientSocket.connect((self.ip, self.port))
                if which == 1:
                    file_name = os.path.basename(data)
                    clientSocket.sendall(f"FILE:{file_name}".encode())
                    with open(data, 'rb') as file:
                        clientSocket.sendfile(file)
                    clientSocket.sendall(b"END")
                elif which == 2:
                    clientSocket.sendall(f"CMD:{data}".encode())
                while True:
                    data = clientSocket.recv(1024)
                    if data == b"File received":
                        break
        except Exception as e:
            sg.popup_error(e)
