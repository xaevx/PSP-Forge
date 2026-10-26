#include <pspkernel.h>
#include <pspdebug.h>
#include <pspdisplay.h>
#include <pspctrl.h>

PSP_MODULE_INFO("PSPForgeSmokeTest", 0, 0, 1);
PSP_MAIN_THREAD_ATTR(THREAD_ATTR_USER);

int main(int, char**) {
    pspDebugScreenInit();
    pspDebugScreenPrintf("PSP Forge - native homebrew smoke test\n\n");
    pspDebugScreenPrintf("If you can read this, the PSP toolchain build works.\n");
    pspDebugScreenPrintf("This is not a game converter yet.\n\n");
    pspDebugScreenPrintf("Press START to exit.\n");

    SceCtrlData pad{};
    sceCtrlSetSamplingCycle(0);
    sceCtrlSetSamplingMode(PSP_CTRL_MODE_ANALOG);

    while (true) {
        sceCtrlReadBufferPositive(&pad, 1);
        if (pad.Buttons & PSP_CTRL_START) break;
        sceDisplayWaitVblankStart();
    }
    sceKernelExitGame();
    return 0;
}
