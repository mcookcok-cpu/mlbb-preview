import os, json
H = os.path.expanduser('~')
V = H + '/downloads/selena_decoded'

# (akhiran mesh, tekstur diffuse tanpa .png, alpha?, tampil awal?)
SETS = [
  {'id': 'selena-hd', 'name': 'Selena · Aspirant (HD)', 'sub': 'Model resolusi tinggi skin Aspirant',
   'dir': 'Art__android__h/hero_selena_skin01_high_add',
   'parts': [
     ('body01', 'selena_skin11_high_body01_d', False, True),
     ('body02', 'selena_skin11_high_body02_d', False, True),
     ('face01', 'selena_skin11_high_head01_d', False, True),
     ('face02', 'selena_skin11_high_head02_d', True, True),
     ('hair01', 'selena_skin11_high_hair01_d', True, True),
     ('hair02', 'selena_skin11_high_hair02_d', True, True),
     ('hair03', 'selena_skin11_high_hair02_d', True, False),
     ('hair04', 'selena_skin11_high_hair01_d', True, False),
     ('weapon01', 'selena_skin11_high_weapon01_d', False, False),
     ('weapon02', 'selena_skin11_high_weapon02_d', False, True),
     ('npc01', 'selena_skin11_high_npc_d', False, False),
     ('fx01', 'selena_skin11_high_fx01_d', True, False),
     ('SP_mesh_01', None, False, False),
     ('SP_mesh_02', None, False, False),
   ]},
  {'id': 'selena-game', 'name': 'Selena · Aspirant (in-game)', 'sub': 'Model ringan yang dipakai saat bertanding',
   'dir': 'Art__android__h/hero_selena_skin01_add',
   'parts': [
     ('hero_selena_skin11', 'selena_skin11_pbs_d', False, True),
     ('Object002', 'liuguang_1', True, False),
     ('Object003', 'liuguang_2', True, False),
   ]},
  {'id': 'evilgirl-game', 'name': 'Evilgirl · Aspirant (in-game)', 'sub': 'Wujud kedua, model in-game',
   'dir': 'Art__android__h/hero_evilgirl_skin01_add',
   'parts': [
     ('hero_evilgirl_skin11', 'evilgirl_skin11_pbs_d', False, True),
     ('Plane026', 'Glow_SD_LY_001_cnnew', True, False),
     ('Plane027', 'Glow_SD_LY_001_cnnew', True, False),
     ('Plane029', 'Glow_SD_LY_001_cnnew', True, False),
   ]},
]

out = {'sets': []}
for s in SETS:
    base = V + '/' + s['dir']
    meshes = sorted(os.listdir(base + '/meshes'))
    parts = []
    for key, tex, alpha, on in s['parts']:
        m = [f for f in meshes if f.endswith(key + '.obj')]
        if not m:
            print('mesh tidak ketemu:', s['id'], key); continue
        t = None
        if tex:
            tp = base + '/textures/' + tex + '.png'
            if os.path.exists(tp): t = 'v/' + s['dir'] + '/textures/' + tex + '.png'
            else: print('tekstur tidak ketemu:', tex)
        parts.append({'n': key, 'm': 'v/' + s['dir'] + '/meshes/' + m[0], 't': t, 'a': alpha, 'on': on,
                      's': os.path.getsize(base + '/meshes/' + m[0])})
    out['sets'].append({'glb': ('g/selena_hd.glb' if s['id']=='selena-hd' else None), 'id': s['id'], 'name': s['name'], 'sub': s['sub'], 'bundle': os.path.basename(s['dir']), 'parts': parts})
json.dump(out, open(H + '/mlbb-preview/hero.json', 'w'), ensure_ascii=False)
print([(x['id'], len(x['parts'])) for x in out['sets']])
