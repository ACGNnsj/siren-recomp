import json
p = 'D:/consoles/ps3/BCJS30020/PS3_GAME/USRDIR/analysis/prx.json'
d = json.load(open(p))
for m in d['modules']:
    name = m.get('name', m.get('module'))
    nids = m.get('nids') or []
    names = m.get('names') or []
    for i, nid in enumerate(nids):
        nm = names[i] if i < len(names) else ''
        if 'spawn' in str(nm).lower():
            print(name, hex(nid), nm)
print('done')
