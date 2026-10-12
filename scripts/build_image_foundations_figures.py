#!/usr/bin/env python3
"""Original synthetic figures for image foundations; authoring requires NumPy/Matplotlib."""
from pathlib import Path
from xml.sax.saxutils import escape
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/figures/tratamiento-digital-imagenes'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'svg.fonttype':'none','svg.hashsalt':'citonauta-image-foundations-v1','axes.spines.top':False,'axes.spines.right':False})
TEAL='#087f82'; ORANGE='#a44815'; BLUE='#315f9c'
def frame(title,subtitle,panels=1):
 f,axes=plt.subplots(1,panels,figsize=(12,8),squeeze=False)
 f.patch.set_facecolor('#f3f7fa');f.subplots_adjust(left=.09,right=.95,bottom=.27,top=.73,wspace=.30)
 f.text(.06,.94,'CITONAUTA / TRATAMIENTO DIGITAL DE IMÁGENES',color=TEAL,weight='bold',fontsize=12)
 f.text(.06,.865,title,fontsize=23,weight='bold');f.text(.06,.80,subtitle,fontsize=12)
 return f,axes[0]
def save(f,name,title,desc,note):
 OUT.mkdir(parents=True,exist_ok=True)
 f.text(.06,.13,note,fontsize=12);f.text(.06,.035,'Datos sintéticos · Elaboración propia · CC BY-NC 4.0',fontsize=11,color='#486174')
 p=OUT/(name+'.svg');f.savefig(p,metadata={'Date':None,'Creator':'CitoNauta'});plt.close(f)
 s=p.read_text();i=s.index('>',s.index('<svg'))+1
 content=s[:i]+'\n<title>'+escape(title)+'</title>\n<desc>'+escape(desc)+'</desc>'+s[i:]
 p.write_text('\n'.join(line.rstrip() for line in content.splitlines())+'\n')
def build():
 f,axes=frame('Dos patrones, las mismas muestras','Cosenos de 3 y 7 ciclos/mm; centros separados 0,1 mm.')
 a=axes[0];x=np.linspace(0,1,1001);n=np.arange(11)/10
 a.plot(x,np.cos(2*np.pi*3*x),color=TEAL,lw=2,label='3 ciclos/mm')
 a.plot(x,np.cos(2*np.pi*7*x),color=ORANGE,ls='--',lw=2,label='7 ciclos/mm')
 a.scatter(n,np.cos(2*np.pi*3*n),color='#17283b',s=38,zorder=5,label='Muestras de ambos')
 a.set(xlabel='Posición (mm)',ylabel='Amplitud (u. a.)',ylim=(-1.2,1.5));a.legend(ncol=3,fontsize=10,loc='upper right');a.grid(alpha=.15)
 save(f,'unit-01-aliasing','Aliasing espacial','Dos cosenos distintos coinciden en todas las muestras separadas 0,1 mm.','Muestreo: 10 muestras/mm; Nyquist: 5 ciclos/mm.\nEl patrón de 7 ciclos/mm no puede distinguirse del de 3 con estas muestras.')
 f,axes=frame('Un histograma no conserva la forma','Dos matrices 8 × 8: 32 ceros y 32 unos en cada una.',3)
 a=np.zeros((8,8));a[4:]=1;b=np.indices((8,8)).sum(axis=0)%2
 for ax,arr,title in zip(axes[:2],[a,b],['Mitades','Tablero']):
  ax.imshow(arr,cmap='gray',vmin=0,vmax=1,interpolation='nearest');ax.set_title(title);ax.set_xlabel('Columna');ax.set_ylabel('Fila');ax.set_xticks([0,3,7]);ax.set_yticks([0,3,7])
 axes[2].bar([0,1],[32,32],color=[TEAL,ORANGE]);axes[2].set(xticks=[0,1],xlabel='Nivel',ylabel='Número de píxeles',ylim=(0,40),title='Histograma compartido')
 save(f,'unit-01-histogram','Histograma y estructura espacial','Mitades y tablero tienen igual histograma pero distinta organización.','Iguales cuentas y media (0,5); diferentes vecindarios y bordes.\nPara analizar estructura se necesita información espacial además del histograma.')
 f,axes=frame('La convención gamma cambia el resultado','En esta figura: salida = entrada elevada a gamma; entradas entre 0 y 1.')
 a=axes[0];x=np.linspace(0,1,501)
 for g,c,ls in [(.5,TEAL,'-'),(1,BLUE,':'),(2,ORANGE,'--')]:a.plot(x,x**g,label=f'γ = {g:g}',color=c,lw=3,ls=ls)
 a.scatter([.25,.25],[.5,.0625],color='#17283b',zorder=5)
 a.set(xlabel='Intensidad de entrada (normalizada)',ylabel='Intensidad de salida (normalizada)',xlim=(0,1),ylim=(0,1));a.legend();a.grid(alpha=.15)
 save(f,'unit-02-gamma','Curvas gamma','Gamma 0,5 eleva 0,25 a 0,5; gamma 2 reduce 0,25 a 0,0625.','Los extremos se conservan; las distancias interiores cambian.\nMejor visibilidad no equivale a información adquirida adicional.')
 f,axes=frame('Una ventana estrecha también pierde diferencias','Modelo continuo didáctico: clip((x − l) / (h − l), 0, 1).')
 a=axes[0];x=np.linspace(-25,125,601)
 for lo,hi,c,ls in [(0,100,TEAL,'-'),(25,75,ORANGE,'--')]:a.plot(x,np.clip((x-lo)/(hi-lo),0,1),color=c,lw=3,ls=ls,label=f'Ventana [{lo}, {hi}]')
 a.set(xlabel='Intensidad de entrada (u. a.)',ylabel='Valor de pantalla (0–1)',ylim=(-.05,1.08));a.legend();a.grid(alpha=.15)
 save(f,'unit-02-window','Ventanas y saturación','La ventana 25–75 tiene doble pendiente interior y mesetas más extensas que la ventana 0–100.','Las mesetas reúnen valores diferentes. Conservar siempre el original para medir.\nEsta función no sustituye la definición de DICOM LINEAR por defecto.')
if __name__=='__main__':build()
