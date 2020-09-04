import pandas as pd
from datetime import datetime, timedelta
import paho.mqtt.client as mqtt
from time import sleep
import configparser


class define_time:
    def __init__(self, year, month, day, hour, minute, second, microsecond):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.microsecond = microsecond


def publislhBuffer(buff, _topic=None):
    print(buff)
    # print('publishing buffer of len:', len(buff))
    mqttclient = mqtt.Client('c1', False)
    # print("connecting to broker")
    mqttclient.connect(host=mqttHost, port=mqttPort)    # connect to broker
    ret = mqttclient.publish(_topic, payload=buff, qos=1)
    # ret.wait_for_publish()
    # print('published returned: ', ret.rc)
    sleep(0.5)
    mqttclient.disconnect()

# Convert a two digit decimal number into binary coded decimal representation
def bcd(val):
    res = val % 100   # we can BCD encode only two digits in one byte
    res = int(res/10) * 0x10 + res % 10
    return int(res)


# Creates an an array of 8-byte values to represent timestamp buffer as described above
def createTimeBuffer(t1):
    timeBuffer = [bcd(t1.year-2000), bcd(t1.month), bcd(t1.day),
    bcd(t1.hour), bcd(t1.minute), bcd(t1.second),
    bcd(int(t1.microsecond/10000)),
    bcd((int((t1.microsecond-int(t1.microsecond/10000)*10000)/1000)*10)) + ([2, 3, 4, 5, 6, 7, 1][t1.weekday()])]
    return timeBuffer


# generates a buffer with 200 hypothetical 2-byte pressure values
def createDataBuffer():
    # return struct.pack('>200H', *original2byteDataArray)
    dataBuffer = []
    for x in original2byteDataArray:
        dataBuffer += [(x/256) % 256, x % 256]
    return dataBuffer


def convertToJsonArray(buff):
    return """{"NPW_array":[""" + ','.join(str(int(x)) for x in completeDataBuffer) + "]}"


# Reading configurations
config = configparser.ConfigParser()
config.read('../config/NPW.ini')

# Kepware
mqttHost = config['Kepware']['mqttHost']
mqttPort = int(config['Kepware']['mqttPort'])


dict1 = {'MKT_out': 0, 'MOV60': 397.5, 'BV61': 18691, 'BV62': 20097, 'BV63': 42458, 'BV64': 42879,
         'BV65': 90166.6, 'BV66': 90447.7, 'MOV67': 150005, 'KBS_in': 150502.5}
cases = pd.read_excel('../data/NPW_cases.xlsx', sheet_name=0)

# Stations on which to send leak wave data
topics = [val.strip() for val in config['Scenarios']['topics'].split(',')]

# Type of leak wave
case_name = config['Scenarios']['case_name']
case = cases[case_name].tolist()

# Leak location for which pressure wave time stamps will be generated
leak_location = float(config['Scenarios']['leak_location'])                        # m

# Speed of sound to be used for generating time stamps
speedOfsound = float(config['Scenarios']['speedOfsound'])                      # m/s

# Current time to used as zero reference
now_time = datetime.now()
print('Original:', now_time)

# Distance of stations relative to leak location
rel_distances = {key: abs(val-leak_location) for key, val in dict1.items()}

# Arrival time of wave at each station relative to time at which the leak is generated (0 seconds)
rel_times = {key: val/speedOfsound for key, val in rel_distances.items()}

for i, topic in enumerate(topics):
    # original2byteDataArray = [60e3]*100+[60e3-6*val for val in range(400)]
    original2byteDataArray = [val*1000 for val in case]
    completeDataBuffer = createTimeBuffer(now_time+timedelta(seconds=rel_times[topic])) + createDataBuffer()
    print(now_time+timedelta(seconds=rel_times[topic]))
    print(len(completeDataBuffer))
    byteArrayJson = convertToJsonArray(completeDataBuffer)
    print(byteArrayJson)
    # np.savetxt('array'+str(i)+'.csv', byteArrayJson, delimiter=',')
    publislhBuffer(byteArrayJson, topic)


# print(len(original2byteDataArray))
# plt.plot(original2byteDataArray)
# plt.show()
