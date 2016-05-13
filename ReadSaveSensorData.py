import requests
import pexpect
import sys
import time
import json
import datetime

baseURL = "http://130.15.3.145:82/"
access_token = "76ec19bf6bed0e9931cae60ae4c3f60c"
sensor_uuid = "134cfcff-247e-4911-8a0f-dd9cdd88059a" 

def Save_Sensor_Data(access_token , sensor_uuid , reading_value , current_time):

    url = baseURL + "api/sensor/timeseries"
    
    headers = {
                'authorization': "Bearer "+ access_token ,
                'accept': "application/json",
                'cache-control': "no-cache"
               }

    data_array = [
            {
                "sensor_id":sensor_uuid,
                "samples":
                        [
                            {
                                "value":reading_value,"time":current_time
                            }
                        ]
            }
        ]

    result = requests.post(url, data=json.dumps(data_array), headers=headers)

    print(result.text)

    #print url
    #print headers
    #print data_array
    print "*******************"


def floatfromhex(h):
    t = float.fromhex(h)
    if t > float.fromhex('7FFF'):
        t = -(float.fromhex('FFFF') - t)
        pass
    return t


def convertTemperature(objT, ambT):
    m_tmpAmb = ambT/128.0
    Vobj2 = objT * 0.00000015625
    Tdie2 = m_tmpAmb + 273.15
    S0 = 6.4E-14            # Calibration factor
    a1 = 1.75E-3
    a2 = -1.678E-5
    b0 = -2.94E-5
    b1 = -5.7E-7
    b2 = 4.63E-9
    c2 = 13.4
    Tref = 298.15
    S = S0*(1+a1*(Tdie2 - Tref)+a2*pow((Tdie2 - Tref),2))
    Vos = b0 + b1*(Tdie2 - Tref) + b2*pow((Tdie2 - Tref),2)
    fObj = (Vobj2 - Vos) + c2*pow((Vobj2 - Vos),2)
    tObj = pow(pow(Tdie2,4) + (fObj/S),.25)
    tObj = (tObj - 273.15)


bluetooth_adr = "B0:B4:48:D3:07:01"
tool = pexpect.spawn('gatttool -b ' + bluetooth_adr + ' --interactive')
tool.expect('\[LE\]>')
print "Connectin..."
tool.sendline('connect')
# test for success of connect
tool.expect('Connection successful')
#Saad- tool.sendline('char-write-cmd 0x29 01')
tool.sendline('char-write-cmd 0x24 01')

tool.expect('\[LE\]>')
while True:

    time.sleep(5)

    #Saad- tool.sendline('char-read-hnd 0x25')
    tool.sendline('char-read-hnd 0x21')
    tool.expect('descriptor: .*') 
    rval = tool.after.split()
    objT = floatfromhex(rval[2] + rval[1])
    ambT = floatfromhex(rval[4] + rval[3])
    raw_ambient_temp = int( '0x'+ rval[4]+ rval[3], 16)

    ambient_temp_int = raw_ambient_temp >> 2 & 0x3FFF # Shift right, based on from TI
    ambient_temp_celsius = float(ambient_temp_int) * 0.03125 # Convert to Celsius based on info from TI
    ambient_temp_fahrenheit = (ambient_temp_celsius * 1.8) + 32 # Convert to Fahrenheit

    # Call Save Sensor Data into Database
    ##RawData = rval[1] + ' ' + rval[2] + ' ' +  rval[3] + ' ' +  rval[4]
    ##url = 'http://52.38.246.143/iot/iot_addsensordata.php'
    ##payload = {'SensorUUID':'864f0cfc-eefb-4abb-9b27-4c0f4beec4dd' , 'SampleValue':''+str(ambient_temp_celsius)+'' , 'SampleTime':''+str(datetime.datetime.now())+'' , 'SampleTypeID':'1' , 'SampleUnitID':'1' , 'SampleRawData':''+RawData+''}
    ##res = requests.get(url, params=payload)
    #print payload  
    # End Call Save Sensor Data into Database

     
    current_timestamp = int(time.time())
    
    print "Celsius Temperature is: " + str(ambient_temp_celsius)
    print "Fahrenheit Temperature is: " + str(ambient_temp_fahrenheit)
    print "-----------------------------------"

    
    Save_Sensor_Data(access_token , sensor_uuid , ambient_temp_celsius , current_timestamp)
    
    
    #print objT
    #print ambT
    
    #convertTemperature(objT, ambT)
