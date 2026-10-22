"""Limpia una grabación: quita los clics de empezar/parar (ruidos cortos al principio y al final),
reduce ruido, iguala volumen y deja 0,3 s de margen. Uso: python clean.py ENTRADA SALIDA.wav"""
import subprocess, sys, re
src, dst = sys.argv[1], sys.argv[2]
err = subprocess.run(['ffmpeg','-i',src,'-af','silencedetect=noise=-38dB:d=0.25','-f','null','-'],capture_output=True,text=True).stderr
m = re.search(r'Duration: (\d+):(\d+):([\d.]+)', err); dur = int(m[1])*3600+int(m[2])*60+float(m[3])
st=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',err)]
en=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',err)]
if len(en)<len(st): en.append(dur)
# tramos con sonido = huecos entre silencios
voiced=[]; t=0.0
for s,e in zip(st,en):
    if s>t: voiced.append([t,s])
    t=e
if t<dur: voiced.append([t,dur])
# los tramos muy cortos al principio o al final son clics
while voiced and voiced[0][1]-voiced[0][0]<0.45: voiced.pop(0)
while voiced and voiced[-1][1]-voiced[-1][0]<0.45: voiced.pop()
a=max(0,voiced[0][0]-0.3); b=min(dur,voiced[-1][1]+0.25)
fo=max(0,b-a-0.15)
af=f"atrim={a}:{b},asetpts=PTS-STARTPTS,highpass=f=80,lowpass=f=12000,afftdn=nf=-25,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,loudnorm=I=-16:TP=-1.5:LRA=9,afade=t=in:d=0.05,afade=t=out:st={fo}:d=0.15"
subprocess.run(['ffmpeg','-v','error','-y','-i',src,'-af',af,'-ar','48000',dst],check=True)
print(f'recortado {a:.2f}-{b:.2f} de {dur:.2f} s')
