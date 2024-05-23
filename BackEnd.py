import os
import PySimpleGUI as sg
import paramiko
import json

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


def current_vehicles():
    hostname = 'malinka.local'
    port = 22  # Domyślny port SSH
    username = 'pi'
    password = 'malinka'
    remote_path = r"/home/pi/parking.json"
    local_path = r"C:\Users\gerfr\OneDrive\Pulpit\RPI\xd.json"

    # Utworzenie klienta SSH
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname, port=port, username=username, password=password)
    sftp = ssh_client.open_sftp()
    sftp.get(remote_path, local_path)
    sftp.close()
    ssh_client.close()

    with open(local_path, 'r') as file:
        data = json.load(file)

    formatted_data = "\n".join([f"{key}: {value}" for key, value in data.items()])
    return formatted_data


def past_vehicles():
    hostname = 'malinka.local'
    port = 22  # Domyślny port SSH
    username = 'pi'
    password = 'malinka'
    remote_path = r"/home/pi/past_parking.json"
    local_path = r"C:\Users\gerfr\OneDrive\Pulpit\RPI\xd.json"

    # Utworzenie klienta SSH
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname, port=port, username=username, password=password)
    sftp = ssh_client.open_sftp()
    sftp.get(remote_path, local_path)
    sftp.close()
    ssh_client.close()

    with open(local_path, 'r') as file:
        data = json.load(file)

    formatted_data = "\n".join([f"{key}: {value}" for key, value in data.items()])

    return formatted_data

