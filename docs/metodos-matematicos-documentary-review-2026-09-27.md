# Reconstrucción documental de Métodos Matemáticos — 27-09-2026

Se sustituyen las seis unidades de plantilla por contenido matemático desarrollado: 19 ejemplos resueltos, 48 problemas con criterios de comprobación, 52 autoevaluaciones y 34 entradas bibliográficas vinculadas desde el texto. Los números de los ejemplos son sintéticos; no proceden de pacientes ni constituyen parámetros fisiológicos recomendados.

## Alcance y fuentes

| Unidad | Contenido reconstruido | Fuentes y localizadores |
|---|---|---|
| 1 | Rango, eliminación, mínimos cuadrados, condicionamiento, modos y SVD | MIT 18.06SC: Column Space and Nullspace, Projection Matrices and Least Squares, Eigenvalues and Eigenvectors, SVD; LAPACK DGESV, Purpose, y Users’ Guide, Linear Least Squares Problems |
| 2 | Gradiente, divergencia, rotacional, circulación, Gauss, Stokes y balance de transporte | OpenStax Calculus 3, §§4.6, 6.2, 6.5, 6.7 y 6.8 |
| 3 | Series de Fourier, transformada continua, DFT y Laplace | NIST DLMF §§1.8 y 1.14; documentación de FFT de NumPy y SciPy; MIT 18.03SC, Definition of Laplace Transform, pp. 1–3 |
| 4 | Primer orden, compartimentos, segundo orden, frontera y estabilidad de Euler | OpenStax Calculus 2, §§4.1–4.5; NIST DLMF §1.13; SciPy solve_ivp, métodos y tolerancias |
| 5 | Fasores, ramas, residuos, Bessel y Legendre | NIST DLMF §§1.9, 1.10(iii–iv), 10.2, 10.22.37, 18.3 y 18.5 |
| 6 | Escalas, sensibilidad, identificabilidad, covarianza y contraste de modelos | FDA, guía final de noviembre de 2023, §§III, IV y VI.A; MIT, The Physical Basis of Dimensional Analysis; NIST Handbook §§2.5.5 y 4.4.4; SciPy curve_fit, covariance y ejemplo de redundancia |

Las URLs exactas y la relación con las afirmaciones se conservan en `sources` y en los párrafos de cada unidad. Se consultaron directamente los recursos. La referencia de Laplace usa 0− para admitir impulsos; la unidad declara su restricción al caso regular desde 0+. NIST usa una convención simétrica distinta para Fourier; la unidad declara su conversión. La guía FDA se identifica como recomendación para un alcance regulatorio concreto, sin atribuir aprobación a los ejercicios.

## Comprobaciones reproducibles

Los tests `test_metodos_matematicos_unit_01.py` y `test_metodos_matematicos_examples.py` contienen 14 comprobaciones. Incluyen aritmética racional para mínimos cuadrados y perturbaciones; cuadratura independiente de circulación, flujo y residuos; inversión y energía de la DFT; conservación compartimental; convergencia y estabilidad de Euler; proyección de Legendre; no identificabilidad exacta; y efecto de covarianzas en la incertidumbre.

La fuente autoral sigue en `data/course_redevelopment/metodos-matematicos/`. Los espejos, la ficha del curso, los estados y el HTML se regeneran mediante el pipeline existente. El programa, los prerrequisitos, el diagnóstico y el proyecto final se adaptan al contenido reconstruido.

## Estado y límites

La auditoría de marcadores pasa de 19 asignaturas / 113 unidades afectadas a 18 / 107, con 544 coincidencias restantes en el catálogo. La desaparición de esos marcadores no demuestra por sí sola calidad científica. El catálogo conserva 1849 incidencias del contrato de trazabilidad canónica previamente identificadas; este bloque no las oculta ni convierte las citas de las unidades en un registro exhaustivo de afirmaciones.

El curso permanece en `review`: se documentan revisión de fuentes y comprobaciones matemáticas, sin inventar una revisión humana externa. Las pruebas cubren cálculos representativos, no una certificación de todas las afirmaciones o de aplicaciones clínicas. Este cambio es una integración intermedia y no declara terminado CitoNauta.
