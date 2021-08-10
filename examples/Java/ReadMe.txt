
Synopsis :
----------

This is a java example to show how rfideas's SDK can be used with java.
This application can be used to list all rfidea's devices, can be used to know
the current version etc.

Prerequisites :
--------------

1. jdk-7 or above
2. jna.jar
3. pcProxAPI.dll  while running on windows
4. libhidapi-hidraw.so and libpcProxAPI.so while running on Linux platform

NOTE: 
    1.To know, how you can install java on your platform please read their official 
      document.
    2.download "jna.jar" and reference jna.jar in your project's CLASSPATH.
	  Command to set the classpath:
	  For window user:
	  set classpath=<jna.jar path>\jna-<version>.jar;.\
	  For linux user:
	  export CLASSPATH=<jna.jar path>/jna.jar:./
    3. Minimum version of JNA required is 3.2.7.

How to compile :
---------------

Use this command to compile :
	javac readercomm.java
	
How To Run :
-----------

Running the example is very easy, to see what are the options available use help.

    java readercomm --help

All supported options are below :

--enumerate        list all the connected rfidea's readers 
--sdk-version      give the sdk version 
--help             print this help 
--getid            give raw data of card which being read

Frequently Asked Questions(FAQ) :
--------------------------------

1. Why do I get "javac: not recognized as internal or external command" error?

	Make sure you have java installed and available in PATH environment variable.

2. Why do I get "java: not recognized as internal or external command" error?

	Make sure you have java installed and available in PATH environment variable.
	
3. Why do my code does not compile?

	Most probably you are facing this issue on Linux platform, give proper permission to 
	readercomm.java before compiling it.

4. Why do I get "No Reader Connected.." even though reader is connected physically?

	It happens because you might have connected a reader other than USB as this sample 
	supports USB readers only. 
	Or probably you are facing this issue on Linux platform, it happen because you don't 
	have proper permissions to access the device/reader. Minimum permissions needed for this 
	to work are "rw-rw-rw-". You should add rfidea's devices into dev rules to fix is properly.
  
5. Why do I get "No Id Found, Please put card on the reader and make sure it must be configured 
   with the card placed on it" even though a correct card is placed on the reader?

	It might happen because few older reader doesn't support GetActiveId32 API , please use GetActiveId instead.
	See API documentation for more details.

6. What to do when I get "dependency <name of lib> does not exists, 
   RFI_DLL_HOME environment variable can used to set DLL home" error?

	In default setup you should not get this error, but you can use RFI_DLL_HOME environment
	variable to point to home of lib where they can be found.

7. Why do I get an error "Exception in thread "main" java.lang.UnsatisfiedLinkError:
   Unable to load library '../../lib/64/pcProxAPI.dll': The specified module could not be found."?
	
	you will get this error if you are using 64 bit dll with 32 bit JVM or vice versa. you may also get this 
	error if you using a JNA jar older then 3.2.7 even though you are running with correct JVM.
