
Synopsis :
----------

This example shows how rfidea's SDK can be used with C/C++, This is a simple 
command line application which can be used to list all rfidea's USB readers, get
raw data of card which is being read etc.


Prerequisites : 
---------------

1. VC++ tools on Windows
2. pcProxAPI.dll  while running on windows
3. libhidapi-hidraw.so and libpcProxAPI.so while running on Linux platform
4. GNU make and g++ on Linux Platform

NOTE:
  
  1. You can download and install Visual studio which will include all the dependencies.
     Follow their official document to know how to do that.
  2. This project is created using Visual Studio 2013.
  3. libhidapi-hidraw.so is packaged with SDK.


How to Build and Run in Windows:
--------------------------------

1. Build solution by using following command.

   "C:\Program Files (x86)\MSBuild\12.0\Bin\msbuild" readercomm.sln /p:Configuration=Release /t:Rebuild /p:Platform=<platform>

NOTE: 
	1. Select <platform> as "x64" for 64 bit and "Win32" for 32 bit compilation.
	2. Location of msbuild program may depend where you have installed it.
 
2. Switch to <platform>\Release directory by using following command.
   
   cd <platform>\Release

3. Run following command to see what are the options available 

   readercomm.exe --help

 All supported arguments :
 -------------------------

 Usages: readercomm [Options]

 --enumerate     list all the connected rfidea's readers
 --sdk-version   give the SDK version
 --help          print this help
 --getid         give raw data of card which being read

NOTE:
	1. You need to set the path of pcProxAPI.dll before running the application.
	  Command to set the path:
	  set path=%path%;<pcProxAPI.dll path>

	  
How to Build and Run in Linux:
------------------------------

1. Build solution by using following command.
	make

2. Run following command to see what are the options available 

   ./readercomm --help

 All supported arguments :
 -------------------------

 Usages: readercomm [Options]

 --enumerate     list all the connected rfidea's readers
 --sdk-version   give the SDK version
 --help          print this help
 --getid         give raw data of card which being read

NOTE:
	1. You need to set the path of libpcProxAPI.so and libhidapi-hidraw.so before running the application.
	  Command to set the path:
	  export LD_LIBRARY_PATH=<libpcProxAPI.so>:<libhidapi-hidraw.so>
	  
	  
Frequently Asked Questions (FAQ) :
----------------------------------

1. Why do I get "No Reader Connected.." even though reader is connected physically?

	It happens because you might have connected a reader other than USB as this sample 
	supports USB readers only. 
	Or probably you are facing this issue on Linux platform, it happen because you don't 
	have proper permissions to access the device/reader. Minimum permissions needed for this 
	to work are "rw-rw-rw-". You should add rfidea's devices into dev rules to fix is properly.
  
2. Why do I get "No Id Found, Please put card on the reader and make sure it must be configured 
   with the card placed on it" even though a correct card is placed on the reader?

	It might happen because few older reader doesn't support GetActiveId32 API , please use GetActiveId instead.
	See API documentation for more details.
	
3. Why do my code does not compile?

	Most probably you are facing this issue on Linux platform, give proper permission to 
	readercomm.cpp before compiling it.