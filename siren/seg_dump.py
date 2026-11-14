import struct
d = open('D:/consoles/ps3/BCJS30020/PS3_GAME/USRDIR/EBOOT.elf', 'rb').read()
phoff = struct.unpack('>Q', d[0x28:0x30])[0]
phn = struct.unpack('>H', d[0x38:0x3A])[0]
for i in range(phn):
    o = phoff + i * 56
    t = struct.unpack('>IIQQQQQQ', d[o:o + 56])
    print(i, 'type', t[0], 'flags', t[1], 'off', hex(t[2]), 'vaddr', hex(t[3]), 'filesz', hex(t[5]), 'memsz', hex(t[6]))
