
#include <stdlib.h>
#include <string.h>
#include "pcProxAPI.h"
#include <stdio.h>

#define PRXDEVTYP_USB 0

void showHelpText()
{
	printf("\nUsage: readercomm [options]\n\n");
	printf("--enumerate\t\t list all the connected rfidea's readers\n");
	printf("--sdk-version\t\t give the sdk version\n");
	printf("--help\t\t         print this help\n");
	printf("--getid\t\t         give raw data of card which being read\n");
}

void listAllConnectedRFIDevice()
{
	short i, getDevCnt;
	SetDevTypeSrch(PRXDEVTYP_USB);
	if (usbConnect() == 0)
	{
		printf("\nReader not connected\n");
		return;
	}
	getDevCnt = GetDevCnt();
	printf("\nPartNumber\t\tVid:Pid\t\t\t\tLUID\n\n");
	for (i = 0; i < getDevCnt; i++)
	{
		SetActDev(i);
		unsigned short luid = GetLUID();
		printf("%s\t\t%s\t\t%d", getPartNumberString(), GetVidPidVendorName(), luid);
		printf("\n");
	}
	USBDisconnect();
}

void printLibVersion()
{
	short m, n, d;
	GetLibVersion(&m, &n, &d);
	printf("\nSDK Version : %02d.%02d.%d\n", m, n, d);
}

void printActiveId()
{
	SetDevTypeSrch(PRXDEVTYP_USB);
	if (usbConnect() == 0)
	{
		printf("\nReader not connected\n");
		return;
	}
#ifdef _WIN32
	Sleep(250);
	BYTE buf[32];
#else
	usleep(250000);
	unsigned char buf[32];
#endif
	memset(buf, 0, sizeof(buf));
	short bits = GetActiveID32(buf, 32);
	int num;
	if (bits == 0)
	{
		printf("\nNo id found, Please put card on the reader and ");
		printf("make sure it must be configured with the card placed on it.\n");
	}
	else
	{
		int bytes_to_read = (bits + 7) / 8;
		if (bytes_to_read < 8){
			bytes_to_read = 8;
		}
		printf("\n%d Bits : ", bits);
		for (int i = bytes_to_read - 1; i >= 0; i--)
		{
			num = buf[i];
			printf("%02X ", buf[i]);
		}
		printf("\n");
	}
	USBDisconnect();
}

int main(int argc, char* argv[])
{
	if (argc == 1)
	{
		showHelpText();
	}

	else if (strcmp(argv[1], "--enumerate") == 0)
	{
		listAllConnectedRFIDevice();
	}

	else if (strcmp(argv[1], "--sdk-version") == 0)
	{
		printLibVersion();
	}

	else if (strcmp(argv[1], "--getid") == 0)
	{
		printActiveId();
	}

	else if (strcmp(argv[1], "--help") == 0)
	{
		showHelpText();
	}

	else
	{
		printf("\nWrong argument passed\n");
		showHelpText();
	}
	return 0;
}
