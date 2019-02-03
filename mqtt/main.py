import wifi_connect
import client

try:
    from config import mqtt_host
except ImportError:
    mqtt_host = 'broker.hivemq.com'
try:
    from config import mqtt_user
except ImportError:
    mqtt_user = 'guest'
try:
    from config import mqtt_password
except ImportError:
    mqtt_password = 'guest'
try:
    from config import robot_name
except ImportError:
    robot_name = 'another robot'

wifi_connect.connect()
client.mqtt_drive(mqtt_host, robot_name=robot_name, mqtt_user=mqtt_user, mqtt_password=mqtt_password)
