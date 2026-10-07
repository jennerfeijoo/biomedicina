#!/usr/bin/env python3
"""Build original, accessible SVG teaching diagrams; no external images required."""
from pathlib import Path
from html import escape
import textwrap

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/figures/desarrollo-dispositivos-medicos'
INK, MUTED, TEAL, BG = '#12334a', '#486174', '#087f82', '#f3f7fa'

def text(x, y, value, size=23, color=INK, weight=400):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}">{escape(value)}</text>'

def box(x, y, w, h, title, lines, accent=TEAL):
    s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="white" stroke="#cddce5" stroke-width="2"/><rect x="{x}" y="{y+18}" width="5" height="{h-36}" rx="2" fill="{accent}"/>'
    s+=text(x+22,y+38,title,25,accent,700)
    for i,line in enumerate(lines):s+=text(x+22,y+77+i*30,line)
    return s

def arrow(x1,y1,x2,y2,both=False):
    return f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{TEAL}" stroke-width="3" marker-end="url(#arrow)"'+(' marker-start="url(#back)"' if both else '')+'/>'

def figure(n,title,subtitle,body,description):
    s=f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="900" viewBox="0 0 900 900" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>
<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10Z" fill="{TEAL}"/></marker><marker id="back" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10Z" fill="{TEAL}"/></marker></defs>
<rect width="900" height="900" rx="24" fill="{BG}"/><g font-family="Arial, sans-serif">'''
    s+=text(44,48,f'CITONAUTA  /  DISPOSITIVOS MÉDICOS  /  U{n}',18,TEAL,700)
    s+=text(44,99,title,34,INK,700)+text(44,137,subtitle,22,MUTED)
    s+=body+text(44,854,'Esquema docente original · CC BY-NC 4.0',19,MUTED)+text(44,880,'Leer junto con el alcance y las fuentes de la unidad.',18,MUTED)+'</g></svg>\n'
    OUT.mkdir(parents=True,exist_ok=True);(OUT/f'unit-{n:02d}.svg').write_text(s)


def build():
    b=box(44,180,386,172,'Observación',['¿Qué ocurrió realmente?','Registrar tarea y contexto.'])
    b+=box(470,180,386,172,'Interpretación',['¿Qué podría explicarlo?','Contrastar otras hipótesis.'])
    b+=box(44,392,386,172,'Actores',['Usuario, paciente y otros','actores no siempre coinciden.'])
    b+=box(470,392,386,172,'Entorno de uso',['¿Dónde y con qué recursos?','Describir restricciones.'])
    b+=arrow(237,572,237,618)+arrow(663,572,663,618)
    b+=box(44,628,812,172,'Necesidad antes que solución',['Población + problema + resultado deseado.','Seleccionar una tecnología requiere un análisis posterior.'])
    figure(1,'De la observación a la necesidad','Cuatro perspectivas para formular una pregunta de diseño.',b,'Observación, interpretación, actores y entorno informan una necesidad. La necesidad describe población, problema y resultado; todavía no selecciona tecnología. La disposición es una síntesis docente, no una secuencia obligatoria.')

    b=box(44,185,386,160,'Necesidad',['Resultado que importa','a la población o al usuario.'])+box(470,185,386,160,'Validación',['¿Se satisface el uso previsto','en su contexto?'])+arrow(438,265,462,265,True)
    b+=box(44,410,386,160,'Requisito identificable',['Condición verificable,','con criterio de aceptación.'])+box(470,410,386,160,'Verificación',['Método, resultado y evidencia','frente al requisito.'])+arrow(438,490,462,490,True)
    b+=arrow(237,355,237,397,True)+arrow(663,355,663,397,True)
    b+=box(44,635,812,165,'Arquitectura y cambios',['Asignar requisitos a funciones, módulos e interfaces.','Mantener enlaces y revisar su impacto cuando cambia el diseño.'])
    b+=arrow(237,580,237,623,True)+arrow(663,580,663,623,True)
    figure(2,'Trazabilidad en dos direcciones','Los enlaces permiten justificar el diseño y revisar cambios.',b,'La necesidad se vincula con validación; el requisito, con verificación. Arquitectura y control de cambios mantienen estos enlaces. Las flechas dobles representan trazabilidad, no causalidad ni una secuencia temporal.')

    b=box(44,180,386,160,'Peligro y exposición',['Identificar una fuente de daño','y situaciones de exposición.'])+box(470,180,386,160,'Daño y riesgo',['Considerar probabilidad','y severidad del daño.'])+arrow(438,260,462,260)
    b+=text(44,390,'PRIORIDAD DE LOS CONTROLES',20,TEAL,700)
    for y,title,lines in [(410,'1 · Seguridad inherente',['Reducir riesgos mediante el diseño.']),(530,'2 · Medidas de protección',['Incorporar protecciones cuando corresponda.']),(650,'3 · Información de seguridad',['Comunicar riesgos y precauciones restantes.'])]:
        b+=box(44,y,812,100,title,lines)
    b+=text(44,794,'Verificar controles y evaluar riesgo residual individual y global.',23,INK,700)
    figure(3,'Del peligro al riesgo residual','La información de seguridad no sustituye un diseño más seguro.',b,'Identificar peligros y exposición, considerar probabilidad y severidad, priorizar seguridad inherente, protección e información de seguridad. Verificar controles y evaluar riesgo residual individual y global. No se propone un umbral universal de aceptación.')

    b=box(44,180,386,200,'Qué se evalúa',['Requisito y criterio previo.','Configuración y versión.','Muestra identificada.'])+box(470,180,386,200,'Cómo se evalúa',['Método y condiciones.','Instrumentos e incertidumbre.','Protocolo documentado.'])
    b+=arrow(237,390,237,438)+arrow(663,390,663,438)
    b+=box(44,450,812,165,'Resultado interpretable',['Comparar evidencia con el criterio predefinido.','Registrar desviaciones, incertidumbre y límites.'])
    b+=arrow(450,625,450,663)
    b+=box(44,675,812,125,'Cambio de diseño → análisis de impacto',['¿La evidencia previa sigue siendo aplicable a esta versión?'])
    figure(4,'Construir evidencia de verificación','Un resultado tiene sentido dentro de una configuración.',b,'El requisito, criterio, configuración y muestra se combinan con método, condiciones, instrumentos e incertidumbre para interpretar el resultado. Un cambio exige analizar la aplicabilidad de la evidencia previa.')

    b=box(44,180,386,250,'Verificación',['¿Cumple especificaciones?','Referencia: requisito definido.','Ejemplo educativo:','error de medición frente','al límite especificado.'])
    b+=box(470,180,386,250,'Validación',['¿Sirve para el uso previsto?','Referencia: necesidad y uso.','Ejemplo educativo:','usuarios representativos','realizan tareas críticas.'])
    b+=box(44,475,812,155,'Evidencia según la pregunta',['Banco, factores humanos y estudios clínicos tienen alcances','distintos. La selección depende del dispositivo y su uso.'])
    b+=box(44,670,812,130,'Límite de inferencia',['Un ensayo de banco no demuestra por sí solo beneficio clínico.'])
    figure(5,'Verificar y validar','Dos preguntas relacionadas que requieren evidencia adecuada.',b,'Verificación compara desempeño con especificaciones; validación considera necesidades y uso previsto. Un ensayo de banco, un estudio de factores humanos y un estudio clínico responden preguntas distintas; el banco por sí solo no demuestra beneficio clínico.')

    b=box(44,180,386,175,'Diseño y transferencia',['Requisitos y riesgos.','Salidas aptas para producción.'])+box(470,180,386,175,'Producción controlada',['Configuración identificada.','Procesos y registros.'])+arrow(438,268,462,268)
    b+=arrow(663,365,663,434)
    b+=box(470,447,386,175,'Información posmercado',['Quejas, incidentes y señales.','Evaluar contexto y calidad.'])+box(44,447,386,175,'Evaluación y cambios',['Actualizar riesgos y controles.','Verificar o validar según impacto.'])+arrow(462,535,438,535)
    b+=arrow(237,437,237,365)
    b+=box(44,678,812,122,'Jurisdicción, uso previsto y sistema de calidad',['Determinan obligaciones; este ciclo es una síntesis docente.'])
    figure(6,'Un ciclo de vida con retroalimentación','La vigilancia alimenta la revisión del diseño y sus controles.',b,'Diseño y transferencia llevan a producción controlada; la información posmercado alimenta evaluación y cambios, que retroalimentan diseño y riesgos. Las obligaciones dependen de jurisdicción, uso previsto y sistema de calidad; el esquema no es una vía de autorización.')

if __name__ == '__main__':
    build()
