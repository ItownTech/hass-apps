import appdaemon.appapi as appapi

class Bedroom(appapi.AppDaemon):
    def initialize(self):
        self.log("Hello from AppDaemon bedroom")        
        self.listen_state(self.in_bedroom,"sensor.indoor_location",new="bedroom",duration=5)
        self.listen_state(self.out_bedroom,"sensor.indoor_location",old="bedroom",duration=30)
        self.entities={}

    def in_bedroom(self,*args,**kwargs):
    	if self.get_state("sensor.sleepstatus")=="Awake" or self.now_is_between("07:00:00","23:59:59"):
            self.turn_back_on()

    def out_bedroom(self,*args,**kwargs):
        self.turn_off_running()

    def turn_off_running(self):
        self.entities={"light.bedroom_light":None,"switch.fan":None}
        for k,v in self.entities.items():
            if self.get_state(k)=="on":
                self.log("{} is on,turning it off".format(k))
                self.turn_off(k)
                self.entities[k]="on"


    def turn_back_on(self):
        for k,v in self.entities.items():
            if v=="on":
                self.log("{} was on before,turning back on".format(k))
                self.turn_on(k)
