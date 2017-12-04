#!/usr/bin/env python

import requests
import json

class Get(object):
    def __init__(self, base_uri):
        self.base_uri = base_uri
        apis = [('all', '/'),
                #('state', '/state'),
                ('on', '/state/on'),
                ('brightness', '/state/brightness'),
                ('hue', '/state/hue'),
                ('saturation', '/state/sat'),
                ('temperature', '/state/ct'),
                ('color_mode', '/state/colorMode'),
                #('effects', '/effects'),
                ('current_effect', '/effects/select'),
                ('all_effects', '/effects/effectsList'),
                ('layout', '/panelLayout/layout')] 
        for api, uri in apis:
            setattr(self, api, self.__get_request(base_uri + uri))

        self.__cached = self.all()
        attrs = [('name', 'name'),
                 ('serial', 'serialNo'),
                 ('model', 'model'),
                 ('firmware', 'firmwareVersion')]
        for name, attr in attrs:
            setattr(self, name, self.__get_cached_value(attr))

    def __get_request(self, uri):
        def req():
            r = requests.get(uri)
            return r.json()
        return req

    def __get_cached_value(self, attr):
        def get():
            return self.__cached[attr]
        return get

    def effect(self, effect_name=None):
        r = requests.put(self.base_uri + '/effects', json.dumps(
                {
                    'write': {
                        'command': 'request',
                        'animName': effect_name or self.current_effect()
                        }
                }))
        return r.json()


class Set(object):
    def __init__(self, base_uri):
        self.base_uri = base_uri

    def __put_request(self, uri, obj):
        r = requests.put(self.base_uri + uri, json.dumps(obj))
    
    def __set_state(self, attr, value):
        self.__put_request('/state',
                {
                    attr: {'value': value}
                })

    def on(self, status):
        self.__set_state('on', bool(status))

    def brightness(self, value=0, inc=0):
        self.__set_state('brightness', value+inc)

    def saturation(self, value=0, inc=0):
        self.__set_state('sat', value+inc)

    def temperature(self, value=0, inc=0):
        self.__set_state('ct', value+inc)

    def effect(self, effect_name):
        self.__put_request('/effects', {'select': effect_name})


class Aurora(object):
    def __init__(self, raw, auth):
        uri = 'http://%s:%d/api/v1/%s' % (raw['server'], raw['port'], auth['auth_token'])
        self.uri = uri
        self.raw = raw
        self.auth = auth
        self.get = Get(uri)
        self.set = Set(uri)

    def delete(self):
        requests.delete(self.uri)

    def identify(self):
        requests.put(self.uri + 'identify')
