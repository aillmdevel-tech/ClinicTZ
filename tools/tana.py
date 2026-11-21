# usage: tana.py VIDEO OUTDIR  -> OUTDIR/<name>.json + sheet jpg
import subprocess, sys, json, re, os, math
v, od = sys.argv[1], sys.argv[2]; os.makedirs(od, exist_ok=True)
name = os.path.splitext(os.path.basename(v))[0]
def run(a): return subprocess.run(a, capture_output=True, text=True).stderr
dur = float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',v],capture_output=True,text=True).stdout.strip())
# cuts
e = run(['ffmpeg','-nostdin','-i',v,'-vf',"scale=320:-1,select='gt(scene,0.22)',showinfo",'-an','-f','null','-'])
cuts = [float(x) for x in re.findall(r'pts_time:([\d.]+)', e)]
# black + silence
e = run(['ffmpeg','-nostdin','-i',v,'-vf','scale=320:-1,blackdetect=d=0.15:pix_th=0.08','-af','silencedetect=n=-45dB:d=0.4','-f','null','-'])
black = [(float(a),float(b)) for a,b in re.findall(r'black_start:([\d.]+) black_end:([\d.]+)', e)]
sil = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', e)]
# loudness per 1s (momentary LUFS via ebur128)
e = run(['ffmpeg','-nostdin','-i',v,'-vn','-af','ebur128=peak=none','-f','null','-'])
lm = {}
for t,m in re.findall(r't:\s*([\d.]+)\s+TARGET.*?M:\s*(-?[\d.]+)', e):
    s=int(float(t)); lm.setdefault(s,[]).append(float(m))
loud = [round(max(lm.get(s,[-70])),1) for s in range(int(dur)+1)]
# windows 5s
W=5; win=[]
for i in range(math.ceil(dur/W)):
    a,b=i*W,(i+1)*W
    c=sum(1 for x in cuts if a<=x<b)
    l=[x for x in loud[a:b] if x>-70]
    win.append([a,c,round(sum(l)/len(l),1) if l else -70])
json.dump(dict(name=name,dur=round(dur,1),ncuts=len(cuts),cuts=[round(x,2) for x in cuts],black=black,silence=sil,loud=loud,win=win),open(f'{od}/{name}.json','w'))
# sheet: one frame per 2s, 8 cols
step = 2 if dur<=150 else 3
subprocess.run(['ffmpeg','-nostdin','-loglevel','error','-y','-i',v,'-vf',
 f"fps=1/{step},scale=240:-2,tile=8x{math.ceil(dur/step/8)}",
 '-frames:v','1','-q:v','4',f'{od}/{name}_sheet.jpg'])
print(name, round(dur,1), 'cuts', len(cuts), 'avgshot', round(dur/max(1,len(cuts)+1),2))
