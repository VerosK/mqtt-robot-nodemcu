import client
try:
    from config import mqtt_host
except ImportError:
    mqtt_host = 'broker.hivemq.com'

client.start_wifi()
client.mqtt_drive(mqtt_host)

import network
wifi = network.WLAN()
print("To connect wifi wifi.connect('WIFI-NETWORK', 'PASSWORD')\n")
print("... and restart the board\n")
