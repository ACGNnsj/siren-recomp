import struct
d = open('D:/consoles/ps3/BCJS30020/PS3_GAME/USRDIR/EBOOT.elf', 'rb').read()
print('class', d[4], 'data', d[5], 'ver', d[6])
if d[4] == 2:
    print('64-bit: phoff', hex(struct.unpack('>Q', d[0x28:0x30])[0]), 'phn', struct.unpack('>H', d[0x38:0x3A])[0])
else:
    print('32-bit: phoff', hex(struct.unpack('>I', d[0x1C:0x20])[0]), 'phn', struct.unpack('>H', d[0x2C:0x2E])[0])
