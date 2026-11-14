import json, re
imps = json.load(open('D:/consoles/ps3/BCJS30020/PS3_GAME/USRDIR/analysis/EBOOT.imports.json'))
items = imps if isinstance(imps, list) else imps.get('imports', imps)
want = set()
for e in items:
    try:
        want.add(int(str(e.get('nid')), 0))
    except Exception:
        pass
txt = open('D:/consoles/ps3/siren/build/ppu_hle_nids.cpp', encoding='utf-8', errors='replace').read()
have = set(int(x, 0) for x in re.findall(r'0x[0-9A-Fa-f]+', txt) if int(x, 0) > 0x1000)
missing = sorted(want - have)
print('want', len(want), 'havehits', len(have), 'missing', len(missing))
for m in missing:
    print(hex(m))
