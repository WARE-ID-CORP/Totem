import configparser
import os
import json

class Conf():
    def __init__(self, path="/home/wareid/Totem/"):
        self.config = {}
        with open(path+'Config.json') as json_data:
            self.config = json.load(json_data)
            print(str(self.config))