import network
from utime import ticks_ms, ticks_add, ticks_diff
import time
from umqtt.simple import MQTTClient
import ubinascii, machine
import motor
from machine import Pin
import wifi_connect

robot_id = ubinascii.hexlify(machine.unique_id())
topic = b'/robot/' + robot_id

time_to_stop = 0
TIMEOUT = 1000 # stop after this ms

# Received messages from subscriptions will be delivered to this callback
def msg_callback(a_topic, msg):
    global time_to_stop

    print(repr(topic), repr(msg))
    tail = a_topic[len(topic)+1:]
    print(repr(tail), repr(msg))
    if tail == b'motors':
        parts = msg.split(b',')

        a,b = int(parts[0]),int(parts[1])
        motor.motor_a.go(a)
        motor.motor_b.go(b)
    else:
        print("got", tail)
    time_to_stop = ticks_ms() + TIMEOUT

def intro():
    motor.motor_a.stop()
    motor.motor_b.stop()

    motor.motor_a.go(100)
    motor.motor_b.go(-100)
    time.sleep(0.5)
    motor.motor_a.go(-100)
    motor.motor_b.go(100)
    time.sleep(0.5)


def mqtt_drive(server="localhost", robot_name='robot'):
    global time_to_stop

    intro()

    motor.motor_a.stop()
    motor.motor_b.stop()

    print("I'm %s" % topic)

    time_to_announce = ticks_ms() + 15 * 1000

    c = MQTTClient(b"umqtt_client/%s" % robot_id, server)
    c.set_callback(msg_callback)
    #    c.set_last_will(topic + "/$online$", "0", retain=1)
    c.connect()
    c.publish(topic+"/$online$", '1')
    c.publish(topic + "/$name$", robot_name, retain=1)
    c.subscribe(topic+'/#')
    while True:
            c.check_msg()
            if ticks_ms() > time_to_stop:
                motor.motor_a.stop()
                motor.motor_b.stop()
                c.ping()
                time_to_stop = ticks_ms() + 10*TIMEOUT

            if ticks_ms() > time_to_announce:
                c.publish(topic + "/$online$", '1')
                time_to_announce = ticks_ms() + 16 * 1000

            # Then need to sleep to avoid 100% CPU usage (in a real
            # app other useful actions would be performed instead)
            time.sleep(0.005)

    c.disconnect()

if __name__ == "__main__":
    wifi_connect.connect()
    mqtt_drive(server="mqtt.toaster.cz")
