
Synopsis :
----------

This is a python example to show how rfideas's SDK can be used with python.
This application can be used to list all rfidea's devices, can be used to know
the current version etc.

Prerequisites\Dependencies:
--------------

1. Python 2.x.x or 3.x.x
2. ctypes python module
3. pcProxAPI.dll  while running on windows
4. libhidapi-hidraw.so and libpcProxAPI.so while running on Linux platform

NOTE: 
    1. To know, how you can install python on your platform please read their official 
       document.
    2. ctypes is part of python standard distribution since 2.5.x and can be downloaded 
       separately for older version via python package manager.
    3. libhidapi-hidraw.so is packaged with SDK.

How To Run :
-----------

Running the example is very easy, to see what are the options available use help.

    python readercomm.py --help

All supported options are below :

--enumerate        list all the connected rfidea's readers 
--sdk-version      give the sdk version 
--help             print this help 
--getid            give raw data of card which being read


Frequently Asked Questions(FAQ) :
--------------------------------

1. Why do I get "python: command not found" error?

  Make sure you have python installed and available in PATH environment variable.

2. Why do I get "No Reader Connected.." even though reader is connected physically?

  a.) if you are facing this issue on Linux platform then it happen because you don't 
      have proper permissions to access the device/reader. Minimum permissions needed for this 
      to work are "rw-rw-rw-". You should add rfidea's devices into dev rules to fix is properly.

 b.)  Make sure your reader is USB. Only USB readers will get listed since we only search those.

3. What to do when I get "dependency <name of lib> does not exists, 
   RFI_DLL_HOME environment variable can used to set DLL home" error?

  In default setup you should not get this error, but you can use RFI_DLL_HOME environment
  variable to point to home of libs where they can be found.

4. Why do I get "No Id Found, Please put card on the reader and make sure it must be configured 
   with the card placed on it"even though a correct card is placed on the reader" error even though
   correct card placed on reader?

  It might happen because few older reader doesn't support GetActiveId32 API , Please use GetActiveId instead.
  See API documentation for more details.
