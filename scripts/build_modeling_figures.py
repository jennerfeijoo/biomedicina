#!/usr/bin/env python3
"""Original analytical teaching figures; NumPy/Matplotlib only for authoring."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from xml.sax.saxutils import escape
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/figures/modelado-simulacion-biomedicina'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':13,'svg.fonttype':'none','svg.hashsalt':'citonauta-modeling-v1','axes.spines.top':False,'axes.spines.right':False})
TEAL='#087f82'; ORANGE='#a44815'; BLUE='#315f9c'

def setup(title,subtitle):
 f,a=plt.subplots(figsize=(12,8));f.patch.set_facecolor('#f3f7fa');f.subplots_adjust(left=.12,right=.94,bottom=.27,top=.75)
 f.text(.06,.94,'CITONAUTA / MODELADO Y SIMULACIÓN',color=TEAL,weight='bold',fontsize=13)
 f.text(.06,.875,title,fontsize=23,weight='bold');f.text(.06,.815,subtitle,fontsize=12)
 return f,a

def save(f,n,title,desc,note):
 OUT.mkdir(parents=True,exist_ok=True)
 f.text(.06,.11,note,fontsize=12);f.text(.06,.035,'Ejemplos sintéticos · Elaboración propia · CC BY-NC 4.0',fontsize=11,color='#486174')
 p=OUT/f'unit-{n:02}.svg';f.savefig(p,metadata={'Date':None,'Creator':'CitoNauta'});plt.close(f)
 s=p.read_text();start=s.index('>',s.index('<svg'))+1
 s=s[:start]+'\n<title>'+escape(title)+'</title>\n<desc>'+escape(desc)+'</desc>'+s[start:];p.write_text(s)


def build():
 f,a=setup('Dilución no es eliminación','Cantidad constante A = 12 mg; solo cambia el volumen V.')
 v=np.linspace(3,6,150);a.plot(v,12/v,color=TEAL,lw=3,label='C = 12 / V');a.scatter([3,6],[4,2],color=ORANGE,zorder=4)
 a.annotate('3 L → 4 mg/L',(3,4),xytext=(15,-15),textcoords='offset points',bbox={'facecolor':'white','edgecolor':'none','alpha':.9});a.annotate('6 L → 2 mg/L',(6,2),xytext=(-155,20),textcoords='offset points',bbox={'facecolor':'white','edgecolor':'none','alpha':.9})
 a.set(xlabel='Volumen (L)',ylabel='Concentración (mg/L)',xlim=(2.8,6.2),ylim=(1.6,4.4));a.legend()
 save(f,1,'Dilución no es eliminación','Al duplicar el volumen de 3 a 6 litros, 12 mg constantes pasan de 4 a 2 mg/L.','La concentración cae a la mitad mientras la cantidad permanece en 12 mg.\nPara inferir eliminación se necesitan también volumen y balance de cantidad.')

 f,a=setup('Euler puede ser estable y dar negativos','A′ = −A; A(0) = 10 mg. Tiempo en horas; k = 1 h⁻¹.')
 t=np.linspace(0,6,300);a.plot(t,10*np.exp(-t),color=TEAL,lw=3,label='Solución exacta')
 for h,c in [(.5,BLUE),(1.5,ORANGE)]:
  ts=np.arange(0,6.01,h);a.plot(ts,10*(1-h)**np.arange(len(ts)),marker='o',ls='--',color=c,label=f'Euler: h = {h:g} h')
 a.axhline(0,color='#777',lw=1);a.set(xlabel='Tiempo (h)',ylabel='Cantidad (mg)');a.legend(loc='upper right')
 save(f,2,'Estabilidad y positividad','Euler con paso 1,5 h alterna cantidades negativas aunque decrece en magnitud; con 0,5 h preserva positividad.','Estabilidad asintótica: 0 < kh < 2. Positividad en este modelo: kh ≤ 1.\nLos valores negativos son un fallo de la aproximación para representar cantidades.')

 f,a=setup('Una tasa no es una probabilidad','Espera exponencial con tasa constante: p = 1 − exp(−λΔt).')
 x=np.linspace(0,2,250);a.plot(x,1-np.exp(-x),color=TEAL,lw=3,label='Probabilidad exacta');a.plot(x,x,color=ORANGE,ls='--',lw=2,label='Aproximación λΔt');a.axhline(1,color='#777',ls=':');a.scatter([1],[1-np.exp(-1)],color=BLUE)
 a.set(xlabel='Producto λΔt (sin unidades)',ylabel='Valor calculado',ylim=(0,2.1));a.legend(loc='upper left')
 save(f,3,'Tasa y probabilidad','La aproximación lineal excede uno cuando el producto tasa por tiempo supera uno; la probabilidad exponencial permanece menor que uno.','Para λΔt = 1: p ≈ 0,632, no 1. La aproximación lineal exige λΔt pequeño.\nLa curva supone riesgo constante durante la espera.')

 f,a=setup('Dos parámetros, una curva indistinguible','Observable normalizado z(t) = exp[−(CL/V)t]. No se conoce V por otra vía.')
 t=np.linspace(0,15,250);a.plot(t,np.exp(-2/10*t),color=TEAL,lw=4,label='CL = 2 L/h; V = 10 L');a.plot(t,np.exp(-4/20*t),color=ORANGE,ls='--',lw=2,label='CL = 4 L/h; V = 20 L')
 a.set(xlabel='Tiempo (h)',ylabel='Cantidad normalizada A/A₀');a.legend()
 save(f,4,'No identificabilidad de una razón','Las curvas para CL/V igual a 2/10 y 4/20 coinciden en todos los tiempos.','La curva identifica k = CL/V = 0,2 h⁻¹, pero no separa CL de V.\nUna observación independiente de volumen aportaría la escala que falta.')

 f,a=setup('Refinamiento frente a una solución exacta','Euler para A′ = −A, A(0) = 1; salida A(1 h) = exp(−1).')
 h=1/2**np.arange(1,9);error=np.abs((1-h)**(1/h)-np.exp(-1));a.loglog(h,error,'o-',color=TEAL,lw=2,label='Error absoluto de Euler');a.loglog(h,error[-1]*h/h[-1],ls='--',color=ORANGE,label='Referencia proporcional a h')
 a.set(xlabel='Paso h (h, escala logarítmica)',ylabel='Error de A(1 h) (escala logarítmica)');a.legend()
 save(f,5,'Convergencia de primer orden','El error de Euler disminuye aproximadamente en proporción al paso al refinar hacia pasos pequeños.','Cada punto mantiene el mismo problema y tiempo final; cambia solo el paso.\nAcercarse a la solución de una ecuación no valida esa ecuación en un organismo.')

 f,a=setup('Una decisión cambia al cruzar un umbral','Pérdidas sintéticas: A = (2, 10); B = (5, 4), para estados bajo y alto.')
 p=np.linspace(0,1,250);a.plot(p,2+8*p,color=TEAL,lw=3,label='A: 2 + 8p');a.plot(p,5-p,color=ORANGE,lw=3,ls='--',label='B: 5 − p');a.axvline(1/3,color=BLUE,ls=':');a.scatter([1/3],[14/3],color=BLUE);a.annotate('Indiferencia: p = 1/3',(1/3,14/3),xytext=(20,35),textcoords='offset points',bbox={'facecolor':'white','edgecolor':'none','alpha':.9})
 a.set(xlabel='Probabilidad del estado alto, p',ylabel='Pérdida esperada (unidades del ejercicio)');a.legend(loc='upper left')
 save(f,6,'Umbral de preferencia','A tiene menor pérdida esperada por debajo de un tercio; B por encima. El umbral depende de la tabla sintética.','A se prefiere para p < 1/3; B para p > 1/3, bajo estas pérdidas.\nEs un ejercicio de decisión: no representa un umbral clínico.')

if __name__=='__main__': build()
