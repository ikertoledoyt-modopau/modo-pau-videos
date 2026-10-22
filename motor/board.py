# Motor de "pizarra": cada bloque del guion es un beat; la animación dura lo que dure el audio del bloque.
from manim import *
import json, os, re
config.pixel_width=1920; config.pixel_height=1080
config.background_color="#0F1D1A"
TEAL="#2EC4A0"; AMBER="#FFB454"; INK="#EAF2EE"; MUTED="#8FA69D"; RED="#FF6B6B"
F="Inter"
STY={"h":(52,TEAL,BOLD),"t":(42,INK,NORMAL),"eq":(50,INK,BOLD),"res":(54,AMBER,BOLD),"m":(34,MUTED,NORMAL),"bad":(42,RED,BOLD)}
def T(s,kind="t"):
    size,color,w=STY[kind]
    t=Text(s,font=F,font_size=size,color=color,weight=w)
    if t.width>12.6: t.scale_to_fit_width(12.6)
    return t
def est(text): return max(2.5, len(text.split())/2.6+0.8)

class Board(Scene):
    BEATS=[]      # [(id, texto_guion, [ops])]
    TAG=""        # p.ej. "PREGUNTA 1"
    TIMINGS=None  # json {id: segundos}
    def construct(self):
        tim={}
        if self.TIMINGS and os.path.exists(self.TIMINGS): tim=json.load(open(self.TIMINGS))
        self.header=T(self.TAG,"m").to_corner(UL,buff=.5)
        brand=T("Modo PAU · Química Madrid 2026","m").scale(.7).to_corner(DR,buff=.35)
        self.add(self.header,brand)
        self.items=VGroup(); self.keys={}
        for bid,text,ops in self.BEATS:
            dur=tim.get(bid,est(text)); used=0
            for op in ops:
                used+=self.do(op)
            self.wait(max(.1,dur-used))
    def place(self,m):
        if len(self.items)==0: m.to_edge(UP,buff=1.3).to_edge(LEFT,buff=.8)
        else: m.next_to(self.items[-1],DOWN,buff=.32).to_edge(LEFT,buff=.8)
        if m.get_bottom()[1]<-3.3:
            self.play(FadeOut(self.items),run_time=.4); self.items=VGroup(); self.keys={}
            m.to_edge(UP,buff=1.3).to_edge(LEFT,buff=.8); return .4
        return 0
    def do(self,op):
        k=op[0]
        if k=="clear":
            if len(self.items): self.play(FadeOut(self.items),run_time=.4)
            self.items=VGroup(); self.keys={}; return .4
        if k=="tag":
            new=T(op[1],"m").to_corner(UL,buff=.5); self.play(Transform(self.header,new),run_time=.4); return .4
        if k in STY:
            m=T(op[1],k); used=self.place(m)
            if len(op)>2: self.keys[op[2]]=m
            self.items.add(m); self.play(FadeIn(m,shift=UP*.15),run_time=.6); return used+.6
        if k=="box":
            if op[1] not in self.keys: return 0
            m=self.keys[op[1]]; b=SurroundingRectangle(m,color=AMBER,buff=.12,corner_radius=.08)
            self.items.add(b); self.play(Create(b),run_time=.5); return .5
        if k=="mark":
            if op[1] not in self.keys: return 0
            m=self.keys[op[1]]; self.play(m.animate.set_color(op[2] if len(op)>2 else AMBER),run_time=.4); return .4
        raise ValueError(k)
