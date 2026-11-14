import json
d = json.load(open('D:/consoles/ps3/BCJS30020/PS3_GAME/USRDIR/analysis/EBOOT.imports.json'))
items = d if isinstance(d, list) else d.get('imports', d)
for e in items:
    try:
        if int(str(e.get('stub')), 0) in (0x614288, 0x616500):
            print(e)
    except Exception:
        pass
