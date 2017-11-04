import network
from utime import ticks_ms, ticks_add, ticks_diff
import time
from umqtt.simple import MQTTClient
import ubinascii, machine
import motor
from machine import Pin

robot_id = ubinascii.hexlify(machine.unique_id())
topic = b'/robot/' + robot_id

def start_wifi():
    global topic
    sta_if = network.WLAN(network.STA_IF); sta_if.active(True)
    timeout = 15
    print("Waiting for WiFi connection")
    while not sta_if.isconnected():
        print("... %ss" % timeout) 
        time.sleep(1)
        timeout = timeout - 1
        assert timeout, "WiFi failed"
    print("WiFi connected", sta_if.ifconfig())

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
        if a > 0:
            motor.motor_a.forward(a)
        else:
            motor.motor_a.backward(a)
        if b > 0:
            motor.motor_b.forward(b)
        else:
            motor.motor_b.backward(b)
    else:
        print("got", tail)
    time_to_stop = ticks_ms() + TIMEOUT

def intro():
    motor.motor_a.stop()
    motor.motor_b.stop()

    motor.motor_a.forward(100)
    motor.motor_b.backward(100)
    time.sleep(0.5)
    motor.motor_a.backward(100)
    motor.motor_b.forward(100)
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
    start_wifi()
    mqtt_drive(server="mqtt.toaster.cz")
