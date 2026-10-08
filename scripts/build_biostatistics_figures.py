#!/usr/bin/env python3
"""Original synthetic teaching plots. Build dependency: numpy and matplotlib."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/figures/bioestadistica'
TEAL='#087f82'; BLUE='#315f9c'; ORANGE='#a44815'; INK='#12334a'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':13,'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':INK,'text.color':INK,'svg.fonttype':'none','svg.hashsalt':'citonauta-bioestadistica-v1'})

def setup(title,subtitle):
 f,a=plt.subplots(figsize=(12,8));f.patch.set_facecolor('#f3f7fa');a.set_facecolor('#ffffff');f.subplots_adjust(left=.12,right=.95,bottom=.26,top=.76)
 f.text(.06,.93,'CITONAUTA / BIOESTADÍSTICA',color=TEAL,weight='bold',fontsize=13)
 f.text(.06,.865,title,fontsize=23,weight='bold');f.text(.06,.81,subtitle,fontsize=13)
 return f,a

def save(f,n,note):
 f.text(.06,.095,note,fontsize=12);f.text(.06,.035,'Datos o modelos sintéticos · Elaboración propia · CC BY-NC 4.0',fontsize=11,color='#486174')
 OUT.mkdir(parents=True,exist_ok=True)
 f.savefig(OUT/f'unit-{n:02d}.svg',metadata={'Date':None,'Creator':'CitoNauta','Description':note})
 plt.close(f)

def build():
 f,a=setup('Mediciones no equivalen a participantes','Tres participantes, cuatro visitas: doce observaciones con estructura de dependencia.')
 visits=np.arange(1,5)
 for label,vals in [('A',[10,11,12,11]),('B',[18,17,19,18]),('C',[26,27,25,28])]:a.plot(visits,vals,'o-',label=f'Participante {label}',lw=2)
 a.set(xlabel='Visita',ylabel='Medición (unidades arbitrarias)',xticks=visits);a.legend(loc='center left',bbox_to_anchor=(.02,.62))
 save(f,1,'Conservar el identificador individual permite reconocer las medidas repetidas.\nNo tratar automáticamente las doce observaciones como independientes.')

 f,a=setup('Un extremo cambia la media','Las dos series comparten siete valores; solo cambia el octavo.')
 for y,values,label in [(1,[1,2,3,4,5,6,7,8],'Serie A'),(0,[1,2,3,4,5,6,7,24],'Serie B')]:
  a.scatter(values,[y]*8,s=75,color=TEAL,label='Observaciones' if y else None)
  a.scatter([np.mean(values)],[y+.17],s=120,marker='D',color=ORANGE,label='Media' if y else None)
  a.scatter([np.median(values)],[y-.17],s=150,marker='|',color=BLUE,label='Mediana' if y else None)
 a.set(yticks=[0,1],yticklabels=['Serie B','Serie A'],xlabel='Valor (unidades arbitrarias)',ylim=(-.5,1.5));a.legend(loc='upper right')
 save(f,2,'La media cambia de 4,5 a 6,5; la mediana permanece en 4,5.\nUn valor extremo se investiga: no se elimina solo por ser diferente.')

 f,a=setup('La media muestral también varía','Modelo: observaciones independientes normales, media 0 y desviación estándar 1.')
 x=np.linspace(-3.5,3.5,900)
 for n,c in [(1,BLUE),(4,ORANGE),(25,TEAL)]:
  se=1/np.sqrt(n);a.plot(x,np.exp(-.5*(x/se)**2)/(se*np.sqrt(2*np.pi)),color=c,lw=2.5,label=f'n = {n}; error estándar = {se:g}')
 a.set(xlabel='Media muestral',ylabel='Densidad de probabilidad');a.legend()
 save(f,3,'En este modelo, el error estándar es 1/√n. Las curvas representan densidades.\nLa independencia es un supuesto; aumentar n no elimina un sesgo de diseño.')

 f,a=setup('El 95 % describe un procedimiento','Treinta muestras simuladas de tamaño 25; media real 0 y desviación conocida 1.')
 rng=np.random.default_rng(20261008);means=rng.normal(size=(30,25)).mean(axis=1);half=1.959963984540054/5
 for i,m in enumerate(means,1):
  hit=abs(m)<=half;a.errorbar(m,i,xerr=half,fmt='o' if hit else 's',color=TEAL if hit else ORANGE,capsize=3)
 a.axvline(0,ls='--',color=INK,label='Media real = 0');a.set(xlabel='Media e intervalo de confianza',ylabel='Muestra simulada',ylim=(0,31));a.legend(loc='upper right')
 hits=int(np.sum(np.abs(means)<=half))
 save(f,4,f'En esta realización, {hits}/30 intervalos contienen la media real. No se fuerza una cobertura de 95 %.\nIntervalo normal con desviación poblacional conocida: media ± 1,96/√25.')

 f,a=setup('Comparar cambios dentro de cada persona','Seis pares sintéticos: las líneas conservan el vínculo entre mediciones.')
 before=np.array([10,14,18,22,26,30]);after=before+np.array([3,1,4,-1,2,3])
 for b,e in zip(before,after):a.plot([0,1],[b,e],'o-',color=TEAL,alpha=.8)
 a.set(xticks=[0,1],xticklabels=['Antes','Después'],xlim=(-.3,1.3),ylabel='Medición (unidades arbitrarias)')
 save(f,5,'Un análisis pareado considera las diferencias individuales y sus supuestos.\nUna comparación antes/después sin control no demuestra por sí sola un efecto causal.')

 f,a=setup('Una relación lineal en log-odds','Modelo ilustrativo: p = 1 / (1 + exp(−x)); no representa pacientes reales.')
 x=np.linspace(-5,5,500);a.plot(x,1/(1+np.exp(-x)),lw=3,color=TEAL);a.axhline(.5,ls=':',color=BLUE);a.scatter([0],[.5],s=70,color=BLUE)
 a.set(xlabel='Predictor x (unidades arbitrarias)',ylabel='Probabilidad del modelo',ylim=(0,1))
 save(f,6,'Una unidad adicional de x multiplica las odds por e ≈ 2,72 en este modelo.\nEl cambio de probabilidad depende del valor inicial de x: no es constante.')

 f,a=setup('Más pruebas, más oportunidades de error','Modelo: todas las hipótesis nulas son verdaderas; pruebas independientes a α = 0,05.')
 m=np.arange(1,101);risk=1-.95**m;a.plot(m,risk*100,color=ORANGE,lw=3);a.axhline(5,color=BLUE,ls='--',label='5 %')
 for k in [1,10,20,100]:a.scatter([k],[(1-.95**k)*100],color=ORANGE);a.annotate(f'{k}: {(1-.95**k)*100:.1f} %',(k,(1-.95**k)*100),xytext=(7,-17),textcoords='offset points',ha='right' if k==100 else 'left')
 a.set(xlabel='Número de pruebas',ylabel='Probabilidad de ≥1 falso positivo (%)',ylim=(0,110),xlim=(0,105));a.legend()
 save(f,7,'Cálculo: 1 − (1 − α)ᵐ. La fórmula exacta aquí depende de la independencia.\nDefinir la familia de hipótesis forma parte de la planificación del análisis.')

 f,a=setup('Leer magnitud e incertidumbre juntas','Tres resultados hipotéticos con la misma estimación puntual y distinta precisión.')
 for y,halfwidth in [(3,.3),(2,.8),(1,1.6)]:a.errorbar(1,y,xerr=halfwidth,fmt='o',color=TEAL,capsize=6,lw=2)
 a.axvline(0,color=INK,ls='--',label='Diferencia nula');a.set(yticks=[1,2,3],yticklabels=['Resultado C','Resultado B','Resultado A'],xlabel='Diferencia estimada e IC del 95 % (unidades arbitrarias)',ylim=(.5,3.5));a.legend(loc='upper left')
 save(f,8,'Intervalos hipotéticos para practicar lectura; no son resultados de estudios publicados.\nLa relevancia requiere contexto; un intervalo estrecho no descarta sesgos.')
 (OUT/'calculation-record.json').write_text(json.dumps({'seed':20261008,'ci_means':means.tolist(),'ci_half_width':half,'ci_covered':hits,'family_error_20':1-.95**20,'before':before.tolist(),'after':after.tolist()},indent=2)+'\n')

if __name__=='__main__':build()
