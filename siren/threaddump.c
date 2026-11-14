#include <windows.h>
#include <tlhelp32.h>
#include <dbghelp.h>
#include <stdio.h>
#pragma comment(lib, "dbghelp.lib")
static HANDLE hProc;
static void walk(DWORD tid) {
  HANDLE hT = OpenThread(THREAD_SUSPEND_RESUME | THREAD_GET_CONTEXT | THREAD_QUERY_INFORMATION, FALSE, tid);
  if (!hT) { printf("tid %lu: OpenThread failed %lu\n", (unsigned long)tid, GetLastError()); return; }
  if (SuspendThread(hT) == (DWORD)-1) { printf("tid %lu: suspend failed\n", (unsigned long)tid); CloseHandle(hT); return; }
  CONTEXT ctx; memset(&ctx, 0, sizeof(ctx)); ctx.ContextFlags = CONTEXT_FULL;
  if (!GetThreadContext(hT, &ctx)) { printf("tid %lu: GetThreadContext failed\n", (unsigned long)tid); ResumeThread(hT); CloseHandle(hT); return; }
  STACKFRAME64 sf; memset(&sf, 0, sizeof(sf));
  sf.AddrPC.Offset = ctx.Rip; sf.AddrPC.Mode = AddrModeFlat;
  sf.AddrFrame.Offset = ctx.Rbp; sf.AddrFrame.Mode = AddrModeFlat;
  sf.AddrStack.Offset = ctx.Rsp; sf.AddrStack.Mode = AddrModeFlat;
  printf("=== tid %lu ===\n", (unsigned long)tid);
  for (int i = 0; i < 40; i++) {
    if (!StackWalk64(IMAGE_FILE_MACHINE_AMD64, hProc, hT, &sf, &ctx, NULL, SymFunctionTableAccess64, SymGetModuleBase64, NULL)) break;
    if (sf.AddrPC.Offset == 0) break;
    char buf[sizeof(SYMBOL_INFO) + 256]; SYMBOL_INFO* sym = (SYMBOL_INFO*)buf;
    sym->SizeOfStruct = sizeof(SYMBOL_INFO); sym->MaxNameLen = 255;
    DWORD64 disp = 0;
    printf("  #%d %016llX ", i, (unsigned long long)sf.AddrPC.Offset);
    if (SymFromAddr(hProc, sf.AddrPC.Offset, &disp, sym)) printf("%s+0x%llX", sym->Name, (unsigned long long)disp);
    else printf("(no sym %lu)", GetLastError());
    printf("\n");
  }
  ResumeThread(hT); CloseHandle(hT);
}
int main(int argc, char** argv) {
  if (argc < 2) { printf("usage: threaddump <pid>\n"); return 1; }
  DWORD pid = (DWORD)strtoul(argv[1], NULL, 10);
  hProc = OpenProcess(PROCESS_VM_READ | PROCESS_QUERY_INFORMATION, FALSE, pid);
  if (!hProc) { printf("OpenProcess failed %lu\n", GetLastError()); return 1; }
  SymSetOptions(SYMOPT_UNDNAME | SYMOPT_DEFERRED_LOADS);
  char sympath[1024];
  snprintf(sympath, sizeof sympath, "D:\\consoles\\ps3\\siren\\build");
  if (!SymInitialize(hProc, sympath, TRUE)) { printf("SymInitialize failed %lu\n", GetLastError()); return 1; }
  HANDLE snap = CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, 0);
  THREADENTRY32 te; te.dwSize = sizeof(te);
  for (BOOL ok = Thread32First(snap, &te); ok; ok = Thread32Next(snap, &te))
    if (te.th32OwnerProcessID == pid) walk(te.th32ThreadID);
  CloseHandle(snap); SymCleanup(hProc); return 0;
}
