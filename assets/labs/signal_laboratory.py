"""Laboratorio sintético de señales: ejecutar con Python 3.10+ sin dependencias.

python assets/labs/signal_laboratory.py

Los resultados verifican cálculos educativos; no son un detector clínico.
La referencia de emparejamiento utiliza programación dinámica para secuencias
ordenadas: maximiza parejas y, en segundo lugar, minimiza error absoluto.
Su coste cuadrático la limita a ejemplos pequeños.
"""
from math import cos, isfinite, log10, pi, sqrt
import json


def rms(values):
    values = tuple(values)
    if not values or not all(isfinite(x) for x in values):
        raise ValueError('RMS requiere valores finitos y no vacíos')
    return sqrt(sum(x*x for x in values) / len(values))


def coverage(size, *excluded_sets):
    if not isinstance(size, int) or size <= 0:
        raise ValueError('El número elegible debe ser un entero positivo')
    excluded = set().union(*excluded_sets)
    if any(not isinstance(i, int) or not 0 <= i < size for i in excluded):
        raise ValueError('Índice excluido fuera del registro')
    return (size - len(excluded)) / size


def match_events(reference, predicted, tolerance):
    """Devuelve pares de índices, TP/FP/FN y métricas; tolerancia inclusiva.

    Los tiempos deben ser finitos y no decrecientes, en una unidad común.
    Los duplicados se mantienen como eventos distintos para revelar FP/FN.
    Ante empates de cardinalidad y coste se prefiere emparejar los últimos
    elementos, después omitir una predicción y después una referencia.
    """
    ref, pred = tuple(reference), tuple(predicted)
    if not isfinite(tolerance) or tolerance < 0:
        raise ValueError('Tolerancia finita no negativa requerida')
    for seq in (ref, pred):
        if not all(isfinite(x) for x in seq) or any(a > b for a, b in zip(seq, seq[1:])):
            raise ValueError('Los eventos deben ser finitos y estar ordenados')
    n, m = len(ref), len(pred)
    score = [[(0, 0.0) for _ in range(m+1)] for _ in range(n+1)]
    direction = [['' for _ in range(m+1)] for _ in range(n+1)]
    for i in range(1, n+1):
        for j in range(1, m+1):
            options = [(score[i-1][j], 0, 'reference'),
                       (score[i][j-1], 1, 'prediction')]
            error = abs(ref[i-1] - pred[j-1])
            if error <= tolerance:
                count, neg_cost = score[i-1][j-1]
                options.append(((count+1, neg_cost-error), 2, 'pair'))
            best = max(options)
            score[i][j], _, direction[i][j] = best
    pairs = []
    i, j = n, m
    while i and j:
        step = direction[i][j]
        if step == 'pair':
            pairs.append((i-1, j-1)); i -= 1; j -= 1
        elif step == 'prediction':
            j -= 1
        else:
            i -= 1
    pairs.reverse()
    tp = len(pairs)
    return dict(pairs=pairs, TP=tp, FN=n-tp, FP=m-tp,
                sensitivity=tp/n if n else None,
                positive_predictive_value=tp/m if m else None,
                signed_errors=[pred[b]-ref[a] for a, b in pairs])


def moving_average_three(values):
    """Media causal de tres muestras con extensión cero a la izquierda."""
    values = tuple(values)
    if not all(isfinite(x) for x in values):
        raise ValueError('No se filtran ausencias sin una política explícita')
    return [sum(values[max(0, i-2):i+1])/3 for i in range(len(values))]


def demonstration():
    fs = 250
    alias_error = max(abs(cos(2*pi*180*n/fs)-cos(2*pi*70*n/fs)) for n in range(fs))
    return {
        'scope': 'Datos sintéticos; sin adquisición humana ni validación clínica',
        'u1': {'calibrated_mV': [(d-1000)/200 for d in [1000, 1200, 800]],
               'last_time_s': 999/fs, 'alias_max_abs_error': alias_error},
        'u2': {'coverage': coverage(1000, range(100), range(80, 130)),
               'snr_dB': 10*log10(4/1)},
        'u3': {'zero_padded_constant': moving_average_three([3, 3, 3]),
               'remapped_index': (720/360)*250},
        'u4': match_events([100, 200, 300], [98, 102, 205, 450], 5),
        'u5': {'rms_mV': rms([1, 3]), 'flat_band_power_mV2': 2*(15-5)},
        'u6': {'rms_uV': rms([1000, 3000]),
               'power_scale': rms([1000, 3000])**2/rms([1, 3])**2},
    }


if __name__ == '__main__':
    print(json.dumps(demonstration(), ensure_ascii=False, indent=2))
