CC = gcc
INCFLAG =    -I .  -I ../../include
LDFLAGS = -lpcProxAPI -lhidapi-hidraw

CXXFLAGS  = -L ../../lib/64

ifeq ($(arch),x86_32)
CXXFLAGS  = -L ../../lib/32
CFLAG = -m32
LDFLAGS+= -m32
endif

all: ./readercomm.cpp
	$(CC) $(CFLAG) $(INCFLAG)  -o  readercomm ./readercomm.cpp $(CXXFLAGS) $(LDFLAGS)
