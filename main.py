import PySimpleGUI as sg
from abc import ABC, abstractmethod
import BackEnd as be

# Klasa odpowiedzialna za szkielet GUI
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


# Klasa odpowiedzialna za interfejs łączenia się z RPI
class ConnectRaspberry(Pattern):
    def __init__(self):
        field = (200, 100)
        self.response = None
        self.ipList = be.findIp()
        super().__init__(field)

    def gui(self, *args):
        super().gui([sg.Text("Wybierz adres IP Raspberry")],
                     [sg.InputCombo(self.ipList, size=(22, 1), key="-IP-", readonly=True)],
                    [sg.Button("Połącz", size=21, key='-BT-')])

    def run(self, mapa, basicEvent = None):
        map = {
            '-BT-': self.connectButtonClicked,
        }
        super().run(map)

    def connectButtonClicked(self, values):
        ip = values['-IP-']
        self.buttonEffect('-BT-', 'Połącz', self.backEndIntegration(ip, 12345))

    def backEndIntegration(self, ip, port):
        # connection = be.Connection(ip, 12345)
        # connection.connect()
        # connection.clientSocket.close()
        self.close()
        myMenu = MenuRaspberry(ip, port)
        myMenu.gui()


# Klasa odpowiedzialna za główne menu RPI
class MenuRaspberry(Pattern):
    def __init__(self, ip, port):
        self.ip, self.port = ip, port
        size = (450, 240)
        super().__init__(size)

    def gui(self):
        super().gui([
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

    def connectButtonClicked(self, values):
        print('xd')

    def run(self, mapa, basicEvent = None):
        map = {
            '-BT-': self.connectButtonClicked,
        }
        super().run(map)


def main():
    myGui = ConnectRaspberry()
    myGui.gui()

if __name__ == "__main__":
    main()