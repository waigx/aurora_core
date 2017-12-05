#!/usr/bin/env python

from aurora_core import Discover

def authed_handler(aurora):
    print aurora.get.name(), aurora.get.serial()
    aurora.set.brightness(50)

discover = Discover([], authed_handler)
discover.start()
