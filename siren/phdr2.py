import struct, sys
d = open('D:/consoles/ps3/BCJS30020/PS3_GAME/USRDIR/EBOOT.elf', 'rb').read()
phoff = struct.unpack('>Q', d[0x20:0x28])[0]
phn = struct.unpack('>H', d[0x38:0x3A])[0]
phes = struct.unpack('>H', d[0x36:0x38])[0]
print('phoff', hex(phoff), 'phn', phn, 'phes', phes)
for i in range(phn):
    o = phoff + i * phes
    t, fl = struct.unpack('>II', d[o:o + 8])
    off, va, pa, fsz, msz, al = struct.unpack('>QQQQQQ', d[o + 8:o + 56])
    print(i, 'type', t, 'flags', hex(fl), 'off', hex(off), 'vaddr', hex(va), 'filesz', hex(fsz), 'memsz', hex(msz))
if len(sys.argv) > 1:
    ea = int(sys.argv[1], 16)
    for i in range(phn):
        o = phoff + i * phes
        t, fl = struct.unpack('>II', d[o:o + 8])
        off, va, pa, fsz, msz, al = struct.unpack('>QQQQQQ', d[o + 8:o + 56])
        if t == 1 and va <= ea < va + fsz:
            ffo = off + (ea - va)
            code = struct.unpack('>Q', d[ffo:ffo + 8])[0]
            toc = struct.unpack('>Q', d[ffo + 8:ffo + 16])[0]
            print('EA', hex(ea), '-> fo', hex(ffo), 'code', hex(code), 'toc', hex(toc))
