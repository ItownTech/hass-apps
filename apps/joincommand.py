
import appdaemon.appapi as appapi

class Join(appapi.AppDaemon):
    def initialize(self):
    	self.log("Hello from AppDaemon Join")
    	self.listen_state(self.send_command, "input_text.text1")

    def send_command(self, entity, attribute, old, new, kwargs):
        if new=="":
            return
        self.log(new)

        r=requests.get("https://joinjoaomgcd.appspot.com/_ah/api/messaging/v1/sendPush?text={}&deviceId=7d3d1060b809416cad7d3c0076eb71ef&apikey=ae854ef404d341dc82fca9514642fc26".format(new))
        if r.status_code!=200:
            self.set_state("input_text.text1",state="Command Failed")
            self.log("Failed to send message {}".format(new))
        self.set_state("input_text.text1",state="")
        self.log(" Message Sent: {}".format(new))
