from manim import *
config.pixel_width=1080; config.pixel_height=1920
config.frame_width=9; config.frame_height=16
config.background_color="#0F1D1A"
TEAL="#2EC4A0"; AMBER="#FFB454"; INK="#EAF2EE"; MUTED="#8FA69D"; RED="#FF6B6B"
F="Inter"
def T(s,size=48,color=INK,w=BOLD):
    t=Text(s,font=F,font_size=size,color=color,weight=w)
    if t.width>8: t.scale_to_fit_width(8)
    return t

class ReactivoLimitante(Scene):
    def construct(self):
        tag=T("PAU · QUÍMICA",26,TEAL).to_edge(UP,buff=1.1)
        self.add(tag)
        hook=VGroup(T("¿Cuál es el",80),T("reactivo limitante?",80,AMBER)).arrange(DOWN,buff=.3)
        self.play(FadeIn(hook,shift=UP*.3),run_time=.6); self.wait(1.6)
        self.play(hook.animate.scale(.6).next_to(tag,DOWN,buff=.5))
        rx=T("2 H₂  +  O₂  →  2 H₂O",76).next_to(hook,DOWN,buff=1.4)
        data=T("Tenemos 4 g de H₂ y 16 g de O₂",42,MUTED,NORMAL).next_to(rx,DOWN,buff=.4)
        self.play(Write(rx),run_time=1.2); self.play(FadeIn(data)); self.wait(2)
        p1=T("1 · Pasa a moles",46,TEAL).next_to(data,DOWN,buff=1.2).to_edge(LEFT,buff=.6)
        m1=T("H₂:  4 ÷ 2 = 2 mol",56).next_to(p1,DOWN,buff=.35).align_to(p1,LEFT)
        m2=T("O₂:  16 ÷ 32 = 0,5 mol",56).next_to(m1,DOWN,buff=.25).align_to(p1,LEFT)
        self.play(FadeIn(p1)); self.play(Write(m1)); self.wait(.8); self.play(Write(m2)); self.wait(2)
        p2=T("2 · Compara con la reacción",46,TEAL).next_to(m2,DOWN,buff=1.1).align_to(p1,LEFT)
        c1=T("2 mol de H₂ necesitan 1 mol de O₂",42,INK,NORMAL).next_to(p2,DOWN,buff=.35).align_to(p1,LEFT)
        c2=T("pero solo hay 0,5 mol",46,RED,NORMAL).next_to(c1,DOWN,buff=.2).align_to(p1,LEFT)
        self.play(FadeIn(p2)); self.play(FadeIn(c1)); self.wait(1.5); self.play(FadeIn(c2)); self.wait(1)
        box=SurroundingRectangle(m2,color=AMBER,buff=.18,corner_radius=.1)
        lim=T("LIMITANTE",38,"#0F1D1A").add_background_rectangle(color=AMBER,opacity=1,buff=.12).next_to(box,DOWN,buff=.1).align_to(box,RIGHT)
        self.play(Create(box),FadeIn(lim,scale=1.3)); self.wait(2)
        steps=VGroup(p1,m1,p2,c1,c2)
        self.play(FadeOut(steps),FadeOut(data),VGroup(m2,box,lim).animate.next_to(rx,DOWN,buff=.6))
        p3=T("3 · Calcula con el limitante",46,TEAL).next_to(m2,DOWN,buff=1.3)
        r1=T("H₂O = 0,5 × 2 = 1 mol",56).next_to(p3,DOWN,buff=.35)
        r2=T("1 mol × 18 g/mol = 18 g",56,AMBER).next_to(r1,DOWN,buff=.25)
        self.play(FadeIn(p3)); self.play(Write(r1)); self.wait(1); self.play(Write(r2)); self.wait(2)
        chk=VGroup(T("Comprueba: sobran 2 g de H₂",42,MUTED,NORMAL),T("4 + 16 = 18 + 2  ✓",54,TEAL)).arrange(DOWN,buff=.2).next_to(r2,DOWN,buff=1.2)
        self.play(FadeIn(chk)); self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not tag])
        cta=VGroup(T("El error típico:",60,INK),T("elegir el que tiene",60,INK,NORMAL),T("menos gramos",60,RED),T("Compara siempre",56,TEAL),T("en moles",56,TEAL)).arrange(DOWN,buff=.3)
        self.play(FadeIn(cta,shift=UP*.3)); self.wait(3)
