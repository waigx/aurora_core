#!/usr/bin/env python

from Tkinter import *
from aurora_core import Manager, Discover

LOCAL_AURORA_DB = 'example_db'

root = Tk()
aur_manager = Manager(LOCAL_AURORA_DB)

def found_handler(aur_raw):
    aur_checkbutton = AuroraCheckbutton(aur_list, text=aur_raw['name'].split('.')[0])
    aur_checkbutton.pack()

def authed_handler(aur):
    for aur_checkbutton in aur_list.winfo_children():
        if aur_checkbutton.name == aur.get.name():
            aur_checkbutton.authed(aur)
    aur_manager.save(aur)

class AuroraCheckbutton(Checkbutton):
    def __init__(self, master, **kargs):
        Checkbutton.__init__(self, master, **kargs)
        self.config(bg='red', state=DISABLED)
        self.name = kargs['text']

    def authed(self, aur):
        self.config(bg='green', state=NORMAL)
        self.aur = aur

aur_list = Frame(root)
aur_list.pack()

for aur in aur_manager.auroras():
    aur_checkbutton = AuroraCheckbutton(aur_list, text=aur.get.name())
    aur_checkbutton.authed(aur)
    aur_checkbutton.pack()

discover = Discover(aur_manager.auroras(), authed_handler=authed_handler, found_handler=found_handler)
discover.start()

root.mainloop()

