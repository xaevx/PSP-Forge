TARGET = pspforge_smoketest
OBJS = main.o

CXXFLAGS = -O2 -G0 -Wall -Wextra -std=c++11
CFLAGS = -O2 -G0 -Wall -Wextra
LIBS = -lpspdebug -lpspdisplay -lpspctrl

EXTRA_TARGETS = EBOOT.PBP
PSP_EBOOT_TITLE = PSP Forge Smoke Test

# Standard PSPSDK build helper. Confirm PSPSDK is set by your PSPDEV install.
include $(PSPSDK)/lib/build.mak
