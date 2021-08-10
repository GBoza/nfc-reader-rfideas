import time
import ctypes

pcproxlib = ctypes.CDLL('../lib/64/libhidapi-hidraw.so', mode = ctypes.RTLD_GLOBAL)
pcproxlib = ctypes.CDLL('../lib/64/libpcProxAPI.so', mode = ctypes.RTLD_GLOBAL)

def setDevTypeSrch(deviceType):
    """
    Helper of  usbconnect, Will restrict
    the device search to a particular category
    for example.
    Device Type could be one of following
    0 : To search only USB devices
    1 :  To Search Serial RS-232 only.
    -1 : Both USB and serial devices.
    This function will return true in case of
    success false otherwise.
    """
    # it's important that we convert data type from
    # python to C properly other wise results are random.
    pcproxlib.SetDevTypeSrch.restype = ctypes.c_short;
    rc = pcproxlib.SetDevTypeSrch(ctypes.c_short(deviceType))
    if rc == 1:
        return True
    else:
        return False

def usbConnect():
    """
    Will return True in case success false otherwise.
    Will open connection to all rfidea's readers/devices
    in onces.

    Individual device can be accessed by using setActiveDev first
    then call other functions.
    """
    pcproxlib.usbConnect.restype = ctypes.c_short;
    rc = pcproxlib.usbConnect()
    if rc == 1:
        return True;
    return False

def usbDisconnect():
    """
    Will return True in case success false otherwise.
    As per API documentation USBDisconnect always returns
    true.
    It will close the handle to all rfidea's devices, should be
    called during clean up.
    """
    pcproxlib.USBDisconnect.restype = ctypes.c_short;
    rc = pcproxlib.USBDisconnect()
    if rc == 1:
        return True
    return False

def getLibVersion():
    """
    Will return the SDK version in following format
    <Major>.<Minor>.<Dev>.
    In case of error will return None
    """
    major = ctypes.c_short()
    minor = ctypes.c_short()
    dev = ctypes.c_short()
    pcproxlib.GetLibVersion.restype = ctypes.c_short;
    rc = pcproxlib.GetLibVersion(byref(major), byref(minor), byref(dev))
    if rc == 1:
        sdk_version = str(major.value) + "." + str(minor.value) + "." \
        + str(dev.value)
        return sdk_version
    return None

def getLUID():
    """
    Will return the LUID of active device/Reader
    """
    pcproxlib.GetLUID.restype = ctypes.c_int;
    luid = pcproxlib.GetLUID()
    return luid

def getDevCnt():
    """
    Will Return the total number of
    connected rfidea's readers.
    """
    pcproxlib.GetDevCnt.restype = ctypes.c_short
    nbOfDevices = pcproxlib.GetDevCnt()
    return nbOfDevices

def getPartNumber():
    """
    Api will return the part number of
    active device and None in case of failure.
    """
    #configure return type of getPartNumberString
    # to pointer to char
    pcproxlib.getPartNumberString.restype = ctypes.POINTER(ctypes.c_char)
    partNb_p = pcproxlib.getPartNumberString()
    if partNb_p == None:
        return None;
    else:
     return ctypes.string_at(partNb_p).decode('utf-8')

def getVidPidVendorName():
    """
    Will return None in case of error other wise will return
    the VID PID and product name in following format
    <VID>:<PID> <product name>
    """
    pcproxlib.GetVidPidVendorName.restype = ctypes.POINTER(ctypes.c_char)
    vid_pid_vendor_name_p = pcproxlib.GetVidPidVendorName()
    if vid_pid_vendor_name_p == None:
        return None
    else:
        return ctypes.string_at(vid_pid_vendor_name_p).decode('utf-8')

def setActiveDev(activeIndex):
    """
    Will return true if able to set
    active device to give device false otherwise
    """
    activeDevice = ctypes.c_short(activeIndex)
    pcproxlib.SetActDev.restype = ctypes.c_short
    rc = pcproxlib.SetActDev(activeDevice)
    if rc == 1:
        return True
    else:
        return False

def getActiveID32():
    """
    Will return a tuple consisting number of bits
    read and actual data. Minimum 8 byte of data will
    be returned.
    """
    rawData = ""
    buffer_size = ctypes.c_short(32);
    pcproxlib.GetActiveID32.restype = ctypes.c_short
    # create a buffer of given size to pass it
    # to get the raw data.
    raw_data_tmp = (ctypes.c_ubyte * buffer_size.value)()
    #as per documentation 250 millisecond sleep is required
    # to get the raw data.
    time.sleep(250/1000.0)
    nbBits = pcproxlib.GetActiveID32(raw_data_tmp , buffer_size)
    bytes_to_read = (nbBits + 7) / 8 ;
    # will read at least 8 bytes
    if bytes_to_read < 8:
        bytes_to_read = 8

    for i in range(0 , bytes_to_read):
        temp_buf = "%02X " % raw_data_tmp[i]
        rawData = temp_buf + rawData
    return (nbBits , rawData)

def listAllConnectedRFIDevice():
    print ("\n")
    if usbConnect() == False:
        print ("Reader Not Connected ....\n")
        return None

    print ("%s\t\t\t%s\t\t\t\t\t%s\n" % ("PartNumber","Vid:Pid" ,"LUID"))
    nbOfDevices = getDevCnt()
    for i in range(0,nbOfDevices):
        if setActiveDev(i) == True:
            print ("%s\t\t\t%s\t\t\t%d" % (getPartNumber(),getVidPidVendorName(),
            getLUID()))
    usbDisconnect()
    print ("\n")

from flask import Flask, request, render_template
from flask import json

app = Flask(__name__)

@app.route('/api/getActiveID32')
def _getactivideid32():
    #return str(getActiveID32())
    _nbBits = None
    _data = None
    _timestamp = timestamp
    with lock:
        _nbBits = nbBits
        _data = data
        _timestamp = timestamp
    return {'bits': _nbBits, 'data': _data, 'time': _timestamp}
    
@app.route('/api/listAllConnectedRFIDevice')
def _listallconnectedrfidevice():
    return  str(listAllConnectedRFIDevice())

import threading
import time
import datetime
nbBits = None
data = None
timestamp = None
lock = threading.Lock()

def thread_fucntion():
    try:
        print('Start thread.')
        usbDisconnect()
        if usbConnect():
            global nbBits
            global data
            global timestamp
            while True:
                (_nbBits, _data) = getActiveID32()
                _timestamp = str(datetime.datetime.now())
                with lock:
                    nbBits = _nbBits
                    data = _data
                    timestamp = _timestamp
                time.sleep(.25)
    except:
        print('End thread.')
        time.sleep(.5)
        threading.Thread(target = thread_fucntion, args = ()).start() #run forever 


if __name__ == '__main__':
    threading.Thread(target = thread_fucntion, args = ()).start() #start thread
    app.run(host='0.0.0.0', port=8080)

