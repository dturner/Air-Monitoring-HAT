import paho.mqtt.client as mqtt  # Correct import
from pms_a003 import Sensor, SensorException
import time

# MQTT Broker settings
broker_address = "192.168.1.23"
topic_prefix = "airquality/sensor1"
mqtt_username = "mqtt-user"
mqtt_password = "flyingd00b"

# Sensor setup
sensor = Sensor()


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)
    # You can add any logic to handle connection properties here (optional)


def publish_sensor_data(client, data):
    pm100 = data.pm100_std
    pm25 = data.pm25_std
    pm10 = data.pm10_std
    # ... read other parameters as needed

    client.publish(f"{topic_prefix}/pm10", pm100)
    client.publish(f"{topic_prefix}/pm2.5", pm25)
    client.publish(f"{topic_prefix}/pm1.0", pm10)
    # ... publish other parameters

    print(f"Published: PM10: {pm100}, PM2.5: {pm25}, PM1.0: {pm10}")  # Optional print


def main():
    # Create MQTT client and set callback
    client_id = "garage_air_quality_sensor"
    client = mqtt.Client(client_id=client_id, callback_api_version=mqtt.CallbackAPIVersion.VERSION2) 
    client.on_connect = on_connect
    client.username_pw_set(mqtt_username, mqtt_password)

    # Connect to broker
    client.connect(broker_address)

    try:
        # Connect to the sensor
        sensor.connect_hat()

        # Keep the connection alive
        client.loop_start()

        while True:
            try:
                data = sensor.read()
                publish_sensor_data(client, data)
            except SensorException as e:
                print(f"Sensor error: {e}")

            time.sleep(5)

    except SensorException as e:
        print(f"Failed to connect to sensor: {e}")

    # Disconnect
    client.loop_stop()
    sensor.disconnect_hat()


if __name__ == "__main__":
    main()