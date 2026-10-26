TARGET = pspforge_smoketest
OBJS = main.o

CXXFLAGS = -O2 -G0 -Wall -Wextra -std=c++11
CFLAGS = -O2 -G0 -Wall -Wextra
LIBS = -lpspdebug -lpspdisplay -lpspctrl

EXTRA_TARGETS = EBOOT.PBP
PSP_EBOOT_TITLE = PSP Forge Smoke Test

# Ask the installed PSPDEV toolchain for the PSPSDK location.
PSPSDK = $(shell psp-config --pspsdk-path)
include $(PSPSDK)/lib/build.mak
