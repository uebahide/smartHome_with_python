from device import SmartLight, Thermostat, SecurityCamera
from datetime import datetime
import csv
import time
import os

class AutomationSystem:
    def __init__(self):
        self.devices = []
        self.stop_threads = False
        self.automation = False

    def get_devices(self):
        return self.devices

    def discover_device(self, device):
        self.devices.append(device)

    def automation_on(self):
        self.automation = True

    def automation_off(self):
        self.automation = False
        
    def automatic_lighting(self):
        while not self.stop_threads:
            for device in self.devices:
                if isinstance(device, SecurityCamera) and device.motion_detected  and self.automation:
                    for light in self.devices:
                        if isinstance(light, SmartLight) and light.get_is_on():
                            light.set_brightness(100)
                             
            time.sleep(1) #every 1 sec
                    
    def store_sensor_data(self):
        while not self.stop_threads:
            for device in self.devices:
                if isinstance(device, SecurityCamera):
                    detected = device.motion_detected
                if isinstance(device, SmartLight):
                    brightness = device.brightness
                if isinstance(device, Thermostat):
                    temperature = device.temperature
            
        
            current_time = datetime.now()
            timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
            
            sensor_data = [
                [timestamp , temperature, brightness, detected]
            ]

            file_path = "sensor_data.csv"
            write_header = not os.path.exists(file_path) or os.path.getsize(file_path) == 0
            
            with open(file_path, mode="a") as file:
                writer = csv.writer(file)
                if write_header:
                    writer.writerow(["Timestamp", "Temperature (°C)", "Brightness", "Motion detected"])
                writer.writerows(sensor_data)

            time.sleep(1) #every 1 sec

    def stop_threads_on(self):
        self.stop_threads = True