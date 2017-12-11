import appdaemon.appapi as appapi
import requests
import pendulum

class Train(appapi.AppDaemon):
	def initialize(self):
		self.log("Hello from AppDaemon Train")
		self.WORK_STATION="lockheed"
		self.HOME_STATION="lick mill"
		self.listen_state(self.print_state, "sensor.train_station")

	def print_state(self, entity, attribute, old, new, kwargs):
		self.log("new state set to {}".format(new))
		if new=="home" or new=="not_home":
			return 

		station=new.lower()
		if station==self.HOME_STATION:
			state="Work" 
		elif station==self.WORK_STATION:
			state="Home"
		url="https://apiaihandler.herokuapp.com/train/{}".format(state)
		r=requests.get(url)
		if r.status_code!=200:
			self.get_app("utils").fb_notify(title = "Next Train", message = "Could not fetch train schedule")
		self.log("Next train at {}".format(r.text))

		dt=pendulum.parse(r.text,tz="America/Los_Angeles")
		self.log("{}".format(dt))
		diff=dt-pendulum.now(tz="America/Los_Angeles")
		self.log("{}".format(diff.in_words()))
		self.get_app("utils").fb_notify(title = "Train Schedule", message = "Next Train to {} is in {}".format(state,diff.in_words()))
