from monitoring_dashboard import MonitoringDashboard
from automation_system import AutomationSystem
from device import SmartLight, Thermostat, SecurityCamera
import tkinter as tk
import threading

def main():
  smartLight = SmartLight(1_1)
  thermostat = Thermostat(2_1)
  securityCamera = SecurityCamera(3_1)
  autoSys = AutomationSystem()
  autoSys.discover_device(smartLight)
  autoSys.discover_device(thermostat)
  autoSys.discover_device(securityCamera)

  automatic_lightning_thread = threading.Thread(target=autoSys.automatic_lighting)
  automatic_lightning_thread.start()

  store_sensor_data_thread = threading.Thread(target=autoSys.store_sensor_data)
  store_sensor_data_thread.start()

  root = tk.Tk()
  app = MonitoringDashboard(root, autoSys)
  root.mainloop()

  autoSys.stop_threads_on()
  automatic_lightning_thread.join()
  store_sensor_data_thread.join()

if __name__ == "__main__":
  main()
