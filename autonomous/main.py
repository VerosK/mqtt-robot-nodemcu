import machine
from time import sleep

from motor import motors

motor_l, motor_r = motors

btn_r = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
btn_l = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)

while True:
    motor_l.go(100)
    motor_r.go(100)
    if btn_l() == 0:
        motor_l.go(-100)
        motor_r.go(-100)
        sleep(0.25)
        motor_l.go(100)
        sleep(0.5)
    elif btn_r() == 0:
        motor_l.go(-100)
        motor_r.go(-100)
        sleep(0.25)
        motor_r.go(100)
        sleep(0.5)
    else:
        sleep(0.1)
