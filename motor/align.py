"""Alinea bloques del guion con el audio sin reconocimiento de voz.
Elige N-1 cortes entre los silencios para que cada tramo dure lo esperado según sus palabras
(ritmo del propio audio) y premia cortar en silencios largos. Programación dinámica."""
import subprocess, re, math, json, sys, importlib.util
def silences(wav, d=0.45):
    e=subprocess.run(['ffmpeg','-i',wav,'-af',f'silencedetect=noise=-38dB:d={d}','-f','null','-'],capture_output=True,text=True).stderr
    m=re.search(r'Duration: (\d+):(\d+):([\d.]+)',e); dur=int(m[1])*3600+int(m[2])*60+float(m[3])
    st=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',e)]; en=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',e)]
    return dur,[((s+t)/2,t-s) for s,t in zip(st,en) if 0.3<s and t<dur-0.3]
def align(wav, words, lam=1.2):
    dur,c=silences(wav); n=len(words); W=sum(words); rate=dur/W
    pos=[0.0]+[p for p,_ in c]+[dur]; sd=[0]+[s for _,s in c]+[0]; K=len(pos)
    INF=1e18; best=[[INF]*K for _ in range(n+1)]; prev=[[-1]*K for _ in range(n+1)]
    best[0][0]=0
    for i in range(1,n+1):
        exp=words[i-1]*rate
        for k in range(1,K):
            if i==n and k!=K-1: continue
            if i<n and k==K-1: continue
            bonus=-lam*min(sd[k],2.5) if i<n else 0
            for j in range(k):
                if best[i-1][j]>=INF: continue
                seg=pos[k]-pos[j]
                if seg<0.8: continue
                cost=best[i-1][j]+math.log(seg/exp)**2+bonus
                if cost<best[i][k]: best[i][k]=cost; prev[i][k]=j
    k=K-1; cuts=[]
    for i in range(n,0,-1):
        j=prev[i][k]; cuts.append((pos[j],pos[k])); k=j
    return list(reversed(cuts))
if __name__=='__main__':
    wav,mod,cls=sys.argv[1:4]
    spec=importlib.util.spec_from_file_location(mod,f'/tmp/claude-0/prod/exam/{mod}.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    B=getattr(m,cls).BEATS; W=json.load(open('/tmp/claude-0/prod/exam/words.json')); words=[W.get(b[0],len(b[1].split())) for b in B]
    segs=align(wav,words)
    json.dump({b[0]:e-s for b,(s,e) in zip(B,segs)},open(f'/tmp/claude-0/prod/exam/timings/{cls}.json','w'),indent=1)
    for b,(s,e),w in zip(B,segs,words): print(b[0],f'{s:6.1f}-{e:6.1f}',f'{e-s:5.1f}s',w,'pal')
