import struct
d = open('D:/consoles/ps3/BCJS30020/PS3_GAME/USRDIR/EBOOT.elf', 'rb').read()
phoff = struct.unpack('>Q', d[0x28:0x30])[0]
phn = struct.unpack('>H', d[0x38:0x3A])[0]
phes = struct.unpack('>H', d[0x36:0x38])[0]
print('phentsize', phes)
for i in range(phn):
    o = phoff + i * phes
    t, fl = struct.unpack('>II', d[o:o + 8])
    off, va, pa, fsz, msz, al = struct.unpack('>QQQQQQ', d[o + 8:o + 56])
    print(i, 'type', t, 'flags', fl, 'off', hex(off), 'vaddr', hex(va), 'filesz', hex(fsz), 'memsz', hex(msz))
