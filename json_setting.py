"""Json File Reader
Reads settings from a JSON format file
""" 

import json

class JsonSetting:
    '''JSON File reader'''

    def __init__(self, settingFilePath="./settings.json"):
        '''Opens a JSON format file'''
        self.setting = json.loads(open(settingFilePath,'r').read())

    def get(self, settingName):
        '''Get a value for a given key'''
        return self.setting[settingName]

if __name__ == "__main__":
    settingStringPath = './settings.json'
    self.setting = json.loads(open(settingFilePath,'r').read())
    print self.setting    
