import json
d = json.load(open('D:/consoles/ps3/BCJS30020/PS3_GAME/USRDIR/analysis/EBOOT.imports.json'))
items = d if isinstance(d, list) else d.get('imports', d)
for e in items:
    nid = e.get('nid')
    try:
        n = int(str(nid), 0)
    except Exception:
        continue
    if n == 0xA2C7BA64:
        print('STUB', hex(e.get('stub', 0)) if isinstance(e.get('stub'), int) else e.get('stub'), e)
