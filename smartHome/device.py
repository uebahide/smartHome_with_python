class Device:
  def __init__(self, device_id, is_on = False):
    self.device_id = device_id
    self.is_on = is_on

  def turn_on(self):
        self.is_on = True
        
  def turn_off(self):
      self.is_on = False
      
  def get_is_on(self):
      return self.is_on
  
  def get_device_id(self):
      return self.device_id
  

class SmartLight(Device):
    def __init__(self, device_id, brightness = 50, is_on = False):
        super().__init__(device_id, is_on)
        self.brightness = brightness
        
    def set_brightness(self, brightness):
        self.brightness = brightness
    
    def get_brightness(self):
        return self.brightness

class Thermostat(Device):
    def __init__(self, device_id, temperature = 24, is_on = False):
        super().__init__(device_id, is_on)
        self.temperature = temperature
        
    def set_temperature(self, temperature):
        self.temperature = temperature
    
    def get_temperature(self):
        return self.temperature

class SecurityCamera(Device):
    def __init__(self, device_id, motion_detected=False, is_on=False):
        super().__init__(device_id, is_on)
        self.motion_detected = motion_detected

    def detect_motion(self):
        self.motion_detected = True

    def not_detect_motion(self):
        self.motion_detected = False

    def set_motion_detected(self, motion_detected):
        self.motion_detected = motion_detected

    def get_motion_detected(self):
        return self.motion_detected

