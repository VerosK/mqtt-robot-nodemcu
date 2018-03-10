import machine
import time

class Motor:
    def __init__(self, dir_pin, speed_pin, reversed=True):
        self.dir_pin = machine.Pin(dir_pin, machine.Pin.OUT)
        self.speed_pwm = machine.PWM(
            machine.Pin(speed_pin, machine.Pin.OUT), freq=500)
        if reversed:
            self._speed_factor = -11
        else:
            self._speed_factor = 11

    def stop(self):
        self.speed_pwm.duty(0)

    def go(self, speed=100):
        """Set current speed (from -100 to 100, negative means backwards)"""
        self._speed = speed = max(min(speed, 100), -100)
        if speed > 0:
            self.dir_pin.value(1)
            self._set_pwm(speed)
        else:
            self.dir_pin.value(0)
            self._set_pwm(-speed)

    def speed(self):
        """Get the current speed"""
        return self.speed

    def _set_pwm(self, speed):
        self.speed_pwm.duty(min(self._speed_factor*speed,1024))

    def test(self):
        "Run motor test"
        for i in range(5,11,+1):
            print("motor forward %i" % i)
            self.go(10*i)
            time.sleep(1)
        for i in range(10,1,-1):
            print("motor backward %i" % i)
            self.go(-10*i)
            time.sleep(1)
        print("motor stop")
        self.stop()


motor_a = Motor(dir_pin=0, speed_pin=5)
motor_b = Motor(dir_pin=2, speed_pin=4)
motors = motor_a, motor_b
