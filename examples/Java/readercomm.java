/*
Author : IntimeTec Visionsoft Private Limited.
Creation Date : 16 Feb,2017
This sample application uses "jna" which does not 
comes by default along with jdk. You have to download 
"jna.jar" and reference jna.jar in your project's CLASSPATH.

This example merely a proof of concept that rfideas's
SDK(which is a C/C++ library) can be used in Java.
Developers are free to use any other binding framework of
their choice.
*/

import com.sun.jna.Library;
import com.sun.jna.Native;

public class readercomm{

	public interface Reader extends Library {
		/*
		Helper of  usbconnect, Will restrict
		the device search to a particular category
		for example.
		Device Type could be one of following
		0 : To search only USB devices
		1 :  To Search Serial RS-232 only.
		-1 : Both USB and serial devices.
		This function will return true in case of
		success false otherwise.
		*/
		public short SetDevTypeSrch(short iSrchType);
		
		/*
		return true in case success, false otherwise.
		Will open connection to all rfidea's readers/devices
		in onces.
		Individual device can be accessed by using setActiveDev first
		then call other functions.
		*/
		public int usbConnect();
		
		/*
		Will return true in case success, false otherwise.
		As per API documentation USBDisconnect always returns
		true.
		It will close the handle to all rfidea's devices, should be
		called during clean up.
		*/
		public int USBDisconnect();
		
		//Will return the LUID of active device/Reader.
		public int GetLUID();
		
		//Will Return the total number of connected rfidea's readers.
		public short GetDevCnt();
		
		//Will return true if able to set active device to given device, false otherwise
		public short SetActDev(short iNdx);
		
		//Will return the part number of active device and none in case of failure.
		public String getPartNumberString();
		
		/*
		Will return None in case of error other wise will return
		the VID PID and product name in following format
		<VID>:<PID> <product name>
		*/
		public String GetVidPidVendorName();

		/*
		Will return a tuple consisting number of bits read and actual data.
		Minimum 8 byte of data will be returned.
		*/
		public short GetActiveID32(byte[] pBuf, short wBufMaxSz);
		
		/*
		Will return the SDK version in following format
		<Major>.<Minor>.<Dev>.
		In case of error will return None
		*/
		public short GetLibVersion(int[] piVerMaj,int[] piVerMin,int[] piVerDev);
    }
	
	public static void listAllConnectedRFIDevice(Reader lib){
		short PRXDEVTYP_USB = 0;
		lib.SetDevTypeSrch(PRXDEVTYP_USB);
		if(lib.usbConnect() == 0){
			System.out.println("\nReader not connected");
			return;
		}
		short getDevCnt = lib.GetDevCnt();
		System.out.println("\nPartNumber" + "\t\t" + "Vid:Pid" + "\t\t\t\t" + "LUID\n");
		for(short i=0; i < getDevCnt; i++){
			lib.SetActDev(i);
			System.out.println(lib.getPartNumberString() + "\t\t" + lib.GetVidPidVendorName() + "\t\t" + lib.GetLUID());
		}
		lib.USBDisconnect();
	}
	
	public static String getLibVersion(Reader lib){
		int major[] = new int [1];
		int minor[] = new int [1];
		int build[] = new int [1];
		lib.GetLibVersion(major,minor,build);
		String libVersion = major[0] + "." + minor[0] + "." + build[0];
		return libVersion;
	}
	
	public static void getActiveId32(Reader lib){
		short PRXDEVTYP_USB = 0;
		lib.SetDevTypeSrch(PRXDEVTYP_USB);
		if(lib.usbConnect() == 0){
			System.out.println("\nReader not connected");
			return;
		}
		
		try {
			Thread.sleep(250);
		} 
		catch(InterruptedException ex) {
			Thread.currentThread().interrupt();
		}
		
		short wBufMaxSz = 32;
		byte buf[] = new byte [wBufMaxSz];
		short bits = lib.GetActiveID32(buf, wBufMaxSz);
		
		if(bits == 0){
			String errorMessage = "\nNo id found, Please put card on the reader and " +
								"make sure it must be configured with the card placed on it.";
			System.out.println(errorMessage);
		}
		else{
			int bytes_to_read = (bits + 7) / 8 ;
			if(bytes_to_read < 8){
				bytes_to_read = 8;
			}
			System.out.print("\n" + bits + " Bits : ");
			for (int i = bytes_to_read-1; i >= 0; i--)
			{
				System.out.printf("%02X ",buf[i]);
			}
			System.out.println();
		}
		lib.USBDisconnect();
	}
	
	public static void showHelpText(){
	System.out.println("\nUsage: readercomm [options]\n");
	System.out.println("--enumerate\t\t list all the connected rfidea's readers");
	System.out.println("--sdk-version\t\t give the sdk version");
	System.out.println("--help\t\t         print this help");
	System.out.println("--getid\t\t         give raw data of card which being read");
	}
	
	public static void main(String args[]){
		Reader lib;
		String lib_home = "";
		String lib_name = "";
		
		if(System.getProperty("os.arch").equals("amd64")){
			//checking whether it is 64 bit process
			lib_home = "../../lib/64";
		}
		else{
			//it is 32 bit process
			lib_home = "../../lib/32";
		}

		if(System.getenv("RFI_DLL_HOME") != null){
			lib_home = System.getenv("RFI_DLL_HOME");
		}
		
		if(System.getProperty("os.name").startsWith("Windows")){
			//checking whether the OS is Windows
			lib_name = "pcProxAPI.dll";
			
		}
		else{
			//OS is Linux
			lib = (Reader) Native.loadLibrary(lib_home + "/libhidapi-hidraw.so", Reader.class);
			lib_name = "libpcProxAPI.so";
		}
		
		lib = (Reader) Native.loadLibrary(lib_home + "/" + lib_name, Reader.class);
		
		if(args.length == 0){
			showHelpText();
		}
		
		else if(args[0].equals("--enumerate")){
			listAllConnectedRFIDevice(lib);
		}
		
		else if(args[0].equals("--sdk-version")){
			String sdk_version = getLibVersion(lib);
			System.out.println("\nSDK Version : " + sdk_version);
		}
		
		else if(args[0].equals("--getid")){
			getActiveId32(lib);
		}
		
		else if(args[0].equals("--help")){
			showHelpText();
		}
		
		else{
			System.out.println("\nWrong argument passed");
			showHelpText();
		}
	}
}