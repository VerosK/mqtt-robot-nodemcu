import network
import time

import config


def turn_off():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(False)
    ap = network.WLAN(network.AP_IF)
    ap.active(False)


def connect():
    ap = network.WLAN(network.AP_IF)
    ap.active(False)

    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(config.wifi_essid, config.wifi_password)

    elapsed = 0
    while not wifi.isconnected():
        time.sleep(1)
        elapsed += 1
        print('connecting to ' + config.wifi_essid + ' ... '  + str(elapsed))
    print("WiFi connected", wifi.ifconfig())
