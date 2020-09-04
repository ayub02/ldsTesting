from tkinter import *
import psycopg2
from psycopg2 import sql
from functools import partial
from matplotlib import pyplot as plt


def decode_time(_buffer_len, _buffer):
    assert len(_buffer) == _buffer_len
    if _buffer[0] >= 90:
        year = '19' + hex(_buffer[0])[2:]
    else:
        year = '20' + hex(_buffer[0])[2:]
    month = hex(_buffer[1])[2:]
    day = hex(_buffer[2])[2:]
    hour = hex(_buffer[3])[2:]
    minute = hex(_buffer[4])[2:]
    second = hex(_buffer[5])[2:]
    millisecond = hex(_buffer[6])[2:] + hex(_buffer[7])[2]

    return year + '-' + month + '-' + day + '  ' + hour + ':' + minute + ':' + second + '.' + millisecond


def decode(_buffer_len, _buffer):
    assert len(_buffer) == _buffer_len
    _pVal = []
    for i in range(8, _buffer_len, 2):
        _pVal.append((_buffer[i] << 8) + _buffer[i + 1])
    return _pVal


def format_time(_t):
    _s = _t.strftime('%Y-%m-%d %H:%M:%S.%f')
    return _s[:-3]


def get_timestamps(_cursor, _tag):
    _query = sql.SQL("SELECT * FROM historytableaug20 where itemid= %s ORDER BY itemtimestamp DESC;")
    _cursor.execute(_query, (_tag,))
    _rows = _cursor.fetchall()
    if _rows:
        _timestamps = []
        for row in _rows:
            _timestamps.append(row[2])
    else:
        return ["Not found"]
    return _timestamps


def get_all_timestamps(_cursor):
    global MKT_timestamps, MOV60_timestamps, BV61_timestamps, BV62_timestamps, BV63_timestamps, BV64_timestamps
    global BV65_timestamps, BV66_timestamps, MOV67_timestamps, KBS_timestamps
    MKT_timestamps = get_timestamps(_cursor, 'MKT_out.NPW.ByteArray')
    MOV60_timestamps = get_timestamps(_cursor, 'MOV60.NPW.ByteArray')
    BV61_timestamps = get_timestamps(_cursor, 'BV61.NPW.ByteArray')
    BV62_timestamps = get_timestamps(_cursor, 'BV62.NPW.ByteArray')
    BV63_timestamps = get_timestamps(_cursor, 'BV63.NPW.ByteArray')
    BV64_timestamps = get_timestamps(_cursor, 'BV64.NPW.ByteArray')
    BV65_timestamps = get_timestamps(_cursor, 'BV65.NPW.ByteArray')
    BV66_timestamps = get_timestamps(_cursor, 'BV66.NPW.ByteArray')
    MOV67_timestamps = get_timestamps(_cursor, 'MOV67.NPW.ByteArray')
    KBS_timestamps = get_timestamps(_cursor, 'KBS_in.NPW.ByteArray')

    draw_dropdown()


def plot(station):
    global tag_dict
    _timestamp_dict = {'MKT': MKT_default.get(), 'MOV60': MOV60_default.get(), 'BV61': BV61_default.get(),
                       'BV62': BV62_default.get(), 'BV63': BV63_default.get(), 'BV64': BV64_default.get(),
                       'BV65': BV65_default.get(), 'BV66': BV66_default.get(), 'MOV67': MOV67_default.get(),
                       'KBS': KBS_default.get()}

    query = sql.SQL("SELECT * FROM historytableaug20 where itemid=%s AND itemtimestamp= %s;")
    cursor.execute(query, (tag_dict[station], _timestamp_dict[station],))
    element = cursor.fetchall()
    assert len(element) == 1

    plt.figure()
    plt.ylabel('Pressure (Pa)')
    buffer = [int(val) for val in element[0][1].split(",")]
    plt.title(station + '       ' + decode_time(1008, buffer))
    plt.plot(decode(1008, buffer))
    plt.show()


def draw_dropdown():
    MKT_default.set(MKT_timestamps[0])
    MOV60_default.set(MOV60_timestamps[0])
    BV61_default.set(BV61_timestamps[0])
    BV62_default.set(BV62_timestamps[0])
    BV63_default.set(BV63_timestamps[0])
    BV64_default.set(BV64_timestamps[0])
    BV65_default.set(BV65_timestamps[0])
    BV66_default.set(BV66_timestamps[0])
    MOV67_default.set(MOV67_timestamps[0])
    KBS_default.set(KBS_timestamps[0])

    d_MKT = OptionMenu(root, MKT_default, *MKT_timestamps)
    d_MOV60 = OptionMenu(root, MOV60_default, *MOV60_timestamps)
    d_BV61 = OptionMenu(root, BV61_default, *BV61_timestamps)
    d_BV62 = OptionMenu(root, BV62_default, *BV62_timestamps)
    d_BV63 = OptionMenu(root, BV63_default, *BV63_timestamps)
    d_BV64 = OptionMenu(root, BV64_default, *BV64_timestamps)
    d_BV65 = OptionMenu(root, BV65_default, *BV65_timestamps)
    d_BV66 = OptionMenu(root, BV66_default, *BV66_timestamps)
    d_MOV67 = OptionMenu(root, MOV67_default, *MOV67_timestamps)
    d_KBS = OptionMenu(root, KBS_default, *KBS_timestamps)

    d_MKT.grid(row=0, column=1)
    d_MOV60.grid(row=1, column=1)
    d_BV61.grid(row=2, column=1)
    d_BV62.grid(row=3, column=1)
    d_BV63.grid(row=4, column=1)
    d_BV64.grid(row=5, column=1)
    d_BV65.grid(row=6, column=1)
    d_BV66.grid(row=7, column=1)
    d_MOV67.grid(row=8, column=1)
    d_KBS.grid(row=9, column=1)


tag_dict = {'MKT': 'MKT_out.NPW.ByteArray', 'MOV60': 'MOV60.NPW.ByteArray', 'BV61': 'BV61.NPW.ByteArray',
            'BV62': 'BV62.NPW.ByteArray', 'BV63': 'BV63.NPW.ByteArray', 'BV64': 'BV64.NPW.ByteArray',
            'BV65': 'BV65.NPW.ByteArray', 'BV66': 'BV66.NPW.ByteArray', 'MOV67': 'MOV67.NPW.ByteArray',
            'KBS': 'KBS_in.NPW.ByteArray'}

conn = psycopg2.connect(dbname='postgres', user='postgres', password='@intech#123', host='10.1.17.113', port='5432')
cursor = conn.cursor()

tag = 'BV66.NPW.ByteArray'

root = Tk()
root.title('NPW visualization')
root.geometry("300x400")

MKT_timestamps = ['Select ... ']
MOV60_timestamps = ['Select ... ']
BV61_timestamps = ['Select ... ']
BV62_timestamps = ['Select ... ']
BV63_timestamps = ['Select ... ']
BV64_timestamps = ['Select ... ']
BV65_timestamps = ['Select ... ']
BV66_timestamps = ['Select ... ']
MOV67_timestamps = ['Select ... ']
KBS_timestamps = ['Select ... ']

MKT_default = StringVar()
MOV60_default = StringVar()
BV61_default = StringVar()
BV62_default = StringVar()
BV63_default = StringVar()
BV64_default = StringVar()
BV65_default = StringVar()
BV66_default = StringVar()
MOV67_default = StringVar()
KBS_default = StringVar()

L_MKT = Label(root, text="MKT")
L_MOV60 = Label(root, text="MOV60")
L_BV61 = Label(root, text="BV61")
L_BV62 = Label(root, text="BV62")
L_BV63 = Label(root, text="BV63")
L_BV64 = Label(root, text="BV64")
L_BV65 = Label(root, text="BV65")
L_BV66 = Label(root, text="BV66")
L_MOV67 = Label(root, text="MOV67")
L_KBS = Label(root, text="KBS")

L_MKT.grid(row=0, column=0)
L_MOV60.grid(row=1, column=0)
L_BV61.grid(row=2, column=0)
L_BV62.grid(row=3, column=0)
L_BV63.grid(row=4, column=0)
L_BV64.grid(row=5, column=0)
L_BV65.grid(row=6, column=0)
L_BV66.grid(row=7, column=0)
L_MOV67.grid(row=8, column=0)
L_KBS.grid(row=9, column=0)

get_all_timestamps(cursor)

MKT_default.set(MKT_timestamps[0])
MOV60_default.set(MOV60_timestamps[0])
BV61_default.set(BV61_timestamps[0])
BV62_default.set(BV62_timestamps[0])
BV63_default.set(BV63_timestamps[0])
BV64_default.set(BV64_timestamps[0])
BV65_default.set(BV65_timestamps[0])
BV66_default.set(BV66_timestamps[0])
MOV67_default.set(MOV67_timestamps[0])
KBS_default.set(KBS_timestamps[0])

d_MKT = OptionMenu(root, MKT_default, *MKT_timestamps)
d_MOV60 = OptionMenu(root, MOV60_default, *MOV60_timestamps)
d_BV61 = OptionMenu(root, BV61_default, *BV61_timestamps)
d_BV62 = OptionMenu(root, BV62_default, *BV62_timestamps)
d_BV63 = OptionMenu(root, BV63_default, *BV63_timestamps)
d_BV64 = OptionMenu(root, BV64_default, *BV64_timestamps)
d_BV65 = OptionMenu(root, BV65_default, *BV65_timestamps)
d_BV66 = OptionMenu(root, BV66_default, *BV66_timestamps)
d_MOV67 = OptionMenu(root, MOV67_default, *MOV67_timestamps)
d_KBS = OptionMenu(root, KBS_default, *KBS_timestamps)

d_MKT.grid(row=0, column=1)
d_MOV60.grid(row=1, column=1)
d_BV61.grid(row=2, column=1)
d_BV62.grid(row=3, column=1)
d_BV63.grid(row=4, column=1)
d_BV64.grid(row=5, column=1)
d_BV65.grid(row=6, column=1)
d_BV66.grid(row=7, column=1)
d_MOV67.grid(row=8, column=1)
d_KBS.grid(row=9, column=1)

plot_MKT = Button(root, text="Plot", command=partial(plot, 'MKT'))
plot_MOV60 = Button(root, text="Plot", command=partial(plot, 'MOV60'))
plot_BV61 = Button(root, text="Plot", command=partial(plot, 'BV61'))
plot_BV62 = Button(root, text="Plot", command=partial(plot, 'BV62'))
plot_BV63 = Button(root, text="Plot", command=partial(plot, 'BV63'))
plot_BV64 = Button(root, text="Plot", command=partial(plot, 'BV64'))
plot_BV65 = Button(root, text="Plot", command=partial(plot, 'BV65'))
plot_BV66 = Button(root, text="Plot", command=partial(plot, 'BV66'))
plot_MOV67 = Button(root, text="Plot", command=partial(plot, 'MOV67'))
plot_KBS = Button(root, text="Plot", command=partial(plot, 'KBS'))
Refresh = Button(root, text="Refresh All", command=partial(get_all_timestamps, cursor))

plot_MKT.grid(row=0, column=2)
plot_MOV60.grid(row=1, column=2)
plot_BV61.grid(row=2, column=2)
plot_BV62.grid(row=3, column=2)
plot_BV63.grid(row=4, column=2)
plot_BV64.grid(row=5, column=2)
plot_BV65.grid(row=6, column=2)
plot_BV66.grid(row=7, column=2)
plot_MOV67.grid(row=8, column=2)
plot_KBS.grid(row=9, column=2)
Refresh.grid(row=10, column=1)

root.mainloop()
