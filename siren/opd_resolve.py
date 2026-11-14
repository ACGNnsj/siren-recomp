import struct, sys
p = 'D:/consoles/ps3/BCJS30020/PS3_GAME/USRDIR/EBOOT.elf'
d = open(p, 'rb').read()
assert d[0:4].hex() == '7f454c46', 'not elf'
phoff = struct.unpack('>Q', d[0x28:0x30])[0]
phn = struct.unpack('>H', d[0x38:0x3A])[0]
print('phoff', hex(phoff), 'phn', phn)
ea = int(sys.argv[1], 16) if len(sys.argv) > 1 else 0x7ACC10
for i in range(phn):
    o = phoff + i * 56
    t = struct.unpack('>IIQQQQQQ', d[o:o + 56])
    if t[0] == 1:
        v, fo, fsz = t[3], t[2], t[5]
        if v <= ea < v + fsz:
            ffo = fo + (ea - v)
            print('LOAD', i, 'vaddr', hex(v), 'fo', hex(ffo))
            code = struct.unpack('>Q', d[ffo:ffo + 8])[0]
            toc = struct.unpack('>Q', d[ffo + 8:ffo + 16])[0]
            print('code', hex(code), 'toc', hex(toc))
