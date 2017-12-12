import appdaemon.appapi as appapi
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

    def getdevicestatus(self,**kwargs):
        device=kwargs['device']
        try:
            entity_id=self.friendly_names[device.lower()]
        except KeyError:
            return "{} not found".format(device)
        state=self.get_state(entity_id=entity_id)
        return "{} is currently {}".format(device,state)
