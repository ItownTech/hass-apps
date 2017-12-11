import re
from datetime import datetime, timedelta

import appdaemon.appapi as appapi

#
# Utility Functions are found here, so they need not be duplicated
#    in all other apps.
#

class utils(appapi.AppDaemon): #it's ok to break convention, with good reason

    def initialize(self):
        self.sriram_phone="+16314287693"
        self.nirmit_phone="+16316453568"
        self.all_phone=[self.sriram_phone,self.nirmit_phone]

    def announce(self,message):
        prevol=self.get_state("media_player.bedroom_home",attribute="volume_level")
        self.log("{}".format(prevol))
        self.call_service("media_player/volume_set",entity_id="media_player.bedroom_home",volume_level=0.6)
        self.call_service("tts/amazon_polly_say",entity_id="media_player.bedroom_home",message=message)
        self.fire_event("schedule",service="media_player/volume_set",entity_id="media_player.bedroom_home",volume_level=prevol,delay=30)

    def fb_notify(self,title=None,message=None):
        self.call_service("notify/facebook",title=title,message=message,target=self.sriram_phone)

    def input_boolean_switch(self,switch,entity_id):
        serv="input_boolean/{}".format("turn_"+switch)
        self.call_service(service=serv,entity_id=entity_id)

    def fb_notify_all(self,title,message):
        self.call_service("notify/facebook",title=title,message=message,target=self.all_phone)

    def lights_on(self):
    	self.turn_on("light.main_light",brightness_pct=100)

    def lights_off(self):
        self.turn_off("light.main_light")

    def mqtt_publish(self,topic,payload,retain=False,qos=0):
        self.call_service("mqtt/publish",topic=topic,payload=payload,qos=qos,retain=retain)
