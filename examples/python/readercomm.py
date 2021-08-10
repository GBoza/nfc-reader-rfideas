"""
Author : IntimeTec Visionsoft Private Limited.
Creation Date : 15 Feb,2017
This sample application uses "ctypes" module which
comes by default along with python installation since
python 2.5.x.

This example merely a proof of concept that rfideas's
SDK(which is a C/C++ library) can be used in python.
Developers are free to use any other binding framework of
their choice.
"""
import ctypes
import sys
import platform
import os
from ctypes import *
import time

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

def showHelpText(program_name):

    print ("\nusage: %s [options] \n\n\
--enumerate\t\t list all the connected rfidea's readers \n\
--sdk-version\t\t give the sdk version \n\
--help\t\t         print this help \n\
--getid\t\t         give raw data of card which being read\n" \
            % program_name)


def main():
    global pcproxlib

    # to know whether process is 64 bit or 32
    # if void pointer size is 8 then 64 bit process
    # if 32 bit process then void pointer size is
    # 4
    void_p_size =  ctypes.sizeof(ctypes.c_voidp)
    if void_p_size == 8:
        lib_home = "../../lib/64"
    else:
        lib_home = "../../lib/32"

    # two arguments can't be supplied in single run.
    if len(sys.argv) != 2:
        showHelpText(sys.argv[0]);
        return None

    # if RFI_DLL_HOME defined then it takes priority
    if os.getenv('RFI_DLL_HOME') != None:
        lib_home = os.getenv('RFI_DLL_HOME')

    # if Unix flavor
    if platform.system() == "Linux" or platform.system() == "Darwin":
        lib_name = "libpcProxAPI.so"
        # load hid raw too since we use that as helper
        # library to communicate with devices.
        hid_lib_path = lib_home + "/libhidapi-hidraw.so"
        if os.path.exists(hid_lib_path):
            pcproxlib = ctypes.CDLL(hid_lib_path,  mode = ctypes.RTLD_GLOBAL)
        else:
            print ("\ndependency %s does not exists, RFI_DLL_HOME \
environment variable can used to set DLL home\n" % hid_lib_path)
            return None
    else:
        lib_name = "pcProxAPI.dll"

    pcprox_lib_name = lib_home + "/" + lib_name

    if os.path.exists(pcprox_lib_name):
        if platform.system() == "Linux" or platform.system() == "Darwin":
            pcproxlib = ctypes.CDLL(pcprox_lib_name)
        else:
            pcproxlib = ctypes.WinDLL(pcprox_lib_name)
    else:
        print ("\ndependency %s does not exists, RFI_DLL_HOME \
environment variable can used to set DLL home\n" % pcprox_lib_name)
        return None

    # Speed up device search restrict it to
    # only usb devices.
    setDevTypeSrch(0)

    if sys.argv[1] == "--help":
        showHelpText(sys.argv[0])

    elif sys.argv[1] == "--enumerate":
        listAllConnectedRFIDevice()

    elif sys.argv[1] == "--sdk-version":
        sdk_version = getLibVersion();
        print ("\nsdk version : %s" % sdk_version)

    elif sys.argv[1] == "--getid":
        if usbConnect():
            (nbBits , data) = getActiveID32()
            if nbBits == 0:
                print ("\nNo Id Found, Please put card on the reader and \
make sure it must be configured with the card placed on it")
            else:
                print ("\n%d Bits : %s" % (nbBits , data))
            usbDisconnect()
    else:
        print ("\nInvalid argument..\n")
        showHelpText(sys.argv[0])


if __name__ == '__main__':
    main()
