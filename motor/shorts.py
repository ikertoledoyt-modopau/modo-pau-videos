# Shorts verticales (1080x1920) a partir de los mismos beats y audios del vídeo largo.
import sys; sys.path.insert(0,'/tmp/claude-0/prod/exam')
from board import *
import p1, p_rest
config.pixel_width=1080; config.pixel_height=1920; config.frame_width=9; config.frame_height=16
TD="/tmp/claude-0/prod/exam/timings/"
SRC={"P1":p1.P1,"P2B":p_rest.P2B,"P4A":p_rest.P4A,"P4B":p_rest.P4B}
MAXW=8.1; TOP=4.4; BOTTOM=-5.6

def _txt(s,kind):
    size,color,w=STY[kind]
    return Text(s,font=F,font_size=size*1.3,color=color,weight=w)
def TV(s,kind="t",depth=0):
    t=_txt(s,kind)
    if t.width<=MAXW or depth>1: 
        if t.width>MAXW: t.scale_to_fit_width(MAXW)
        return t
    # partir en dos líneas por el punto de corte más centrado
    best=None
    for sep in ["  →  "," → ",":  ",": "," = ","  ·  "," · ",", "," / "," "]:
        idx=[i for i in range(len(s)) if s.startswith(sep,i)]
        for i in idx:
            score=abs(i-len(s)/2)
            if best is None or score<best[0]: best=(score,i,sep)
        if best and best[0]<len(s)*0.3: break
    if not best: t.scale_to_fit_width(MAXW); return t
    _,i,sep=best
    a=s[:i]+(sep.rstrip() if sep.strip() in [":",","] else "")
    b=(sep.strip()+" " if sep.strip() in ["→","=","·","/"] else "")+s[i+len(sep):]
    g=VGroup(TV(a,kind,depth+1),TV(b,kind,depth+1)).arrange(DOWN,aligned_edge=LEFT,buff=.18)
    g[1].shift(RIGHT*.4)
    if g.width>MAXW: g.scale_to_fit_width(MAXW)
    return g

class ShortBoard(Board):
    SRCCLS="P1"; FIRST=""; LAST=""; HOOK=""; TAG0=""; END="Examen completo en el canal · Modo PAU"
    def construct(self):
        tim=json.load(open(TD+self.SRCCLS+".json"))
        beats=SRC[self.SRCCLS].BEATS; ids=[b[0] for b in beats]
        sel=beats[ids.index(self.FIRST):ids.index(self.LAST)+1]
        bar=Rectangle(width=9,height=.12,fill_color=TEAL,fill_opacity=1,stroke_width=0).to_edge(UP,buff=0)
        hook=Text(self.HOOK,font=F,font_size=62,color=INK,weight=BOLD,line_spacing=.9)
        if hook.width>MAXW: hook.scale_to_fit_width(MAXW)
        hook.move_to([0,6.55,0])
        self.header=self.tagtext(self.TAG0)
        brand=Text("MODO PAU · PAU Madrid 2026",font=F,font_size=30,color=TEAL,weight=BOLD).move_to([0,-7.3,0])
        self.add(bar,hook,self.header,brand)
        self.items=VGroup(); self.keys={}
        for bid,text,ops in sel:
            dur=tim[bid]; used=0
            for op in ops:
                if op[0]=="clear" and len(self.items)==0: continue
                used+=self.do(op)
            self.wait(max(.1,dur-used))
        end=Text(self.END,font=F,font_size=40,color=AMBER,weight=BOLD)
        if end.width>MAXW: end.scale_to_fit_width(MAXW)
        end.move_to([0,-6.4,0]); self.play(FadeIn(end,shift=UP*.2),run_time=.5); self.wait(1.3)
    def tagtext(self,s):
        t=Text(s,font=F,font_size=30,color=MUTED)
        if t.width>MAXW: t.scale_to_fit_width(MAXW)
        return t.move_to([0,5.15,0])
    def place(self,m):
        if len(self.items)==0: m.move_to([0,TOP,0],aligned_edge=UP).to_edge(LEFT,buff=.45)
        else: m.next_to(self.items[-1],DOWN,buff=.45).to_edge(LEFT,buff=.45)
        if m.get_bottom()[1]<BOTTOM:
            self.play(FadeOut(self.items),run_time=.4); self.items=VGroup(); self.keys={}
            m.move_to([0,TOP,0],aligned_edge=UP).to_edge(LEFT,buff=.45); return .4
        return 0
    def do(self,op):
        k=op[0]
        if k=="tag":
            new=self.tagtext(op[1]); self.play(Transform(self.header,new),run_time=.4); return .4
        if k in STY:
            m=TV(op[1],k); used=self.place(m)
            if len(op)>2: self.keys[op[2]]=m
            self.items.add(m); self.play(FadeIn(m,shift=UP*.15),run_time=.6); return used+.6
        return Board.do(self,op)

class S_PILA(ShortBoard):
    SRCCLS="P1"; FIRST="1.11"; LAST="1.13"; HOOK="¿Ánodo o cátodo?\nLa pila de la PAU 2026"; TAG0="PAU MADRID 2026 · QUÍMICA · PILA"
class S_KS(ShortBoard):
    SRCCLS="P1"; FIRST="1.14"; LAST="1.19"; HOOK="¿Cuándo precipita?\nKs en la PAU 2026"; TAG0="PAU MADRID 2026 · SOLUBILIDAD"
class S_FOTON(ShortBoard):
    SRCCLS="P2B"; FIRST="2.8"; LAST="2.9"; HOOK="Energía de un fotón\nen eV (PAU 2026)"; TAG0="PAU MADRID 2026 · ESPECTRO"
class S_GIBBS(ShortBoard):
    SRCCLS="P4A"; FIRST="4.5"; LAST="4.6"; HOOK="El fallo de unidades\nque más puntos quita"; TAG0="PAU MADRID 2026 · GIBBS"
class S_PH(ShortBoard):
    SRCCLS="P4B"; FIRST="5.3"; LAST="5.7"; HOOK="pH del amoniaco\npaso a paso"; TAG0="PAU MADRID 2026 · BASE DÉBIL"
class S_NEUTRA(ShortBoard):
    SRCCLS="P4B"; FIRST="5.8"; LAST="5.12"; HOOK="¿Qué sobra, ácido o base?\npH tras neutralizar"; TAG0="PAU MADRID 2026 · NEUTRALIZACIÓN"
