from device import SmartLight, Thermostat, SecurityCamera
import tkinter as tk
import threading
import random
import time
from datetime import datetime

class MonitoringDashboard:
  def __init__(self, root, autoSys):
    self.root = root
    self.root.title("Smart Home IoT Simulator")
    gui_width = 600
    gui_height = 690
    self.root.geometry(f"{gui_width}x{gui_height}")
    self.autoSys = autoSys
    self.automation = False
    self.random_detect_motion = False
    self.exit_flag = False

    devices = autoSys.get_devices()

    for device in devices:
      if isinstance(device, SmartLight):
        self.smartLight = device
        self.brightness = device.get_brightness()
      if isinstance(device, Thermostat):
        self.thermostat = device
        self.temperature = device.get_temperature()
      if isinstance(device, SecurityCamera):
        self.securityCamera = device
        self.motion_detected = device.get_motion_detected()

    #region methods in init
    def update_device_status_periodically():
      while not self.exit_flag:
        if self.random_detect_motion and not self.random_detect_motion_loop_thread.is_alive():
          self.random_detect_motion_loop_thread = threading.Thread(target=random_detect_motion_loop)
          self.random_detect_motion_loop_thread.start()
        update_brightness_gui()
        update_motion_detected_text()
        time.sleep(0.5) #every 0.5 sec

    def random_detect_motion_loop():
      while self.random_detect_motion and not self.exit_flag and self.securityCamera.get_is_on():
        self.motion_detected = random.choice([True, False])
        self.securityCamera.set_motion_detected(self.motion_detected)
        time.sleep(5) #every 5 sec

    def update_status():
      status_field.config(state="normal")
      status_field.delete(1.0, tk.END)
      status_text = "Living Room Light: SmartLight Status: "
      status_text += "On" if self.smartLight.get_is_on() else "Off" 
      status_text += "\nLiving Room Thermostat: Thermostat Status: "
      status_text += "On" if self.thermostat.get_is_on() else "Off" 
      status_text += "\nFront Door Camera: SecurityCamera Status: "
      status_text += "On" if self.securityCamera.get_is_on() else "Off" 
      status_text += "\nRandom Detect Motion: "
      status_text += "On" if self.random_detect_motion else "Off"
      status_field.insert(tk.END, status_text)
      status_field.config(state="disable")

    def update_automation_label_text():
      automation_label_text = "Automation Status: "
      automation_label_text += "On" if self.automation else "Off"
      automaiton_label.config(text = automation_label_text)

    def update_motion_detected_text():
      motion_label_text = "Front Door Camera - Motion: "
      motion_label_text += "YES" if self.motion_detected else "NO"
      motion_label_2.config(text = motion_label_text)

    def update_automation_toggle():
      self.automation = not self.automation
      self.autoSys.automation_on() if self.automation else self.autoSys.automation_off()
      update_automation_label_text()

    def update_smartlight_toggle():
      self.smartLight.turn_off() if self.smartLight.get_is_on() else self.smartLight.turn_on()
      update_status()

    def update_thermostat_toggle():
      self.thermostat.turn_off() if self.thermostat.get_is_on() else self.thermostat.turn_on()
      update_status()

    def update_camera_toggle():
      self.securityCamera.turn_off() if self.securityCamera.get_is_on() else self.securityCamera.turn_on()
      update_status()

    def update_random_detect_motion_toggle():
      self.random_detect_motion = not self.random_detect_motion
      update_status()

    def update_brightness(value):
      self.smartLight.set_brightness(value)
      self.brightness = value
      self.light_label_2.config(text=f"Living Room Light - {self.brightness}%")

    def update_brightness_gui():
      self.brightness = self.smartLight.get_brightness()
      self.light_label_2.config(text=f"Living Room Light - {self.brightness}%")
      self.brightness_scale.config(variable=tk.IntVar(value=self.brightness))


    def update_temperature(value):
      self.thermostat.set_temperature(value)
      self.temperature = value
      self.temperature_label_2.config(text=f"Living Room Thermostat - {self.temperature}°C")

    def update_events_field():
      while not self.exit_flag:
        events_field.config(state="normal")
        current_datetime = datetime.now()
        current_date_string = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        new_text = f"[{current_date_string}], brightness: {self.brightness}, temperature: {self.temperature}, motion_detected: {self.motion_detected}\n"
        events_field.insert(tk.END, new_text)
        time.sleep(3) #every 3 sec
    #endregion

    #region Automation
    automation_toggle_button = tk.Button(root, text="Automation ON/OFF", command=update_automation_toggle)
    automation_toggle_button.pack()
    automaiton_label = tk.Label(root)
    automaiton_label.pack()
    update_automation_label_text()
    #endregion

    #region status_field
    status_field = tk.Text(root, width=60, height=10, state="disabled")
    status_field.pack()
    update_status()
    #endregion

    #region SmartLight
    light_label_1 = tk.Label(root, text="Living Room Light Brightness")
    light_label_1.pack()

    self.brightness_scale = tk.Scale(root, from_=0, to=100, orient="horizontal", command=update_brightness, variable=tk.IntVar(value=50))
    self.brightness_scale.pack()

    light_toggle_button = tk.Button(root, text="Toggle ON/OFF", bd=0, command=update_smartlight_toggle)
    light_toggle_button.pack()

    self.light_label_2 = tk.Label(root, text=f"Living Room Light - {self.brightness}%")
    self.light_label_2.pack()
    #endregion

    #region Thermostat
    temperature_label_1 = tk.Label(root, text=f"Living Room Thermostat Temperature")
    temperature_label_1.pack()

    temperature_scale = tk.Scale(root, from_=18, to=32, orient="horizontal", command=update_temperature, variable=tk.IntVar(value=24))
    temperature_scale.pack()

    thermostat_toggle_button = tk.Button(root, text="Toggle ON/OFF", command=update_thermostat_toggle)
    thermostat_toggle_button.pack()

    self.temperature_label_2 = tk.Label(root, text=f"Living Room Thermostat - {self.temperature}°C")
    self.temperature_label_2.pack()
    #endregion

    #region SecurityCamera
    motion_label_1 = tk.Label(root, text="Front Door Camera Motion Detection")
    motion_label_1.pack()

    random_detect_button = tk.Button(root, text="Random Detect Motion ON/OFF", command=update_random_detect_motion_toggle)
    random_detect_button.pack()

    motion_toggle_button = tk.Button(root, text="Toggle ON/OFF", command=update_camera_toggle)
    motion_toggle_button.pack()

    motion_label_2 = tk.Label(root)
    motion_label_2.pack()
    update_motion_detected_text()
    #endregion

    auto_rule_label = tk.Label(root, text="Automation Rule: Turn on lights when motion is detected")
    auto_rule_label.pack()

    brightness_events_label = tk.Label(root, text="Events")
    brightness_events_label.pack()

    events_field = tk.Text(root, width=90, height=10, state="disabled")
    events_field.pack()
    

    #region threads
    self.random_detect_motion_loop_thread = threading.Thread(target=random_detect_motion_loop)
    self.update_device_status_periodically_thread = threading.Thread(target=update_device_status_periodically)
    self.update_device_status_periodically_thread.start()
    self.update_events_field_thread = threading.Thread(target=update_events_field)
    self.update_events_field_thread.start()
    #endregion
    
  def on_close(self):
    self.exit_flag = True

    self.update_device_status_periodically_thread.join()
    self.random_detect_motion_loop_thread.join()

    self.root.destroy()