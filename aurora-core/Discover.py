#!/usr/bin/env python

import requests
import time
import threading
from aurora import Aurora 
from zeroconf import ServiceBrowser, Zeroconf

class DiscoverHandler(object):
    def __init__(self, callback):
        self.callback = callback

    def remove_service(self, zeroconf, type, name):
        pass

    def add_service(self, zeroconf, type, name):
        raw_service_info = zeroconf.get_service_info(type, name)
        aurora_info = {attr: getattr(raw_service_info, attr, '') for attr in 
                        ('type', 'name', 'address', 'port', 'weight', 'priority', 'server', 'properties')}
        self.callback(aurora_info)


class Discover(object):
    def __init__(self, existed, found_handler, authed_handler, failed_handler):
        self.custom_found_handler = found_handler
        self.custom_authed_handler = authed_handler
        self.existed_aurora = [aurora['raw']['name'] for aurora in existed]
        self.aurora_info_dict = {}
        self.current_authed = None
        self.thread = threading.Thread(target=self.discover_and_auth)

    def start_discover(self):
        self.thread.start()

    def discover_and_auth(self):
        self.zeroconf = Zeroconf()
        self.handler = DiscoverHandler(self.discovered_callback)
        self.browser = ServiceBrowser(self.zeroconf, "_nanoleafapi._tcp.local.", self.handler)

        while not self.current_authed:
            time.sleep(0.2)
            for aurora, info in self.aurora_info_dict.items():
                new_auth_req = requests.post('http://%s:%d/api/v1/new' % (info['server'], info['port']))
                if new_auth_req.status_code == 200:
                    self.current_authed = info
                    self.authed_callback(info, new_auth_req.json())
                    break;

        self.zeroconf.close()

    def discovered_callback(self, aurora_info):
        if aurora_info['name'] not in self.existed_aurora:
            self.aurora_info_dict[aurora_info['name']] = aurora_info
            self.custom_found_handler(aurora_info)

    def authed_callback(self, aurora_info, auth_data):
        self.existed_aurora.append(aurora_info['name'])
        self.custom_authed_handler(Aurora(aurora_info, auth_data))
