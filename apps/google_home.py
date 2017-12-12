import appdaemon.appapi as appapi

class GoogleHome(appapi.AppDaemon):
    def initialize(self):
        self.log("Hello from Google Home")
        self.register_endpoint(self.api_call)
        self.actions=self.get_app("actions")
        self.log(self.actions)
    def api_call(self,data):
        intent=self.get_apiai_intent(data).lower()
        if "." in intent:
            intent=intent.replace(".","_")
        slots=self.get_apiai_slot_value(data)
        self.log("got {} and {}".format(intent,slots))
        res=self.actions.trigger(intent,slots)
        return self.response(res),200

    def response(self,text):
        return self.format_apiai_response(text)
