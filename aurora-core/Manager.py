#!/usr/bin/env python

import pickle
import os.path
import requests
from aurora import Aurora

class Manager(object):
    def __init__(self, db_file_path):
        if not os.path.isfile(db_file_path):
            with open(db_file_path, 'wb') as raw_db:
                pickle.dump([], raw_db)
            
        with open(db_file_path, 'rb') as raw_db:
            self.raw_auroras = pickle.load(raw_db)
        self.db_file_path = db_file_path

    def __raw_to_aurora(self, raw_aurora):
        return Aurora(raw_aurora['raw'], raw_aurora['auth'])

    def __aurora_to_raw(self, aurora):
        return {
            'raw': aurora.raw,
            'auth': aurora.auth,
        }
 
    def auroras(self):
        return [self.__raw_to_aurora(raw_aurora) for raw_aurora in self.raw_auroras]

    def save(self, aurora):
        raw_aurora = self.__aurora_to_raw(aurora)
        if raw_aurora not in self.raw_auroras:
            self.raw_auroras.append(raw_aurora)
        with open(self.db_file_path, 'wb') as raw_db:
            pickle.dump(self.raw_auroras, raw_db)

    def delete(self, aurora):
        raw_aurora = self.__aurora_to_raw(aurora)
        aurora.delete()
        self.raw_auroras.remove(raw_aurora)
        with open(self.db_file_path, 'wb') as raw_db:
            pickle.dump(self.raw_auroras, raw_db)
