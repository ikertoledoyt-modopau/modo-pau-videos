"""Sincroniza audio y animación de una sección.
Uso: python assemble.py AUDIO SECCION N_BEATS
Detecta los silencios (>=1.2 s) del audio, los convierte en N_BEATS tramos y guarda timings/SECCION.json.
Si hay más tramos que beats (repeticiones), avisa para revisarlo a mano."""
import subprocess, sys, json, re, os
audio, sec, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
ids = sys.argv[4].split(',') if len(sys.argv) > 4 else None
out = subprocess.run(['ffmpeg','-i',audio,'-af','silencedetect=noise=-35dB:d=1.2','-f','null','-'],capture_output=True,text=True).stderr
dur = float(re.search(r'Duration: (\d+):(\d+):([\d.]+)',out).groups()[2]) + 60*int(re.search(r'Duration: (\d+):(\d+)',out).groups()[1])
starts=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',out)]
ends=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',out)]
# segmentos de voz: entre fin de un silencio y el inicio del siguiente; el corte se pone en mitad del silencio
cuts=[(s+e)/2 for s,e in zip(starts,ends) if s>0.3 and e<dur-0.3]
bounds=[0]+cuts+[dur]
segs=[bounds[i+1]-bounds[i] for i in range(len(bounds)-1)]
print(f'{sec}: {len(segs)} tramos de voz para {n} bloques')
os.makedirs('timings',exist_ok=True)
if ids and len(segs)==n:
    json.dump(dict(zip(ids,segs)),open(f'timings/{sec}.json','w'),indent=1); print('OK timings')
else:
    print('Revisar: ', [round(s,1) for s in segs])
