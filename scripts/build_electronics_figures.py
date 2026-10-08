#!/usr/bin/env python3
"""Original circuit models and plots; NumPy/Matplotlib only at authoring time."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/figures/electronica'
TEAL='#087f82'; BLUE='#315f9c'; ORANGE='#a44815'; INK='#12334a'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':13,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','svg.hashsalt':'citonauta-electronics-v1','text.color':INK})

def setup(title,subtitle):
 f,a=plt.subplots(figsize=(12,8));f.patch.set_facecolor('#f3f7fa');f.subplots_adjust(left=.12,right=.95,bottom=.26,top=.76)
 f.text(.06,.93,'CITONAUTA / ELECTRÓNICA',color=TEAL,weight='bold',fontsize=13)
 f.text(.06,.865,title,fontsize=23,weight='bold');f.text(.06,.81,subtitle,fontsize=12)
 return f,a

def save(f,n,note):
 f.text(.06,.095,note,fontsize=12);f.text(.06,.035,'Modelos educativos · Elaboración propia · CC BY-NC 4.0',fontsize=11,color='#486174')
 OUT.mkdir(parents=True,exist_ok=True);f.savefig(OUT/f'unit-{n:02d}.svg',metadata={'Date':None,'Creator':'CitoNauta','Description':note});plt.close(f)

def wire(a,x,y):a.plot(x,y,color=INK,lw=2)
def resistor(a,x,y,label):
 wire(a,[x,x+.15],[y,y]);a.add_patch(Rectangle((x+.15,y-.1),.5,.2,fill=False,lw=2,color=INK));wire(a,[x+.65,x+.8],[y,y]);a.text(x+.4,y+.2,label,ha='center',fontsize=11)

def build():
 f,a=setup('Rectificación de media onda','Modelo ideal sin condensador: el diodo conduce en el semiciclo positivo.')
 t=np.linspace(0,40,1000);vin=2*np.sin(2*np.pi*50*t/1000);vout=np.maximum(vin,0)
 a.plot(t,vin,label='Entrada: 2 V de amplitud, 50 Hz',color=BLUE,lw=2);a.plot(t,vout,label='Salida ideal sobre carga resistiva',color=ORANGE,ls='--',lw=2.5)
 a.set(xlabel='Tiempo (ms)',ylabel='Tensión (V)',ylim=(-2.4,2.6));a.legend(loc='lower left')
 save(f,1,'La salida ideal es max(entrada, 0). Sigue siendo pulsante: rectificar no equivale a filtrar.\nUn diodo real añade caída directa, fugas y límites de corriente y tensión.')

 f,a=setup('Las pérdidas crecen con el cuadrado','Modelo de conducción: P = I² · RDS(on), con resistencia constante.')
 current=np.linspace(0,5,200)
 for r,c in [(.05,TEAL),(.2,ORANGE)]:a.plot(current,current**2*r,label=f'RDS(on) = {r*1000:g} mΩ',color=c,lw=3)
 a.set(xlabel='Corriente de drenador (A)',ylabel='Potencia de conducción (W)');a.legend()
 save(f,2,'Duplicar la corriente cuadruplica estas pérdidas si la resistencia permanece constante.\nModelo parcial: no incluye conmutación ni calentamiento; VGS(th) no garantiza baja RDS(on).')

 f,a=setup('Ganancia y ancho de banda','Aproximación de un polo, pequeña señal: GBW = 1 MHz; ganancias no inversoras 10 y 100.')
 freq=np.logspace(2,7,600)
 for gain,c in [(10,TEAL),(100,ORANGE)]:
  fc=1e6/gain;mag=gain/np.sqrt(1+(freq/fc)**2);a.semilogx(freq,20*np.log10(mag),color=c,lw=2.5,label=f'G = {gain}; fc ≈ {fc/1000:g} kHz');a.scatter([fc],[20*np.log10(gain/np.sqrt(2))],color=c)
 a.set(xlabel='Frecuencia (Hz, escala logarítmica)',ylabel='Ganancia de tensión (dB)');a.legend()
 save(f,3,'En este modelo, fc ≈ GBW/G; en fc la magnitud cae aproximadamente 3 dB respecto a DC.\nNo representa slew rate, saturación, polos adicionales ni todos los operacionales.')

 f,a=setup('Un filtro RC de primer orden','R = 10 kΩ; C = 100 nF; fuente ideal y salida sin carga: fc ≈ 159 Hz.')
 freq=np.logspace(0,5,500);fc=1/(2*np.pi*1e4*1e-7);a.semilogx(freq,-10*np.log10(1+(freq/fc)**2),color=TEAL,lw=3);a.axvline(fc,color=ORANGE,ls='--',label='Frecuencia de corte');a.set(xlabel='Frecuencia (Hz, escala logarítmica)',ylabel='Magnitud (dB)',ylim=(-60,3));a.legend(loc='lower left')
 a.set_position([.12,.26,.83,.33]);circuit=f.add_axes([.25,.61,.5,.15]);circuit.set(xlim=(0,3),ylim=(-.7,1));circuit.axis('off')
 wire(circuit,[0,.3],[.5,.5]);resistor(circuit,.3,.5,'10 kΩ');wire(circuit,[1.1,2.7],[.5,.5]);wire(circuit,[2,2],[.5,.05]);wire(circuit,[1.75,2.25],[.05,.05]);wire(circuit,[1.75,2.25],[-.07,-.07]);wire(circuit,[2,2],[-.07,-.4]);wire(circuit,[1.75,2.25],[-.4,-.4]);circuit.text(2.3,-.1,'100 nF',fontsize=10);circuit.text(0,.76,'Entrada',fontsize=10);circuit.text(2.3,.76,'Salida',fontsize=10);circuit.text(1.8,-.65,'0 V',fontsize=10)
 save(f,4,'H(jω) = 1/(1 + jωRC). Un polo atenúa progresivamente, no elimina toda frecuencia alta.\nLa carga, tolerancias y componentes parásitos pueden modificar esta respuesta ideal.')

 f,a=setup('Los niveles lógicos tienen márgenes','Ejemplo hipotético de una interfaz de 3,3 V; no son límites universales.')
 a.set(xlim=(-.5,2.1),ylim=(0,3.5),xticks=[0,1],xticklabels=['Salida del emisor','Entrada del receptor'],ylabel='Tensión (V)')
 for x,lo,hi in [(0,.4,2.9),(1,.8,2.0)]:
  a.fill_between([x-.25,x+.25],0,lo,color=BLUE,alpha=.2);a.fill_between([x-.25,x+.25],hi,3.3,color=TEAL,alpha=.2)
  for y,label in [(lo,'VOL máx.' if x==0 else 'VIL máx.'),(hi,'VOH mín.' if x==0 else 'VIH mín.')]:a.hlines(y,x-.25,x+.25,color=INK,lw=2);a.text(x+.28,y,f'{label} {y:g} V',va='center',fontsize=11)
 a.annotate('',xy=(.4,.8),xytext=(.4,.4),arrowprops={'arrowstyle':'<->','color':ORANGE});a.annotate('',xy=(.4,2.9),xytext=(.4,2),arrowprops={'arrowstyle':'<->','color':ORANGE});a.text(-.48,1.45,'Margen bajo: 0,4 V\nMargen alto: 0,9 V',fontsize=12)
 save(f,5,'NML = VIL máx. − VOL máx.; NMH = VOH mín. − VIH mín.\nComprobar condiciones de carga y alimentación; la banda de entrada intermedia no garantiza 0 ni 1.')

 f,a=setup('El instrumento también carga el circuito','Modelo DC: fuente de 1 V con resistencia de salida de 10 kΩ y voltímetro resistivo.')
 rm=np.logspace(3,8,500);vm=rm/(10000+rm);a.semilogx(rm,vm,color=TEAL,lw=3)
 for r in [1e4,1e6]:a.scatter([r],[r/(10000+r)],color=ORANGE);a.annotate(f'{r/1000:g} kΩ → {r/(10000+r):.3f} V',(r,r/(10000+r)),xytext=(10,-25),textcoords='offset points')
 a.axhline(1,color=BLUE,ls='--',label='Tensión sin carga');a.set(xlabel='Resistencia de entrada del instrumento (Ω)',ylabel='Tensión medida (V)',ylim=(0,1.1));a.legend(loc='lower right')
 save(f,6,'Vmedida = Vfuente · Rin/(Rfuente + Rin). Una entrada finita modifica la tensión del nodo.\nLa capacitancia de la sonda y su retorno también importan en AC; no se modelan aquí.')
 (OUT/'calculation-record.json').write_text(json.dumps({'rc_ohm':10000,'c_farad':1e-7,'fc_hz':fc,'gbw_hz':1e6,'gains':[10,100],'bandwidth_hz':[100000,10000],'logic_vol':.4,'logic_vil':.8,'logic_voh':2.9,'logic_vih':2.,'loaded_voltage_1meg':1e6/(1e4+1e6)},indent=2)+'\n')
if __name__=='__main__':build()
