import client
try:
    from config import mqtt_host
except ImportError:
    mqtt_host = 'broker.hivemq.com'
try:
    from config import robot_name
except ImportError:
    robot_name = 'another robot'

client.start_wifi()
client.mqtt_drive(mqtt_host, robot_name=robot_name)
