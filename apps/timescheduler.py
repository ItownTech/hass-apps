
import appdaemon.appapi as appapi
import datetime

class TimeScheduler(appapi.AppDaemon):
    def initialize(self):
      self.log("Hello from AppDaemon Time Scheduler")
      self.register_endpoint(self.api_call,"timeschedule")
       
    def api_call(self,data):
      self.log("{}".format(data))
      def execute(kwargs):
        self.log("Executing Dynamic Callback")
        serv=kwargs.pop('service',None)
        self.log("{}".format(serv))
        self.call_service(serv,**kwargs)
      time=self.parse_time(data.pop('time'))
      if isinstance(time,datetime.time):
        runtime=datetime.datetime.combine(datetime.date.today(),time)
      try:
        self.run_at(execute,runtime,**data)
      except ValueError:
        return {"message":"Failure"},404
      return {"message":"Success"},200
