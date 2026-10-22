"""Transcribe el audio por trozos (cortados en silencios) con Whisper y asigna cada trozo al bloque del guion
que mejor encaja, en orden. Detecta repeticiones (bloque leído dos veces) y se queda con la última toma.
Uso: python asr_align.py WAV CLASE  -> timings/CLASE.json y una lista de cortes a eliminar."""
import sys, re, json, subprocess, unicodedata, difflib
import numpy as np, soundfile as sf, sherpa_onnx
M='/tmp/claude-0/asr/sherpa-onnx-whisper-base/'
rec=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=M+'base-encoder.int8.onnx',decoder=M+'base-decoder.int8.onnx',tokens=M+'base-tokens.txt',language='es',task='transcribe',num_threads=4)
def norm(s):
    s=unicodedata.normalize('NFD',s.lower()); s=''.join(c for c in s if unicodedata.category(c)!='Mn')
    return re.findall(r'[a-zñ]+',s)
wav,cls=sys.argv[1],sys.argv[2]
x,sr=sf.read(wav)
if x.ndim>1: x=x.mean(1)
if sr!=16000:
    subprocess.run(['ffmpeg','-v','error','-y','-i',wav,'-ac','1','-ar','16000','/tmp/claude-0/asr/tmp.wav'],check=True); x,sr=sf.read('/tmp/claude-0/asr/tmp.wav')
dur=len(x)/sr
e=subprocess.run(['ffmpeg','-i',wav,'-af','silencedetect=noise=-38dB:d=0.45','-f','null','-'],capture_output=True,text=True).stderr
st=[float(v) for v in re.findall(r'silence_start: ([\d.]+)',e)]; en=[float(v) for v in re.findall(r'silence_end: ([\d.]+)',e)]
cuts=[0.0]+[(a+b)/2 for a,b in zip(st,en) if 0.2<a and b<dur-0.2]+[dur]
chunks=[]
for a,b in zip(cuts,cuts[1:]):
    s=rec.create_stream(); s.accept_waveform(sr,x[int(a*sr):int(b*sr)].astype(np.float32)); rec.decode_stream(s)
    chunks.append((a,b,s.result.text.strip()))
# guion
G=open('/mnt/project-files/canal/guiones/GUION Quimica Madrid 2026 junio.txt').read()
pref={'P1':'1.','P2B':'2.','P4A':'4.','P4B':'5.','CIERRE':'9.','INTRO':'0.'}[cls]
blocks=[(m[0],norm(m[1])) for m in re.findall(r'^\[(\d+\.\d+)\] (.+)$',G,re.M) if m[0].startswith(pref)]
if cls=='INTRO': blocks=[('0.1',norm('Este es el examen de Química de la PAU de Madrid de junio de 2026, resuelto paso a paso.')),('0.2',norm('Tienes los capítulos abajo, así que puedes saltar directamente a la pregunta que te interese.')),('0.3',norm('Y si te sirve, suscríbete, porque vamos a subir los exámenes de todas las comunidades.'))]
# asignar cada trozo al bloque cuyo texto contiene mejor sus palabras (búsqueda local, monotónica con retroceso permitido para repeticiones)
def score(cw,bw):
    if not cw: return 0
    sm=difflib.SequenceMatcher(None,cw,bw); return sum(m.size for m in sm.get_matching_blocks())/len(cw)
assign=[]; cur=0
for a,b,t in chunks:
    cw=norm(t)
    cands=range(max(0,cur-1),min(len(blocks),cur+3))
    sc={i:score(cw,blocks[i][1]) for i in cands}
    i=max(sc,key=lambda k:(sc[k], -abs(k-cur)))
    if not cw or sc[i]<0.3: i=cur
    assign.append(i); cur=max(cur,i) if i>=cur else i
# tramos por bloque: última aparición continua de cada bloque (si se repite, la toma buena es la última)
spans={}
for (a,b,t),i in zip(chunks,assign):
    k=blocks[i][0]
    if k in spans and spans[k][2]==len(spans)-1 and spans[k][1]>=a-0.01: spans[k][1]=b
    else: spans[k]=[a,b,len(spans)]
order=[k for k,_ in blocks]
missing=[k for k in order if k not in spans]
print('trozos:',len(chunks),' bloques sin audio:',missing)
for (a,b,t),i in zip(chunks,assign): print(f'{a:6.1f}-{b:6.1f} [{blocks[i][0]}] {t}')
json.dump({k:spans[k][:2] for k in order if k in spans},open(f'/tmp/claude-0/prod/exam/timings/{cls}.spans.json','w'),indent=1)
