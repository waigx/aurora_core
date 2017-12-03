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
            setattr(self, api, self.__get_value(base_uri + uri))

    def __get_value(self, uri):
        def req():
            r = requests.get(uri)
            return r.json()
        return req
    
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
    def __init__(self, uri):
        self.uri = uri
        self.get = Get(uri)
        self.set = Set(uri)


a = Aurora('')
print a.set.effect('Snowfall')
