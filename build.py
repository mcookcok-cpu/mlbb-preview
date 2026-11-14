import os, json, hashlib
from PIL import Image
H=os.path.expanduser('~'); V=H+'/downloads/selena_decoded'; A=H+'/downloads/selena_decoded_audio'; T=H+'/mlbb-preview/thumbs'
tex=[];mesh=[];anim=[];aud=[]
for dp,_,fs in os.walk(V):
    for f in sorted(fs):
        rel=os.path.relpath(os.path.join(dp,f),V); parts=rel.split('/')
        bundle=parts[1] if len(parts)>2 else ''
        if '/textures/' in '/'+rel and f.endswith('.png'):
            h=hashlib.md5(rel.encode()).hexdigest()[:12]; th=T+'/'+h+'.jpg'
            try:
                im=Image.open(os.path.join(dp,f)); w,hh=im.size
                if not os.path.exists(th):
                    t=im.convert('RGBA'); bg=Image.new('RGB',t.size,(40,40,40)); bg.paste(t,mask=t.split()[3]); bg.thumbnail((220,220)); bg.save(th,quality=80)
                tex.append({'n':f[:-4],'b':bundle,'p':'v/'+rel,'t':'t/'+h+'.jpg','w':w,'h':hh})
            except Exception as e: pass
        elif '/meshes/' in '/'+rel and f.endswith('.obj'):
            mesh.append({'n':f[:-4],'b':bundle,'p':'v/'+rel,'s':os.path.getsize(os.path.join(dp,f))})
        elif '/animationclip/' in '/'+rel:
            anim.append({'n':f[:-5],'b':bundle,'p':'v/'+rel})
for dp,_,fs in os.walk(A):
    for f in sorted(fs):
        if f.endswith('.wav'):
            rel=os.path.relpath(os.path.join(dp,f),A); aud.append({'n':f[:-4],'b':rel.split('/')[0],'p':'a/'+rel,'s':os.path.getsize(os.path.join(dp,f))})
json.dump({'tex':tex,'mesh':sorted(mesh,key=lambda x:x['s']),'anim':anim,'aud':aud},open(H+'/mlbb-preview/index.json','w'))
print(len(tex),'tekstur',len(mesh),'mesh',len(anim),'anim',len(aud),'audio')
