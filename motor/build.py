"""Monta el vídeo largo: limpia audios, calcula tiempos, renderiza cada sección, une todo y genera los capítulos.
Uso: python build.py CARPETA_AUDIOS SALIDA.mp4"""
import subprocess, sys, json, os, importlib.util
AUD, OUT = sys.argv[1], sys.argv[2]
os.chdir('/tmp/claude-0/prod/exam')
SECS=[('INTRO','p_rest','Intro'),('P1','p1','Pregunta 1 · Redox, pila y solubilidad'),('P2B','p_rest','Pregunta 2B · Estructura atómica'),
      ('P4A','p_rest','Pregunta 4A · Termodinámica y síntesis de metanol'),('P4B','p_rest','Pregunta 4B · Ácido-base y neutralización'),('CIERRE','p_rest','Cierre')]
def beats(mod,cls):
    spec=importlib.util.spec_from_file_location(mod,f'{mod}.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return [b[0] for b in getattr(m,cls).BEATS]
parts=[]; chapters=[]; t=0.0
for sec,mod,title in SECS:
    src=next((os.path.join(AUD,f) for f in os.listdir(AUD) if os.path.splitext(f)[0].upper()==sec),None)
    if not src: print('FALTA',sec); continue
    subprocess.run(['python3','clean.py',src,f'clean/{sec}.wav'],check=True)
    ids=beats(mod,sec)
    r=subprocess.run(['python3','assemble.py',f'clean/{sec}.wav',sec,str(len(ids)),','.join(ids)],capture_output=True,text=True); print(r.stdout.strip())
    if 'OK timings' not in r.stdout: print('!! revisar pausas de',sec)
    subprocess.run(['/tmp/claude-0/venv/bin/manim','-qh','--fps','30',f'{mod}.py',sec],check=True,capture_output=True)
    v=f'media/videos/{mod}/1080p30/{sec}.mp4'; o=f'clean/{sec}_av.mp4'
    subprocess.run(['ffmpeg','-v','error','-y','-i',v,'-i',f'clean/{sec}.wav','-c:v','libx264','-crf','20','-preset','medium','-c:a','aac','-b:a','160k','-ar','48000','-shortest',o],check=True)
    d=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',o],capture_output=True,text=True).stdout)
    chapters.append((t,title)); t+=d; parts.append(o)
open('clean/list.txt','w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in parts))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','clean/list.txt','-c','copy','-movflags','+faststart',OUT],check=True)
with open(OUT.rsplit('.',1)[0]+'-capitulos.txt','w') as f:
    for s,ti in chapters: f.write(f"{int(s//60)}:{int(s%60):02d} {ti}\n")
print(open(OUT.rsplit('.',1)[0]+'-capitulos.txt').read())
