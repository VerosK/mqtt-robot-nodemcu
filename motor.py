import machine
import time

class _Motor:

    def __init__(self, dir_pin, speed_pin):
        self.dir_pin = machine.Pin(dir_pin, machine.Pin.OUT)
        self.speed_pwm = machine.PWM(
            machine.Pin(speed_pin, machine.Pin.OUT), freq=500)

    def stop(self):
        self.speed_pwm.duty(0)

    def _go(self, speed):
        self.speed_pwm.duty(min(11*speed,1024))

    def set_dir(self, dir):
        self.dir_pin.value(dir)

    def set_speed(self, speed=100):
        self._go(speed)

    def forward(self, speed=100):
        self.dir_pin.value(1)
        self._go(speed)

    def backward(self, speed=100):
        self.dir_pin.value(0)
        self._go(speed)

    def test(self):
        "Run motor test"
        for i in range(5,11,+1):
            print("motor forward %i" % i)
            self.forward(10*i)
            time.sleep(1)
        for i in range(10,1,-1):
            print("motor backward %i" % i)
            self.forward(10*i)
            self.backward(10*i)
            time.sleep(1)
        print("motor stop")
        self.stop()

motor_a = _Motor(dir_pin=0, speed_pin=5)
motor_b = _Motor(dir_pin=2, speed_pin=4)


