import requests
import json


# Generate Access Token

def Get_Access_Token(client_id , client_secret):

    url = "http://130.15.3.145:82/oauth/access_token/client_id="+client_id+"/client_secret="+client_secret

    headers = {
        'cache-control': "no-cache"
        }

    response = requests.request("GET", url, headers=headers)
    data = response.json()

    access_token = data['access_token']
    
    return access_token



# Create Sensor
def Create_Sensor(access_token):
        
    url = "http://130.15.3.145:82/api/sensor"

    params = {"name":"Sensor-123","identifier":"Sensor-123-Identifier","building":"Goodwin-Building"}
   
    headers = {
        'authorization': "Bearer "+ access_token ,
        'accept': "application/json",
        'cache-control': "no-cache"
        }
    
    #result = requests.request("POST", url, headers=headers, params=params)

    result = requests.post(url, data=json.dumps(params), headers=headers)
    
    sensor_uuid = result['uuid']

    return sensor_uuid

   

access_token = Get_Access_Token("liWDTDiNZzsEVSTo53KWJJLo4N97p8Iw72eBlV8I" , "3CzlOPHis2tZCqfzoScyk8RhKUJ8AuiMcHbBGY7JHITD02sBGA")

sensor_uuid = Create_Sensor(access_token)




