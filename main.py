import PySimpleGUI as sg
from abc import ABC, abstractmethod
import BackEnd as be
import paramiko

class Pattern(sg.Window, ABC):
    def __init__(self, field):
        super().__init__(title="garageBarrier", size=field)
        self.closed = False

    @abstractmethod
    def gui(self, *args):
        interface = [arg for arg in args]
        self.layout([[interface]])
        self.run(None)

    @abstractmethod
    def run(self, mapa, basicEvent=None):
        def closeWindow(_):
            self.closed = True
            self.close()

        self.eventsMap = {
            sg.WIN_CLOSED: closeWindow,
        }

        self.eventsMap.update(mapa)
        while not self.closed:
            event, values = self.read()
            runFunction = self.eventsMap.get(event, basicEvent)
            runFunction(values)

    @staticmethod
    def buttonEffect(buttonTrigger, buttonName, effect):
        if buttonTrigger == buttonName:
            return effect

    @staticmethod
    def checkboxEffect(checkboxTrigger, checkboxStatus):
        if checkboxTrigger == checkboxStatus:
            pass


# Klasa odpowiedzialna za główne menu RPI
class MenuRaspberry(Pattern):
    def __init__(self):
        self.ssh_client = None
        self.hostname = 'malinka'
        self.port = 22
        self.username = 'pi'
        self.password = 'malinka'
        size = (450, 240)
        super().__init__(size)

    def gui(self):
        super().gui([sg.Frame('Zdjęcie ostatniego pojazadu', [])],
            [
            sg.Frame('Sprawdź informacje na temat \naktualnych pojazdów', [
                [sg.Multiline(default_text="", size=(25, 5), key="-AC-", autoscroll=True)],
                [sg.Button("Uaktualnij dane", size=23, key='-BA-')]
            ]),
            sg.Push(),
            sg.Frame('Sprawdź informacje na temat \npojazdów które wyjechały', [
                [sg.Multiline(default_text="", size=(25, 5), key="-PC-", autoscroll=True)],
                [sg.Button("Uaktualnij dane", size=23, key='-BP-')]
            ])],
            [
            sg.Frame('Ręczne sterowanie szlabanem', [
                [sg.Button("Otwórz szlaban", size=24, key='-BO-'),
                 sg.Button("Zamknij szlaban", size=24, key='-BC-')]
            ]
        )])

    def connect_ssh(self):
        if not self.ssh_client:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(self.hostname, port=self.port, username=self.username, password=self.password)

    def open_barrier(self, values):
        self.connect_ssh()
        stdin, stdout, stderr = self.ssh_client.exec_command('python3 /home/pi/engine.py open')
        print(stdout.read().decode())
        print(stderr.read().decode())

    def close_barrier(self, values):
        self.connect_ssh()
        stdin, stdout, stderr = self.ssh_client.exec_command('python3 /home/pi/engine.py close')
        print(stdout.read().decode())
        print(stderr.read().decode())

    def connectButtonClicked(self, values):
        print('xd')

    def backend_integration(self, values):
        xd = be.current_vehicles()
        self['-AC-'].update(xd)

    def backend_integration2(self, values):
        xd = be.past_vehicles()
        self['-PC-'].update(xd)

    def run(self, mapa, basicEvent = None):
        map = {
            '-BA-': self.backend_integration,
            '-BP-': self.backend_integration2,
            '-BO-': self.open_barrier,
            '-BC-': self.close_barrier,

        }
        super().run(map)


def main():
    myMenu = MenuRaspberry()
    myMenu.gui()

if __name__ == "__main__":
    main()