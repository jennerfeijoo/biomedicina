#!/usr/bin/env python3
"""Reproducible synthetic signal figures; NumPy/Matplotlib for authoring only."""
from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from build_electronics_figures import setup as base_setup, TEAL, BLUE, ORANGE, INK
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/figures/senales-biomedicas'
plt.rcParams['svg.hashsalt']='citonauta-signals-v1'

def setup(title,subtitle):
 f,a=base_setup(title,subtitle);f.texts[0].set_text('CITONAUTA / SEÑALES BIOMÉDICAS');return f,a

def save(f,n,note):
 f.text(.06,.095,note,fontsize=12);f.text(.06,.035,'Señales y datos sintéticos · Elaboración propia · CC BY-NC 4.0',fontsize=11,color='#486174')
 OUT.mkdir(parents=True,exist_ok=True);f.savefig(OUT/f'unit-{n:02d}.svg',metadata={'Date':None,'Creator':'CitoNauta','Description':note});plt.close(f)

def build():
 f,a=setup('Dos frecuencias, las mismas muestras','Cosenos de 3 Hz y 7 Hz, muestreados a 10 muestras por segundo.')
 t=np.linspace(0,1,1001);ts=np.arange(11)/10
 a.plot(t,np.cos(2*np.pi*3*t),color=TEAL,lw=2,label='3 Hz');a.plot(t,np.cos(2*np.pi*7*t),color=ORANGE,ls='--',label='7 Hz');a.scatter(ts,np.cos(2*np.pi*3*ts),color=INK,s=45,zorder=3,label='Muestras compartidas')
 a.set_position([.12,.26,.83,.44]);a.set(xlabel='Tiempo (s)',ylabel='Amplitud (u. a.)');a.legend(loc='upper center',ncol=3,bbox_to_anchor=(.5,1.15))
 save(f,1,'En estos instantes, cos(2π·3·t) = cos(2π·7·t): las muestras no distinguen ambas señales.\nEl filtrado antialiasing se aplica antes de digitalizar; un filtro digital no deshace esta ambigüedad.')

 f,a=setup('Suavizar también cambia la forma','Pulso gaussiano sintético y media móvil causal de cinco muestras; fs = 100 Hz.')
 t=np.arange(101)/100;x=np.exp(-.5*((t-.4)/.035)**2);filtered=np.convolve(x,np.ones(5)/5,mode='full')[:len(x)]
 a.plot(t,x,color=BLUE,lw=2,label='Pulso original');a.plot(t,filtered,color=ORANGE,lw=2,label='Media móvil causal');a.set(xlabel='Tiempo (s)',ylabel='Amplitud (u. a.)',xlim=(.2,.7));a.legend()
 save(f,2,'La media usa la muestra actual y las cuatro anteriores: retrasa y reduce el máximo del pulso.\nUna señal más suave no garantiza mejor conservación de eventos o morfología.')

 f,a=setup('Una detección no puede contarse dos veces','Tolerancia de emparejamiento: ±50 ms; cada referencia admite como máximo una detección.')
 refs=[1,2,3];preds=[1.02,2.03,2.04,4]
 a.scatter(refs,[1]*3,s=110,marker='|',color=BLUE,label='Referencias');a.scatter(preds[:2],[0,0],s=65,color=TEAL,label='Emparejadas');a.scatter(preds[2:],[-.14,0],s=65,marker='x',color=ORANGE,label='Sin pareja');a.annotate('Duplicada: 2,04 s',xy=(2.04,-.14),xytext=(2.35,.3),arrowprops={'arrowstyle':'->','color':ORANGE},fontsize=11)
 for r,p in [(1,1.02),(2,2.03)]:a.plot([r,p],[1,0],color=TEAL,lw=2)
 for r in refs:a.axvspan(r-.05,r+.05,color=BLUE,alpha=.12)
 a.set(xlabel='Tiempo (s)',yticks=[0,1],yticklabels=['Detecciones','Referencias'],ylim=(-.4,1.5),xlim=(.7,4.3));a.legend(loc='upper right')
 save(f,3,'Resultado del emparejamiento mostrado: 2 verdaderos positivos, 2 falsos positivos y 1 omisión.\nLa segunda detección próxima a 2 s queda sin emparejar; contarla otra vez inflaría el resultado.')

 f,a=setup('La ventana de observación importa','DFT de 100 muestras a 100 Hz: separación entre bins de 1 Hz; ventana rectangular.')
 n=100;time=np.arange(n)/100;freq=np.fft.rfftfreq(n,1/100)
 spectra=[]
 for hz,c in [(10,TEAL),(10.5,ORANGE)]:
  amp=2*np.abs(np.fft.rfft(np.sin(2*np.pi*hz*time)))/n;amp[[0,-1]]/=2;spectra.append(amp)
  a.plot(freq,amp,'o-',color=c,lw=1.5,markersize=4,label=f'Seno de {hz:g} Hz')
 a.set(xlabel='Frecuencia (Hz)',ylabel='Amplitud unilateral (u. a.)',xlim=(0,25));a.legend()
 save(f,4,'El tono de 10 Hz encaja en un bin; el de 10,5 Hz reparte amplitud entre varios bins: fuga espectral.\nNo es una PSD. Las ventanas modifican la fuga y la resolución; los bins no son frecuencias fisiológicas.')

 f,a=setup('Separar ventanas no siempre separa personas','Ejemplo de generalización a participantes nuevos: cuatro personas, cuatro ventanas por persona.')
 a.remove();left=f.add_axes([.12,.30,.35,.40]);right=f.add_axes([.60,.30,.35,.40]);mixed=np.array([[0,0,1,0],[1,0,0,0],[0,1,0,0],[0,0,0,1]]);grouped=np.array([[0]*4,[0]*4,[0]*4,[1]*4])
 for ax,data,title in [(left,mixed,'Ventanas mezcladas'),(right,grouped,'Participante reservado')]:
  ax.imshow(data,cmap=ListedColormap([TEAL,ORANGE]),vmin=0,vmax=1,aspect='auto');ax.set(xticks=range(4),xticklabels=['1','2','3','4'],yticks=range(4),yticklabels=['A','B','C','D'],xlabel='Ventana',ylabel='Participante',title=title)
  for row in range(4):
   for col in range(4):ax.text(col,row,'Prueba' if data[row,col] else 'Entreno',ha='center',va='center',color='white',fontsize=10)
 save(f,5,'Si una misma persona aparece en entrenamiento y prueba, no se evalúa un participante nuevo.\nLa partición depende del objetivo; un solo participante reservado no basta para una evaluación estable.')

 f,a=setup('Probabilidad predicha y frecuencia observada','Cinco grupos hipotéticos de 100 casos; no son datos clínicos ni una validación de modelo.')
 p=np.array([.1,.3,.5,.7,.9]);observed=np.array([8,22,38,58,76])/100
 a.plot([0,1],[0,1],ls='--',color=BLUE,label='Concordancia ideal');a.plot(p,observed,'o-',color=ORANGE,lw=2,label='Ejemplo hipotético');a.set(xlabel='Probabilidad predicha media del grupo',ylabel='Fracción observada del evento',xlim=(0,1),ylim=(0,1));a.legend()
 save(f,6,'Los puntos bajo la diagonal muestran frecuencias observadas menores que las probabilidades predichas.\nEl agrupamiento y el tamaño muestral influyen; este esquema omite intervalos de incertidumbre.')
 (OUT/'calculation-record.json').write_text(json.dumps({'sampling_hz':10,'sample_times':ts.tolist(),'alias_a':np.cos(2*np.pi*3*ts).tolist(),'alias_b':np.cos(2*np.pi*7*ts).tolist(),'pulse_peak_s':float(t[np.argmax(x)]),'filtered_peak_s':float(t[np.argmax(filtered)]),'references':refs,'detections':preds,'matches':[[0,0],[1,1]],'tolerance_s':.05,'dft_bin_spacing_hz':1.,'dft_10hz_peak_amplitude':float(spectra[0][10]),'train_test_groups':grouped.tolist(),'calibration_counts':[8,22,38,58,76],'calibration_bin_n':100},indent=2)+'\n')
if __name__=='__main__':build()
