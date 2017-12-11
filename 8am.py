import appdaemon.appapi as appapi
import datetime
import calendar

class EarlyMorning(appapi.AppDaemon):
	def initialize(self):
		time=datetime.time(8,00,00)
		self.run_daily(self.run_daily_callback, time)

	def run_daily_callback(self, kwargs):
		self.turn_off(entity_id="switch.fan")

class Night(appapi.AppDaemon):
    def initialize(self):
        time=datetime.time(23,00,00)
        self.run_daily(self.run_daily_callback, time)
        self.log("{}".format("hello from Night"))

    def run_daily_callback(self, kwargs):
        self.call_service("media_player/volume_set",entity_id="media_player.bedroom_home",volume_level=0.3)
