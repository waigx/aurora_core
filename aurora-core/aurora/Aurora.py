#!/usr/bin/env python

import requests

class Get(object):
    def __init__(self, base_uri):
       apis = [('all', '/'),
               ('state', '/state'),
               ('on', '/state/on'),
               ('brightness', '/state/brightness'),
               ('hue', '/state/hue'),
               ('saturation', '/state/sat'),
               ('temperature', '/state/ct'),
               ('effects', '/effects'),
               ('select_effect', '/effects/select'),
               ('all_effects', '/effects/effectsList')] 
       for api, uri in apis:
           setattr(self, api, self._get(base_uri + uri))

    def _get(self, uri):
        def req():
            r = requests.get(uri)
            return r.json()
        return req

class Aurora(object):
    def __init__(self, uri):
        self.uri = uri
        self.get = Get(uri)


a = Aurora('')
print a.get.effects()['effectsList']
