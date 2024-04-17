import RPi.GPIO as GPIO
import time
import subprocess
import json
import requests
import os
import datetime
from gpiozero import Button
import threading

class Sensor:
    def __init__(self):
        self.trigger_sensor, self.echo_sensor = 18, 22
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_sensor, GPIO.OUT)
        GPIO.setup(self.echo_sensor, GPIO.IN)

    def distance(self):
        GPIO.output(self.trigger_sensor, True)
        time.sleep(0.00001)
        GPIO.output(self.trigger_sensor, False)
        StartTime, StopTime = time.time(), time.time()

        while GPIO.input(self.echo_sensor) == 0:
            StartTime = time.time()

        while GPIO.input(self.echo_sensor) == 1:
            StopTime = time.time()

        TimeElapsed = StopTime - StartTime
        distance = (TimeElapsed * 34300) / 2

        return distance


class Engine:
    def __init__(self):
        self.in_one_engine, self.in_two_engine, self.ena_engine = 24, 23, 25
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.in_one_engine, GPIO.OUT)
        GPIO.setup(self.in_two_engine, GPIO.OUT)
        GPIO.setup(self.ena_engine, GPIO.OUT)
        GPIO.output(self.in_one_engine, GPIO.LOW)
        GPIO.output(self.in_two_engine, GPIO.LOW)
        if not hasattr(self, 'pwm'):
            self.pwm = GPIO.PWM(self.ena_engine, 1000)

    def forward(self):
        start_time = time.time()

        while time.time() - start_time < 5:
            self.pwm.start(70)
            GPIO.output(self.in_one_engine, GPIO.HIGH)
            GPIO.output(self.in_two_engine, GPIO.LOW)
            time.sleep(0.5)

        GPIO.output(self.in_one_engine, GPIO.LOW)
        GPIO.output(self.in_two_engine, GPIO.LOW)
        GPIO.cleanup()

    def backward(self):
        start_time = time.time()

        while time.time() - start_time < 5:
            self.pwm.start(70)
            GPIO.output(self.in_one_engine, GPIO.LOW)
            GPIO.output(self.in_two_engine, GPIO.HIGH)
            time.sleep(0.5)

        GPIO.output(self.in_one_engine, GPIO.LOW)
        GPIO.output(self.in_two_engine, GPIO.LOW)
        GPIO.cleanup()


def capture_image():
    subprocess.run(['libcamera-still','-t 10', '-o', 'image.jpg'])
    file_info = os.stat('image.jpg')
    modification_time = file_info.st_mtime
    readable_time = datetime.datetime.fromtimestamp(modification_time)
    return readable_time


def api():
    path = r"/home/pi/samochodzik.jpg"
    with open(path, 'rb') as fp:
        response = requests.post(
            'https://api.platerecognizer.com/v1/plate-reader/',
            data=dict(regions=['pl'], config=json.dumps(dict(region="strict"))),
            files=dict(upload=fp),
            headers={'Authorization': 'Token 6bf05633011339939e0a8ca7002c6774318c63a6'})

    if response.status_code == 201:
        try:
            #os.remove(path)
            data = response.json()
            return data["results"][0]['plate']
        except FileNotFoundError:
            return "error"
    else:
        return "error"

def file_json(data, time):
    with open('parking.json', 'w') as file:
        json.dump({data : time}, file)

def change_mode(current_value):
    button = Button(3)
    button.wait_for_press()
    if current_value%2 == 0:
        print('xd')
    else:
        print('xx')
    current_value += 1
    return current_value

def main_logic():
    eng = None
    file_time = capture_image()
    time.sleep(2)
    result = api()      # Tablica rejestracyjna
    file_json(result, file_time)
    if result != "error":
        if not eng:
            eng = Engine()
        eng.forward()



def button_pressed():
    global running
    print("Przycisk został naciśnięty!")
    running = False  # Zatrzymaj działanie pętli
    time.sleep(5)     # Odczekaj 5 sekund
    running = True    # Wznów działanie pętli
    print("Program kontynuuje działanie...")



if __name__ == '__main__':
    confirm = 0
    button = Button(4)
    running = True
    button.when_pressed = button_pressed
    try:
        while True:
            if running:
                # tutaj daj logikę przycisku
                dist = Sensor()
                distance_value = dist.distance()
                print(distance_value)
                if distance_value < 100:
                    if confirm == 2:
                        main_logic()
                        confirm = 0
                    confirm += 1
                time.sleep(2)
                print("Wykonuję pracę...")
            time.sleep(1)  # Czekaj 1 sekundę, aby zmniejszyć użycie procesora
    except KeyboardInterrupt:
        print("Program zakończony przez użytkownika")
    finally:
        print("Zakończenie pracy programu")
