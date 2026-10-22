"""Monta el audio final de una sección a partir de los tramos buenos de cada bloque.
Uso: python edit.py WAV CLASE SPANS.json  -> clean/CLASE_edit.wav y timings/CLASE.json"""
import sys, json, subprocess
wav,cls,sp=sys.argv[1:4]; spans=json.load(open(sp)); PAD=0.35
parts=[]; tim={}
for i,(k,v) in enumerate(spans.items()):
    pieces=v if isinstance(v[0],list) else [v]
    for j,(a,b) in enumerate(pieces):
        f=f'/tmp/claude-0/asr/{cls}_{i}_{j}.wav'
        subprocess.run(['ffmpeg','-v','error','-y','-i',wav,'-af',f'atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st={max(0,b-a-0.05)}:d=0.05,apad=pad_dur={PAD}','-ar','48000','-ac','1',f],check=True)
        parts.append(f)
    tim[k]=sum(b-a+PAD for a,b in pieces)
open('/tmp/claude-0/asr/list.txt','w').write(''.join(f"file '{p}'\n" for p in parts))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','/tmp/claude-0/asr/list.txt',f'/tmp/claude-0/prod/exam/clean/{cls}_edit.wav'],check=True)
json.dump(tim,open(f'/tmp/claude-0/prod/exam/timings/{cls}.json','w'),indent=1)
print(cls,'total',round(sum(tim.values()),1),'s')
