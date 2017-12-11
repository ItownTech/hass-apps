import appdaemon.appapi as appapi
import requests,time
from collections import defaultdict
from transitions import Machine
from transitions.core import MachineError
import logging
logging.basicConfig(level=logging.DEBUG)

class StateMachineHandler(appapi.AppDaemon):

	def initialize(self):
		self.log("Hello")

	def lights_at_home(self):
		self.turn_on("light.table_lamp",brightness_pct=100)

	def on_nearhome(self):
		self.turn_off("light.table_lamp")

class StateHandler(appapi.AppDaemon):
	def initialize(self):
		self.states=['Home','Work','Outside','Car','NearHome']
		self.log("Hello from StateHandler")
		state=self.get_state("sensor.state","state")
		self.sm=self.get_app("StateMachineHandler")
		self.listen_state(self.add_state, "sensor.transitions")
		self.statemachine=Machine(self.sm,initial=state,states=self.states)
		self.add_transitions()
		self.test()

	def add_transitions(self):
		self.statemachine.add_transition('Home_NearHome', 'Home', 'NearHome')
		self.statemachine.add_transition('NearHome_Home', 'NearHome', 'Home')
		self.statemachine.add_transition('Outside_NearHome', 'Outside', 'NearHome')
		self.statemachine.add_transition('NearHome_Outside', 'NearHome', 'Outside')
		self.statemachine.add_transition('Outside_Car', 'Outside', 'Car')
		self.statemachine.add_transition('Car_Outside', 'Car', 'Outside')
		self.statemachine.add_transition('Outside_Work', 'Outside', 'Work')
		self.statemachine.add_transition('Work_Outside', 'Work', 'Outside')

	def test(self):
		self.add_callback("NearHome","enter",self.sm.on_nearhome)
		self.add_callback("Home","exit",self.sm.lights_at_home)

	def add_callback(self,state,event,func):
		state="on_{}_{}".format(event.lower(),state)
		try:
			getattr(self.statemachine,state)(func)
		except Exception as e:
			self.log(e)

	def add_state(self,*args,**kwargs):
		transition=args[3]
		transition=transition.replace("-","_")
		try:
			self.sm.trigger(transition)
		except Exception as e:
			self.log(e)
			self.get_app('utils').fb_notify(e)
		self.log("state:{}".format(self.sm.state))
		self.get_app('utils').fb_notify("State set to {}".format(self.sm.state))
