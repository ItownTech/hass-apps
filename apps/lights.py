
import appdaemon.appapi as appapi
import datetime

class LightsatNight(appapi.AppDaemon):

  def initialize(self):
      self.log("Hello from Lights")
      ontime=self.parse_time("sunset - 00:20:00")
      self.run_daily(self.lights_on,ontime)
      self.listen_state(self.near_home_enter,"sensor.state",new="NearHome",old="Outside")
      self.listen_state(self.home_exit,"sensor.state",old="Home")

  def lights_on(self,*args,**kwargs):
      if self.get_state("sensor.state")=="Home" and self.get_state("light.main_light")=="off":
          self.get_app("utils").lights_on()

  def near_home_enter(self, entity, attribute, old, new, kwargs):
    if self.time() > self.parse_time("sunset-00:30:00"):
        self.get_app("utils").lights_on()
    if float(self.get_state("sensor.weather_temperature"))>=17.0:
        self.turn_on("switch.fan")

  def home_exit(self, entity, attribute, old, new, kwargs):
      self.turn_off("group.bedroom")
      
