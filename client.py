import network
from utime import ticks_ms, ticks_add, ticks_diff
import time
from umqtt.simple import MQTTClient
import ubinascii, machine
import motor
from machine import Pin

topic = b'/robot/' + ubinascii.hexlify(machine.unique_id())

def start_wifi():
    global topic
    sta_if = network.WLAN(network.STA_IF); sta_if.active(True)
    timeout = 12
    print("Waiting for WiFi connection")
    while not sta_if.isconnected():
        print("... %ss" % timeout) 
        time.sleep(1)
        timeout = timeout - 1
        assert timeout, "WiFi failed"
    print("WiFi connected", sta_if.ifconfig())

# Publish test messages e.g. with:
# mosquitto_pub -t foo_topic -m hello

time_to_stop = 0
TIMEOUT = 100*1000 # stop after this ms

# Received messages from subscriptions will be delivered to this callback
def sub_cb(a_topic, msg):
    global time_to_stop

    tail = a_topic[len(topic)+1:]
    if tail == b'a/speed':
        motor.motor_a.set_speed(int(msg))
    elif tail == b'b/speed':
        motor.motor_b.set_speed(int(msg))
    elif tail == b'a/dir':
        motor.motor_a.set_dir(int(msg))
    elif tail == b'b/dir':
        motor.motor_b.set_dir(int(msg))
    else:
        print("got", tail)
    time_to_stop = ticks_add(ticks_ms, TIMEOUT)

def mqtt_drive(server="localhost"):
    global time_to_stop

    motor.motor_a.forward(100)
    motor.motor_b.forward(100)
    time.sleep(0.5)
    motor.motor_a.stop()
    motor.motor_b.stop()

    print("I'm %s" % topic)

    c = MQTTClient("umqtt_client", server)
    c.set_callback(sub_cb)
    c.set_last_will(topic + "/$online$", "0", retain=1)
    c.connect()
    c.subscribe(topic+'/#')
    while True:
            c.check_msg()
            if ticks_diff(ticks_ms(), time_to_stop) < 0:
                motor.motor_a.stop()
                motor.motor_b.stop()
                c.ping()
                time_to_stop = ticks_add(ticks_ms, 10*TIMEOUT)
            # Then need to sleep to avoid 100% CPU usage (in a real
            # app other useful actions would be performed instead)
            time.sleep(0.001)

    c.disconnect()

if __name__ == "__main__":
    start_wifi()
    mqtt_drive(server="mqtt.toaster.cz")
