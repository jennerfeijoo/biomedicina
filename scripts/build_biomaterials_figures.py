#!/usr/bin/env python3
"""Original biomaterials teaching figures. Matplotlib/NumPy are authoring-only dependencies."""
from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Ellipse
from build_electronics_figures import setup as base_setup, TEAL, BLUE, ORANGE, INK
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/figures/biomateriales'
plt.rcParams['svg.hashsalt'] = 'citonauta-biomaterials-v1'

def setup(title, subtitle, diagram=False):
    f, a = base_setup(title, subtitle)
    f.texts[0].set_text('CITONAUTA / BIOMATERIALES')
    if diagram:
        a.set(xlim=(0, 10), ylim=(0, 6)); a.axis('off')
    return f, a

def box(a, x, y, w, h, text, color=TEAL):
    a.add_patch(Rectangle((x,y),w,h,facecolor='white',edgecolor=color,lw=2))
    a.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=13,color=INK)

def arrow(a, start, end):
    a.annotate('', xy=end, xytext=start, arrowprops={'arrowstyle':'->','color':INK,'lw':1.8})

def save(f, n, note):
    f.text(.06,.095,note,fontsize=12)
    f.text(.06,.035,'Esquemas educativos originales · CC BY-NC 4.0 · No son resultados experimentales',fontsize=11,color='#486174')
    OUT.mkdir(parents=True,exist_ok=True)
    f.savefig(OUT/f'unit-{n:02d}.svg',metadata={'Date':None,'Creator':'CitoNauta','Description':note})
    plt.close(f)

def build():
    f,a=setup('Seleccionar exige definir el contexto','Las familias orientan la búsqueda; los requisitos deciden qué datos hacen falta.',True)
    box(a,0,4,4.2,1.5,'Uso previsto\nFunción · cargas · contacto · duración')
    box(a,5.8,4,4.2,1.5,'Candidatos\nMetales · cerámicas\nPolímeros · compuestos',BLUE)
    box(a,0,1,4.2,1.8,'Requisitos explícitos\nRestricciones obligatorias\nObjetivos de optimización')
    box(a,5.8,1,4.2,1.8,'Comparación trazable\nGrado · proceso · geometría\nPropiedades y condiciones de ensayo',BLUE)
    arrow(a,(2.1,4),(2.1,2.8));arrow(a,(7.9,4),(7.9,2.8));arrow(a,(4.2,1.9),(5.8,1.9))
    save(f,1,'La salida es una preselección provisional, no una garantía de seguridad o desempeño clínico.\nLa biocompatibilidad depende del dispositivo y su uso; no es una etiqueta universal del material.')

    f,a=setup('La geometría cambia la fuerza necesaria','Dos probetas hipotéticas del mismo material lineal: E = 1 000 MPa; longitud inicial = 20 mm.')
    a.remove();left=f.add_axes([.10,.29,.36,.42]);right=f.add_axes([.60,.29,.35,.42])
    extension=np.linspace(0,.2,101);strain=extension/20;stress=1000*strain
    for area,color,style in [(2,TEAL,'-'),(4,ORANGE,'--')]:
        left.plot(extension,stress*area,color=color,ls=style,lw=2.5,label=f'Área = {area} mm²')
        right.plot(strain*100,stress,color=color,ls=style,lw=2.5,label=f'Área = {area} mm²')
    left.set(xlabel='Alargamiento (mm)',ylabel='Fuerza (N)');right.set(xlabel='Deformación (%)',ylabel='Tensión nominal (MPa)')
    left.legend(fontsize=10);right.legend(fontsize=10)
    save(f,2,'Tensión nominal = F / A₀; deformación = ΔL / L₀. Al normalizar, las curvas coinciden.\nModelo elástico ideal a pequeña deformación: no incluye fluencia, rotura ni viscoelasticidad.')

    f,a=setup('La célula encuentra una interfaz acondicionada','Esquema conceptual de adhesión mediada por proteínas; sin escala espacial ni temporal.',True)
    a.add_patch(Rectangle((.3,.2),6.1,.7,color=BLUE));a.text(3.35,.55,'Superficie del material',color='white',ha='center',va='center')
    for x in [1,2.4,3.8,5.2]:
        a.add_patch(Ellipse((x,1.25),.85,.4,angle=20,facecolor=ORANGE))
    a.add_patch(Ellipse((3.35,4),5.8,2,facecolor='#d4ecea',edgecolor=TEAL,lw=2));a.text(3.35,4.25,'Célula',ha='center',fontsize=16)
    for x in [2.4,3.8]:
        a.plot([x,x],[1.5,3.1],color=INK,lw=2);a.plot([x-.2,x,x+.2],[1.65,1.45,1.65],color=INK,lw=2)
    a.text(7,4.2,'Adhesión y señalización\ndependen del contexto',fontsize=12,va='center')
    a.text(7,2.6,'Receptores de adhesión\n(p. ej., integrinas)',fontsize=12,va='center');arrow(a,(6.8,2.6),(3.8,2.3))
    a.text(7,1.25,'Proteínas adsorbidas',fontsize=12,va='center');arrow(a,(6.8,1.25),(5.65,1.25))
    save(f,3,'La composición y conformación de la capa adsorbida condicionan la interacción celular.\nAdhesión celular no equivale a ausencia de inflamación ni demuestra biocompatibilidad completa.')

    f,a=setup('Masa retenida y longitud de cadena difieren','Ejemplo hipotético de degradación: ambas variables están normalizadas a su valor inicial.')
    t=np.linspace(0,10,101);molar=np.exp(-.25*t);mass=np.exp(-.12*np.maximum(t-4,0)**2)
    a.plot(t,molar,color=TEAL,lw=2.5,label='Masa molar media normalizada');a.plot(t,mass,color=ORANGE,lw=2.5,ls='--',label='Masa de la muestra normalizada')
    a.set(xlabel='Tiempo arbitrario (u. a.)',ylabel='Fracción del valor inicial',ylim=(0,1.1));a.legend()
    save(f,4,'La escisión de cadenas puede preceder a la pérdida apreciable de masa de la muestra.\nCurvas didácticas elegidas para ilustrarlo: no predicen un polímero, una vida útil ni una tasa in vivo.')

    f,a=setup('Cada medición responde a una pregunta','La caracterización combina resultados; ninguna técnica describe por sí sola todo el material.',True)
    box(a,0,3.4,4.5,2,'Mecánica\nCurva de tracción → módulo\nGeometría y velocidad del ensayo')
    box(a,5.5,3.4,4.5,2,'Topografía\nPerfil o mapa → rugosidad\nEscala y filtrado de la medida',BLUE)
    box(a,0,.4,4.5,2,'Mojabilidad\nGota → ángulo de contacto\nLíquido, limpieza y protocolo',ORANGE)
    box(a,5.5,.4,4.5,2,'Química superficial\nEspectro XPS → composición\nProfundidad y calibración',BLUE)
    save(f,5,'Documentar mensurando, muestra, método, unidades, incertidumbre y condiciones de medida.\nUna superficie rugosa no es necesariamente más mojable; un ángulo aislado no prueba seguridad.')

    f,a=setup('Evaluar la configuración final','El procesamiento forma parte del problema de evaluación biológica.',True)
    box(a,0,4,4.3,1.5,'Material y fabricación\nComposición · residuos · acabado',BLUE)
    box(a,0,1,4.3,1.5,'Esterilización, si corresponde\nMétodo y condiciones definidos',ORANGE)
    box(a,5.7,4,4.3,1.5,'Dispositivo final\nComponentes e interacciones',TEAL)
    box(a,5.7,1,4.3,1.5,'Evaluación contextual\nContacto · duración · exposición',TEAL)
    arrow(a,(4.3,4.75),(5.7,4.75));arrow(a,(4.3,1.75),(5.7,4.2));arrow(a,(7.85,4),(7.85,2.5))
    save(f,6,'Los datos del material de partida no cubren automáticamente la configuración final procesada.\nEsquema de razonamiento: no es una lista completa de ensayos ni una autorización de uso clínico.')
    record={'scope':'Ejemplos hipotéticos; no son datos de materiales reales','young_modulus_mpa':1000,'initial_length_mm':20,'areas_mm2':[2,4],'final_extension_mm':float(extension[-1]),'final_strain':float(strain[-1]),'final_stress_mpa':float(stress[-1]),'final_forces_n':[float(stress[-1]*v) for v in [2,4]],'degradation_time':t.tolist(),'molar_fraction':molar.tolist(),'specimen_mass_fraction':mass.tolist(),'molar_formula':'exp(-0.25*t)','mass_formula':'exp(-0.12*max(t-4,0)^2)'}
    (OUT/'calculation-record.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':build()
