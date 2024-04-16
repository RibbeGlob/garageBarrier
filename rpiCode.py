import RPi.GPIO as GPIO
import time
import subprocess


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

def capture_image():
    # Wykonanie polecenia libcamera-still
    subprocess.run(['libcamera-still', '-o', 'image.jpg'])


class Engine:
    def __init__(self):
        self.in_one_engine, self.in_two_engine, self.ena_engine = 24, 23, 25
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.in_one_engine, GPIO.OUT)
        GPIO.setup(self.in_two_engine, GPIO.OUT)
        GPIO.setup(self.ena_engine, GPIO.OUT)
        GPIO.output(self.in_one_engine, GPIO.LOW)
        GPIO.output(self.in_two_engine, GPIO.LOW)
        self.pwm = GPIO.PWM(self.ena_engine, 1000)

    def forward(self):
        start_time = time.time()

        while time.time() - start_time < 5:
            self.pwm.start(50)
            GPIO.output(self.in_one_engine, GPIO.HIGH)
            GPIO.output(self.in_two_engine, GPIO.LOW)
            time.sleep(0.5)

        GPIO.output(self.in_one_engine, GPIO.LOW)
        GPIO.output(self.in_two_engine, GPIO.LOW)
        GPIO.cleanup()

    def backward(self):
        start_time = time.time()

        while time.time() - start_time < 5:
            self.pwm.start(50)
            GPIO.output(self.in_one_engine, GPIO.LOW)
            GPIO.output(self.in_two_engine, GPIO.HIGH)
            time.sleep(0.5)

        GPIO.output(self.in_one_engine, GPIO.LOW)
        GPIO.output(self.in_two_engine, GPIO.LOW)
        GPIO.cleanup()



if __name__ == '__main__':
    try:
        while True:
            dist = Sensor()
            distance_value = dist.distance()
            print("Measured Distance = %.1f cm" % distance_value)
            if distance_value < 100:
                print("Obstacle detected close. Taking a picture...")
                capture_image()
            time.sleep(1)

    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()

