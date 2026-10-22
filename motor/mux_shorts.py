import json,subprocess,os
os.chdir('/tmp/claude-0/prod/exam'); os.makedirs('out/shorts',exist_ok=True)
S={"S_PILA":("P1","1.11","1.13"),"S_KS":("P1","1.14","1.19"),"S_FOTON":("P2B","2.8","2.9"),"S_GIBBS":("P4A","4.5","4.6"),"S_PH":("P4B","5.3","5.7"),"S_NEUTRA":("P4B","5.8","5.12")}
for name,(c,a,b) in S.items():
    t=json.load(open(f'timings/{c}.json'));ks=list(t);i,j=ks.index(a),ks.index(b)
    off=sum(t[k] for k in ks[:i]);d=sum(t[k] for k in ks[i:j+1])
    v=f'media/videos/shorts/1920p30/{name}.mp4'
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',v,'-ss',str(off),'-t',str(d),'-i',f'clean/{c}_edit.wav',
      '-filter_complex','[1:a]afade=t=out:st=%f:d=0.3,apad[a]'%(d-0.3),'-map','0:v','-map','[a]','-shortest',
      '-c:v','libx264','-crf','21','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-ar','48000','-ac','2','-movflags','+faststart',f'out/shorts/{name}.mp4'],check=True)
    print(name, subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'out/shorts/{name}.mp4'],capture_output=True,text=True).stdout.strip(), os.path.getsize(f'out/shorts/{name}.mp4')//1024,'KB')
