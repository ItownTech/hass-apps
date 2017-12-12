import appdaemon.appapi as appapi
import os
import re
from datetime import datetime

#
# App to display a Persistent Notification on the Front End whenever AppDaemon has encountered
# an error
#
# Args: (set these in appdaemon.cfg)
# path_to_errorlog = full path of location of errorlog
# refresh_interval = time in seconds to check for new errors
#
#
# EXAMPLE appdaemon.cfg entry below
#
# # Apps
#
# [error_notifier]
# module = error_notifier
# class = ErrorNotifier
# path_to_errorlog = /home/homeassistant/.homeassistant/appdaemon/conf/errfile.log
# refresh_interval = 5
#

class ErrorNotifier(appapi.AppDaemon):

    def initialize(self):
        self.seen_errors = []
        self.last_update = datetime(2013, 9, 13)

        self.run_every(self.get_last_file_update, start=self.datetime(),
                                                  interval=int(self.args['refresh_interval']))

    def get_last_file_update(self, kwargs):
        last_update_seconds = os.stat(self.args['path_to_errorlog']).st_mtime
        last_update = datetime.fromtimestamp(last_update_seconds)

        if last_update > self.last_update:
            self.last_update = last_update

            if os.stat(self.args['path_to_errorlog']).st_size > 0:
                self.compare_errors()
            else:
                self.seen_errors = []

    def compare_errors(self):
        re_time = re.compile('(.*). WARNING Traceback .*')
        re_app = re.compile('apps/(.*).py')
        re_func = re.compile(', in (.*)')
        re_line = re.compile('line (\d{1,})')
        re_error = re.compile('(.*(Error|Iteration|Warning)): (.*)')

        for error in self.get_errorlog_content():

            dt_string = re_time.search(error).group(1)
            dt_object = datetime.strptime(dt_string, '%Y-%m-%d %H:%M:%S.%f')

            app = re_app.search(error).group(1)
            func = re_func.findall(error)[-1]
            line = re_line.findall(error)[-1]
            exc = re_error.search(error).group(1)
            desc = re_error.search(error).group(3)

            full_error = '{}.{}:{} {}: {}'.format(app, func, line, exc, desc)

            if full_error not in self.seen_errors:
                self.seen_errors.append(full_error)
                self.notify_frontend(dt=dt_object,
                                     app=app,
                                     func=func,
                                     line=line,
                                     exc=exc,
                                     desc=desc)

    def get_errorlog_content(self):
        with open(self.args['path_to_errorlog']) as f:
            all_errors = f.read()
            all_errors_list = all_errors.split('\n\n')

            for error in all_errors_list[:-1]:
                if error is not None:
                    yield error

    def notify_frontend(self, dt, app, func, line, exc, desc):
        pretty_timestamp = dt.strftime('%X on %x')
        self.call_service('notify/telegram',
            title="[AppDaemon] {}".format(exc),
            message=("At {}, in app {}, in def {}, on line {}, {}"
                     .format(pretty_timestamp, app, func, line, desc)))
        self.call_service('persistent_notification/create',
            title="[AppDaemon] {}".format(exc),
            message=("At {}, in app {}, in def {}, on line {}, {}"
                     .format(pretty_timestamp, app, func, line, desc)))
