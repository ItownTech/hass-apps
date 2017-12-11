
import appdaemon.appapi as appapi

class Announce(appapi.AppDaemon):
  def initialize(self):
    self.log("Hello from AppDaemon Announce")
    self.listen_event(self.announce,"announce")

  def announce(self, event_name, data, kwargs):
    message=data['data']['message']
    self.get_app('utils').announce(message)