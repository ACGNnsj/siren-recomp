p = 'D:/consoles/ps3/ps3recomp/libs/system/sysPrxForUser.c'
t = open(p, encoding='utf-8').read()
old = 's32 sys_prx_exitspawn_with_level(void)\n{\n    printf(\"[sysPrxForUser] sys_prx_exitspawn_with_level() - no-op\\n\");\n    return CELL_OK;\n}'
assert t.count(old) == 1, t.count(old)
new = '''s32 sys_prx_exitspawn_with_level(void)
{
    /* Titles reboot themselves here (fresh boot, often with a bigger memory
     * container): on HW this call never returns to the old instance, which
     * goes on to sys_process_exit while the new instance boots. Emulate by
     * re-executing our own command line, capped so a title that keeps asking
     * (a container we cannot grow) degrades to the old no-op. Siren: Blood
     * Curse needs this: its EBOOT exits 0 right after this call. */
#ifdef _WIN32
    {
        char cntbuf[16] = { 0 };
        DWORD cnt = 0;
        if (GetEnvironmentVariableA("PS3_RESPAWN_COUNT", cntbuf,
                                    (DWORD)sizeof(cntbuf)) > 0)
            cnt = (DWORD)strtoul(cntbuf, NULL, 10);
        if (cnt < 3) {
            char self[MAX_PATH], cmd[8192];
            STARTUPINFOA si; PROCESS_INFORMATION pi;
            snprintf(cntbuf, sizeof(cntbuf), "%lu", (unsigned long)(cnt + 1));
            SetEnvironmentVariableA("PS3_RESPAWN_COUNT", cntbuf);
            fflush(stdout); fflush(stderr);
            GetModuleFileNameA(NULL, self, (DWORD)sizeof(self));
            snprintf(cmd, sizeof(cmd), "\\"%s\\" %s", self, GetCommandLineA());
            /* GetCommandLineA starts with the exe path; skip it. */
            {
                const char* args = GetCommandLineA();
                if (*args == \'"\') {
                    args++;
                    while (*args && *args != \'"\') args++;
                    if (*args) args++;
                } else {
                    while (*args && *args != \' \' && *args != \'\\t\') args++;
                }
                while (*args == \' \' || *args == \'\\t\') args++;
                snprintf(cmd, sizeof(cmd), "\\"%s\\" %s", self, args);
            }
            ZeroMemory(&si, sizeof(si)); si.cb = sizeof(si);
            ZeroMemory(&pi, sizeof(pi));
            if (CreateProcessA(NULL, cmd, NULL, NULL, TRUE, 0, NULL, NULL,
                               &si, &pi)) {
                printf("[sysPrxForUser] exitspawn: re-executed (gen %lu)\\n",
                       (unsigned long)(cnt + 1));
                CloseHandle(pi.hProcess); CloseHandle(pi.hThread);
                _exit(42); /* old instance is gone; child boots fresh */
            }
            printf("[sysPrxForUser] exitspawn: re-exec failed (%lu) - no-op\\n",
                   GetLastError());
        } else {
            printf("[sysPrxForUser] exitspawn: gen cap reached - no-op\\n");
        }
    }
#else
    printf("[sysPrxForUser] sys_prx_exitspawn_with_level() - no-op\\n");
#endif
    return CELL_OK;
}'''
open(p, 'w', encoding='utf-8', newline='').write(t.replace(old, new))
print('patched')
