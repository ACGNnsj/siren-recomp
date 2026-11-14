import struct
f = open('D:/consoles/ps3/BCJS30020/PS3_GAME/USRDIR/EBOOT.elf', 'rb')
d = f.read(64)
phoff = struct.unpack('>Q', d[0x28:0x30])[0]
phentsz = struct.unpack('>H', d[0x36:0x38])[0]
phnum = struct.unpack('>H', d[0x38:0x3a])[0]
print('n', phnum, 'entsz', phentsz)
for i in range(phnum):
    f.seek(phoff + i * phentsz)
    p = f.read(phentsz)
    typ, flags, off, vaddr, paddr, filesz, memsz, align = struct.unpack('>IIQQQQQQ', p)
    hit = vaddr <= 0x79D1C8 < vaddr + memsz
    print(i, 'type', typ, 'vaddr', hex(vaddr), 'memsz', hex(memsz), 'HIT' if hit else '')
    if hit:
        f.seek(off + (0x79D1C8 - vaddr))
        print('   code=', hex(struct.unpack('>I', f.read(4))[0]), 'toc=', hex(struct.unpack('>I', f.read(4))[0]))
