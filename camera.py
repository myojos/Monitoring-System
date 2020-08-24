import os
import yaml
import models
from alert import Alert
from datetime import datetime

CONFIG_DIR = 'config'
LOGS_DIR = 'logs'


class Camera:
    def __init__(self, room_name):
        self.rome_name = room_name
        dir_path = os.path.dirname(os.path.realpath(__file__))

        config_file = os.path.join(dir_path, CONFIG_DIR)
        config_file = os.path.join(config_file, '{room}.yaml'.format(room=room_name))
        if not os.path.exists(config_file):
            print('Failed to initialize room {room}'.format(room=room_name))
        with open(config_file, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        if 'rules' in config:
            config = config['rules']
        self.alerts = {}
        for rule_name in config:
            rule = config[rule_name]
            self.alerts[rule_name] = Alert(rule)

        logs_path = os.path.join(dir_path, LOGS_DIR)
        self.values_log = os.path.join(logs_path, 'values-{room}.log'.format(room=room_name))
        self.alert_log = os.path.join(logs_path, 'alerts.log')
        pass

    def check(self, img_path, frame):
        for alert_name in self.alerts:
            alert = self.alerts[alert_name]
            if alert.check(img_path, frame):
                with open(self.alert_log, 'a') as log:
                    log.write('[{time}] - [{room}] - [{alert}]\n'
                              .format(room=self.rome_name, alert=alert_name,
                                      time=datetime.now().strftime("%d %B %Y %H:%M:%s")))
