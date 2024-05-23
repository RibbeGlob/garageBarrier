import RPi.GPIO as GPIO
import time

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
        self.pwm.start(20)

        while time.time() - start_time < 0.2:
            GPIO.output(self.in_one_engine, GPIO.HIGH)
            GPIO.output(self.in_two_engine, GPIO.LOW)
            time.sleep(0.5)

        GPIO.output(self.in_one_engine, GPIO.LOW)
        GPIO.output(self.in_two_engine, GPIO.LOW)
        GPIO.cleanup()

    def backward(self):
        start_time = time.time()
        self.pwm.start(20)

        while time.time() - start_time < 0.2:
            GPIO.output(self.in_one_engine, GPIO.LOW)
            GPIO.output(self.in_two_engine, GPIO.HIGH)
            time.sleep(0.5)

        GPIO.output(self.in_one_engine, GPIO.LOW)
        GPIO.output(self.in_two_engine, GPIO.LOW)
        GPIO.cleanup()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        action = sys.argv[1]
        engine = Engine()
        if action == "open":
            engine.forward()
        elif action == "close":
            engine.backward()
