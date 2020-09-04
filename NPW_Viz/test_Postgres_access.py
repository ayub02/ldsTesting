import psycopg2
from psycopg2 import sql
from matplotlib import pyplot as plt


def decode(_buffer_len, _buffer):
    assert len(_buffer) == _buffer_len
    _pVal = []
    for i in range(8, _buffer_len, 2):
        _pVal.append((_buffer[i] << 8) + _buffer[i+1])
    return _pVal

def format_time(_t):
    _s = _t.strftime('%Y-%m-%d %H:%M:%S.%f')
    return _s[:-3]


conn = psycopg2.connect(dbname='postgres', user='postgres', password='@intech#123', host='10.1.17.113', port='5432')
cursor = conn.cursor()
cursor.execute("SELECT * FROM historytableaug20 where itemid='MKT_out.NPW.ByteArray';")

timestamps = []
rows = cursor.fetchall()
for row in rows:
    timestamps.append(row[2])
print("Timestamps", timestamps)
print('Data fetched')

# buffer = [int(val) for val in rows[0][1].split(",")]
# pVal = decode(1008, buffer)
#
# gettime = format_time(timestamps[1])
# print('gettime', gettime)

# query = sql.SQL("SELECT * FROM historytableaug20 where itemtimestamp= %s;")
#
# cursor.execute(query, (gettime, ))
# print(cursor.fetchall())

# plt.plot(pVal)
# plt.show()
