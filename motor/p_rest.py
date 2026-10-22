import sys; sys.path.insert(0,'/tmp/claude-0/prod/exam')
from board import *
TD="/tmp/claude-0/prod/exam/timings/"
class INTRO(Board):
    TAG="QUÍMICA · PAU MADRID · JUNIO 2026"; TIMINGS=TD+"INTRO.json"
    BEATS=[
("0.1","Este es el examen de Química de la PAU de Madrid de junio de 2026, resuelto paso a paso.",
 [("h","Examen PAU Química · Madrid · Junio 2026"),("t","Resuelto paso a paso")]),
("0.2","Tienes los capítulos abajo, así que puedes saltar directamente a la pregunta que te interese.",
 [("m","1 · Redox, pila y solubilidad"),("m","2B · Configuración electrónica y espectro"),("m","4A · Termodinámica y síntesis de metanol"),("m","4B · Ácido-base y neutralización")]),
("0.3","Y si te sirve, suscríbete, porque vamos a subir los exámenes de todas las comunidades.",
 [("res","Suscríbete · exámenes de todas las comunidades")]),
]
class CIERRE(Board):
    TAG="MODO PAU"; TIMINGS=TD+"CIERRE.json"
    BEATS=[
("9.1","Y hasta aquí el examen. Si te ha servido, dale a me gusta, que ayuda mucho al canal.",[("h","¡Examen terminado!"),("t","Si te ha servido, dale a me gusta 👍")]),
("9.2","Dime en los comentarios de qué comunidad quieres el siguiente examen. ¡Mucho ánimo con la PAU!",[("t","¿Qué comunidad quieres para el siguiente examen?"),("res","¡Mucho ánimo con la PAU!")]),
]
class P2B(Board):
    TAG="PREGUNTA 2B · ESTRUCTURA ATÓMICA"; TIMINGS=TD+"P2B.json"
    BEATS=[
("2.1","Pregunta 2B. Un elemento con configuración neón más ns uno.",[("h","X:  [Ne] ns¹")]),
("2.2","Después del neón viene el nivel tres, así que n vale tres. Es el sodio: grupo 1, alcalinos, periodo 3.",[("res","n = 3  →  sodio (Na) · grupo 1 · periodo 3","na"),("box","na")]),
("2.3","La energía de ionización disminuye al bajar en un grupo. El radio aumenta y los electrones internos apantallan, así que el electrón externo está menos atraído y cuesta menos arrancarlo.",
 [("t","Energía de ionización ↓ al bajar en un grupo"),("m","más radio + más apantallamiento → el e⁻ externo está menos atraído")]),
("2.4","Apartado b: el sodio pierde su electrón 3s y queda como Na más, con la configuración del neón. Ese es su catión más estable.",
 [("clear",),("tag","PREGUNTA 2B · b) ISOELECTRÓNICOS"),("eq","Na → Na⁺ + e⁻   (configuración del Ne)")]),
("2.5","Na más tiene diez electrones. Isoelectrónicos con él: el catión Mg dos más, el gas noble neón y el anión flúor menos.",
 [("t","Na⁺ tiene 10 e⁻"),("res","Mg²⁺  ·  Ne  ·  F⁻","iso"),("box","iso")]),
("2.6","Apartado c: el electrón pasa de 3s a 3p. n sigue siendo tres. l pasa de cero a uno. m sub l puede ser menos uno, cero o uno. Y el espín puede ser más o menos un medio.",
 [("clear",),("tag","PREGUNTA 2B · c) NÚMEROS CUÁNTICOS"),("eq","3s  →  3p"),("t","n = 3 (no cambia)    l: 0 → 1"),("t","mₗ: 0 → −1, 0 o +1     mₛ: ±½")]),
("2.7","Sube a un nivel de más energía, así que es una absorción.",[("res","Sube de energía → ABSORCIÓN","abs"),("box","abs")]),
("2.8","Apartado d: E igual a h por c entre lambda. Cuidado, lambda en metros: 766,5 nanómetros son 766,5 por diez a la menos nueve metros.",
 [("clear",),("tag","PREGUNTA 2B · d) ENERGÍA DEL FOTÓN"),("eq","E = h · c / λ"),("t","λ = 766,5 nm = 766,5·10⁻⁹ m")]),
("2.9","Sale 2,59 por diez a la menos diecinueve julios. Dividimos entre 1,602 por diez a la menos diecinueve y obtenemos 1,62 electronvoltios.",
 [("t","E = 6,626·10⁻³⁴ · 3,00·10⁸ / 766,5·10⁻⁹ = 2,59·10⁻¹⁹ J"),("res","E = 2,59·10⁻¹⁹ / 1,602·10⁻¹⁹ = 1,62 eV","ev"),("box","ev")]),
]
class P4A(Board):
    TAG="PREGUNTA 4A · TERMODINÁMICA Y CINÉTICA"; TIMINGS=TD+"P4A.json"
    BEATS=[
("4.1","Pregunta 4A. Monóxido de carbono gas más dos de hidrógeno gas dan metanol líquido.",[("h","CO (g) + 2 H₂ (g) → CH₃OH (l)")]),
("4.2","Primero la entalpía de reacción: productos menos reactivos. Menos 238,7 menos menos 110,5. El hidrógeno es un elemento, así que su entalpía de formación es cero. Sale menos 128,2 kilojulios por mol.",
 [("t","ΔH°r = −238,7 − [(−110,5) + 2·0]"),("eq","ΔH°r = −128,2 kJ/mol")]),
("4.3","Ahora la entropía: 126,8 menos la suma de 197,7 más dos por 130,7. Sale menos 332,3 julios por mol y kelvin.",
 [("t","ΔS°r = 126,8 − (197,7 + 2·130,7)"),("eq","ΔS°r = −332,3 J/(mol·K)")]),
("4.4","Tiene sentido: pasamos de tres moles de gas a un líquido, así que el desorden baja.",[("m","3 mol de gas → 1 líquido: el desorden baja")]),
("4.5","Gibbs: delta H menos T por delta S. Ojo con las unidades: la entropía hay que pasarla a kilojulios.",
 [("clear",),("eq","ΔG° = ΔH° − T·ΔS°"),("bad","⚠ ΔS° en kJ: −0,3323 kJ/(mol·K)")]),
("4.6","Menos 128,2 menos 298 por menos 0,3323. Sale menos 29,2 kilojulios por mol. Negativo, así que es espontánea a 25 grados.",
 [("t","ΔG° = −128,2 − 298·(−0,3323)"),("res","ΔG° = −29,2 kJ/mol  →  espontánea","g"),("box","g")]),
("4.7","Apartado b: las tres propuestas aumentan la velocidad. El catalizador baja la energía de activación.",
 [("clear",),("tag","PREGUNTA 4A · b) VELOCIDAD"),("res","Las tres aumentan la velocidad"),("t","i) Catalizador: menor energía de activación")]),
("4.8","Subir la temperatura da más energía a las moléculas y hay más choques eficaces. Y más presión parcial significa más concentración y más choques.",
 [("t","ii) Más T: más choques eficaces (Arrhenius)"),("t","iii) Más presión parcial: más concentración, más choques")]),
("4.9","Apartado c: masa de metanol igual a volumen por densidad. 145 por 0,786, unos 114 gramos.",
 [("clear",),("tag","PREGUNTA 4A · c) ESTEQUIOMETRÍA Y GASES"),("t","m = V·d = 145 · 0,786 = 114 g de CH₃OH")]),
("4.10","Entre 32 gramos por mol salen 3,56 moles de metanol.",[("t","n = 114 / 32,0 = 3,56 mol de CH₃OH")]),
("4.11","Por cada mol de metanol hacen falta dos de hidrógeno: 7,12 moles. Pero el rendimiento es del 87 por ciento, así que en realidad reaccionó más: 7,12 entre 0,87, unos 8,18 moles.",
 [("t","n(H₂) = 2 · 3,56 = 7,12 mol"),("eq","Rendimiento 87 %:  7,12 / 0,87 = 8,18 mol de H₂")]),
("4.12","Un detalle: en las soluciones oficiales pone 8,18 gramos, pero son moles. Es una errata.",[("bad","Ojo: la solución oficial pone «8,18 g», pero son mol")]),
("4.13","Ley de los gases: V igual a nRT entre P. 8,18 por 0,082 por 298, entre 0,980. Sale 204 litros de hidrógeno.",
 [("t","V = nRT/P = 8,18 · 0,0820 · 298 / 0,980"),("res","V(H₂) = 204 L","v"),("box","v")]),
]
class P4B(Board):
    TAG="PREGUNTA 4B · ÁCIDO-BASE"; TIMINGS=TD+"P4B.json"
    BEATS=[
("5.1","Pregunta 4B. Amoniaco comercial al 8 por ciento en masa y densidad 0,85 gramos por centímetro cúbico.",[("h","NH₃ comercial · 8,0 % en masa · d = 0,85 g/cm³")]),
("5.2","Un litro de disolución pesa 850 gramos. El 8 por ciento es amoniaco: 68 gramos. Entre 17 gramos por mol, 4 moles. Así que es 4 molar.",
 [("t","1 L de disolución = 850 g  →  8 % = 68 g de NH₃"),("res","68 / 17,0 = 4,0 mol  →  [NH₃] = 4,0 M","m"),("box","m")]),
("5.3","Apartado b: amoniaco más agua da amonio más OH menos. Inicial 4, y en el equilibrio 4 menos x, x y x.",
 [("clear",),("tag","PREGUNTA 4B · b) pH Y GRADO DE DISOCIACIÓN"),("eq","NH₃ + H₂O ⇌ NH₄⁺ + OH⁻"),("t","Equilibrio:   4,0 − x        x        x")]),
("5.4","Kb igual a x al cuadrado entre 4 menos x. Como Kb es muy pequeña, aproximamos 4 menos x a 4.",[("eq","Kb = x² / (4,0 − x) ≈ x² / 4,0")]),
("5.5","x igual a la raíz de 1,8 por diez a la menos cinco por 4. Sale 8,5 por diez a la menos tres molar de OH menos.",[("t","x = √(1,8·10⁻⁵ · 4,0) = 8,5·10⁻³ M = [OH⁻]")]),
("5.6","pOH igual a 2,1, así que pH igual a 14 menos 2,1: 11,9.",[("res","pOH = 2,1   →   pH = 11,9","ph"),("box","ph")]),
("5.7","Grado de disociación: x entre la concentración inicial. 0,0021, o sea, un 0,21 por ciento. Muy pequeño, así que la aproximación era buena.",
 [("t","α = x / c₀ = 8,5·10⁻³ / 4,0 = 0,0021  (0,21 %)")]),
("5.8","Apartado c: ácido clorhídrico más hidróxido de sodio dan cloruro de sodio y agua.",
 [("clear",),("tag","PREGUNTA 4B · c) NEUTRALIZACIÓN"),("eq","HCl + NaOH → NaCl + H₂O")]),
("5.9","Moles de HCl: 2,50 por 0,015, igual a 0,0375. Moles de NaOH: 1,70 por 0,025, igual a 0,0425.",
 [("t","n(HCl) = 2,50 · 0,01500 = 0,0375 mol"),("t","n(NaOH) = 1,70 · 0,02500 = 0,0425 mol")]),
("5.10","Sobra base: 0,005 moles de NaOH. El volumen total es 40 mililitros.",[("t","Sobra NaOH: 0,0050 mol   ·   V total = 40,00 mL")]),
("5.11","Concentración de OH menos: 0,005 entre 0,040, igual a 0,125 molar. pOH 0,9. pH 13,1.",
 [("res","[OH⁻] = 0,125 M  →  pOH = 0,9  →  pH = 13,1","p"),("box","p")]),
("5.12","Error típico: calcular el pH con el ácido sin mirar cuál está en exceso. Resta siempre los moles primero.",[("bad","⚠ Resta los moles antes de calcular el pH")]),
]
