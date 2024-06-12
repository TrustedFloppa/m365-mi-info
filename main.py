import json
import time
from paho.mqtt import client as mqtt_client

broker = '127.0.0.1'
port = 1883
username = 'scooter'
password = 'PASSWORD'
topic = "m365/test/"
client_id = f'python-reader-{int(time.time())}'

data_mapping = {
    'esc_phase_a_current': 'ESC Phase A Current',
    'esc_phase_b_current': 'ESC Phase B Current',
    'esc_phase_c_current': 'ESC Phase C Current',
    'drive_mode': 'Drive Mode',
    'bms_level': 'BMS Level',
    'esc_current_ma': 'ESC Current (mA)',
    'bms_volt': 'BMS Voltage (V)',
    'esc_volt': 'ESC Voltage (V)',
    'speed': 'Speed (km/h)',
    'total_km': 'Total Mileage (km)',
    'current_m': 'Current Mileage (m)',
    'total_uptime': 'Total Uptime (s)',
    'triptime1': 'Trip Time',
    'frame_temp1': 'Frame Temperature 1 (C)',
    'frame_temp2': 'Frame Temperature 2 (C)',
    'bms_cell_voltages': 'BMS Cell Voltages',
    'bms_health': 'BMS Health (%)',
    'bms_status': 'BMS Status',
    'bms_chargecount': 'BMS Charge Count',
    'bms_chargefullcount': 'BMS Charge Full Count',
    'bms_serial': 'BMS Serial Number',
    'bms_current_ma': 'BMS Current (mA)',
    'bms_temp1': 'BMS Temperature 1 (C)',
    'bms_temp2': 'BMS Temperature 2 (C)',
}

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}\n")

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def on_message(client, userdata, msg):
    reg = msg.topic.replace(topic, "")
    payload = msg.payload.decode()
    
    if reg in data_mapping:
        if reg == 'bms_cell_voltages':
            payload = json.loads(payload)
            formatted_payload = ', '.join([f"Cell {i+1}: {v}V" for i, v in enumerate(payload)])
        else:
            formatted_payload = payload
        print(f"{data_mapping[reg]}: {formatted_payload}")

def main():
    mqtt_client = connect_mqtt()
    mqtt_client.subscribe(topic + '#')
    mqtt_client.on_message = on_message
    mqtt_client.loop_forever()

if __name__ == "__main__":
    main()
