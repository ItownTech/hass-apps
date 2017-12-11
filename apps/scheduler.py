import appdaemon.appapi as appapi
import datetime

class Scheduler(appapi.AppDaemon):
   def initialize(self):
       self.log("Hello from AppDaemon Scheduler")
       self.register_endpoint(self.api_call,"schedule")

   def api_call(self,data):
       self.log("{}".format(data))
       def execute(kwargs):
           self.log("Executing Dynamic Callback")
           serv=kwargs.pop('service',None)
           self.call_service(serv,**kwargs)
       delay=data.pop("delay",0)
       self.run_in(execute,delay,**data)
       return {"message":"Success"},200

