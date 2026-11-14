import re
lines = open('D:/consoles/ps3/BCJS30020/PS3_GAME/USRDIR/analysis/lifted/ppu_recomp_001.cpp', encoding='utf-8', errors='replace').read().splitlines()
start = 312376 - 1
calls = {}
n = 0
for i in range(start, min(start + 1500, len(lines))):
    l = lines[i]
    if i > start + 50 and re.match(r'void func_', l):
        n = i + 1 - start
        break
    for m in re.findall(r'func_([0-9A-Fa-f]+)\(ctx\)', l):
        calls[m] = calls.get(m, 0) + 1
print('func_00355060 lines:', n, 'calls:')
for k in sorted(calls):
    print(' ', k, calls[k])
