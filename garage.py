import appdaemon.appapi as appapi

class Garage(appapi.AppDaemon):
    def initialize(self):
        self.log("Hello from AppDaemon garage")
        self.listen_state(self.open_garage,"sensor.state",new="NearHome",old="Outside")
        self.listen_state(self.close_garage,"sensor.state",new="NearHome",old="Home")
        self.listen_state(self.open_garage,"sensor.state",new="Home",old="Outside")
        self.listen_state(self.close_garage,"sensor.state",new="Outside",old="Home")
        self.listen_state(self.close_garage,"cover.garage",new="open",duration=3*60)
        self.listen_state(self.closed,"cover.garage",new="closed")
        self.listen_state(self.opened,"cover.garage",new="open")

    def open_garage(self, entity, attribute, old, new, kwargs):
        garage_state=self.get_state("cover.garage")
        self.log("garage is now {}".format(garage_state))
        if self.get_state("input_boolean.garage_flag")=="on" and self.now_is_between("16:30:00", "21:00:00"):
            self.open()
            self.turn_off(entity_id="input_boolean.garage_flag")

    def close_garage(self, entity, attribute, old, new, kwargs):
        garage_state=self.get_state("cover.garage")
        if garage_state=="open" and self.now_is_between("07:00:00", "21:00:00"):
             self.close()

    def open(self):
        self.log("Opening garage")
        self.call_service("cover/open_cover",entity_id="cover.garage")

    def close(self):
        self.log("Closing garage")
        self.call_service("cover/close_cover",entity_id="cover.garage")

    def opened(self, entity, attribute, old, new, kwargs):
        self.get_app("utils").fb_notify_all(title="Jarvis",message="Garage is now open")
        self.get_app("utils").announce("Sir, the garage is now open")

    def closed(self, entity, attribute, old, new, kwargs):
        self.get_app("utils").fb_notify_all(title="Jarvis",message="Garage is now closed")
        self.get_app("utils").announce("Sir, the garage is now closed")
