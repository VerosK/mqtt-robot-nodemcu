import pexpect
import sys
import time

try:
    PORT = sys.argv[1]
except IndexError:
    PORT = '/dev/ttyUSB0'

try:
    NETWORK = sys.argv[2]
except IndexError:
    NETWORK = "robot"

try:
    PASSWORD = sys.argv[3]
except IndexError:
    PASSWORD = "12345678"


child = pexpect.spawn("picocom -b 115200 {}".format(PORT), 
        logfile=open('debug.log','wt'))

def sendline(ln):
    sys.stderr.write('>>> {}\r\n'.format(ln))
    return child.sendline(ln+"\r\n")

def expect(x, timeout=1):
    child.expect([x], timeout=timeout)
    # drain buffer
#
sendline('\003') # Ctrl+C
expect(">", timeout=2)
#
sendline("happy = ''.join(['O','K']); happy")
expect("OK", timeout=1)
#
sendline("import network; network")
#child.expect("module", timeout=1)
expect(b">", timeout=1)
# 
sendline("wifi = network.WLAN(network.STA_IF); ")
expect(b">", timeout=1)
# 
sendline("wifi.active(True); wifi")
expect(b"WLAN", timeout=1)

sendline("wifi.connect('{}', '{}'); wifi".format(NETWORK, PASSWORD))
expect("WLAN", timeout=1)
sendline("print('Waiting for connection')")
time.sleep(10)
#
sendline("wifi.isconnected()")
expect("True", timeout=1)

