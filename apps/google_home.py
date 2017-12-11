import appdaemon.appapi as appapi

class GoogleHome(appapi.AppDaemon):
    def initialize(self):
        self.log("Hello from Google Home")
        self.register_endpoint(self.api_call)
        self.actions=self.get_app("actions")
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


class Actions(appapi.AppDaemon):
    def initialize(self):
        self.log("Hello from Actions")
        self.bootstrap()

    def trigger(self,intent,slots):
        if not hasattr(self,intent):
            return "Action for {} not defined in webhook".format(intent)
        intentfunc=getattr(self,intent)
        res=intentfunc(**slots)
        if not res:
            return "Sorry, there was an error and I could not proceed further"
        return res

    def bootstrap(self):
        entities=self.get_state()
        self.friendly_names={}
        for e,v in entities.items():
            try:
                fn=v["attributes"]["friendly_name"]
                self.friendly_names[fn.lower()]=e.lower()
            except:
                pass

    def input_unknown(self):
        return "Oh!,I didnt understand that"

    def getdevicestatus(self,device):
        try:
            entity_id=self.friendly_names[device.lower()]
        except KeyError:
            return "{} not found".format(device)
        state=self.get_state(entity_id=entity_id)
        return "{} is currently {}".format(device,state)
