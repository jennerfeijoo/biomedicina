# Notación matemática en las unidades

Las expresiones matemáticas de las lecciones se renderizan con MathJax 3 y sintaxis LaTeX.

## Reglas editoriales

1. Usar `\(...\)` para expresiones breves integradas en una oración.
2. Usar el campo estructurado `equations` para ecuaciones, sistemas, matrices, derivaciones o expresiones que deban aparecer en bloque.
3. No escribir matrices como listas anidadas (`[[1, 0], [0, 1]]`) cuando forman parte de una explicación matemática.
4. No representar exponentes mediante `^` sin renderizado, divisiones largas con `/` ni sistemas como una sola línea de texto.
5. Toda ecuación debe acompañarse de interpretación, unidades cuando corresponda y supuestos.
6. Evitar convertir párrafos completos en LaTeX. La prosa permanece como texto semántico y accesible.
7. El código fuente se mantiene dentro de bloques `code`; MathJax no procesa `pre` ni `code`.

## Estructura JSON recomendada

```json
{
  "equations": [
    {
      "label": "Sistema equivalente",
      "latex": "\\begin{cases}x_1+0.1x_2=11,\\\\0.2x_1+x_2=12.\\end{cases}"
    },
    {
      "label": "Matriz inversa",
      "latex": "A^{-1}=\\frac{1}{0.98}\\begin{bmatrix}1&-0.1\\\\-0.2&1\\end{bmatrix}"
    }
  ]
}
```

El campo `equations` puede incorporarse en la unidad, una sección teórica, un ejemplo o una actividad.

## Patrones frecuentes

- Fracción: `\\frac{a}{b}`
- Exponente: `x^{2}`
- Subíndice: `x_{1}`
- Vector: `\\mathbf{x}`
- Matriz: `\\begin{bmatrix}a&b\\\\c&d\\end{bmatrix}`
- Sistema: `\\begin{cases}...\\\\...\\end{cases}`
- Integral: `\\int_a^b f(x)\\,dx`
- Derivada: `\\frac{dy}{dx}`
- Sumatoria: `\\sum_{i=1}^{n} x_i`
- Aproximación: `\\approx`
- Unidades: `\\mathrm{mg\\,mL^{-1}}`

## Criterio de calidad

La notación debe facilitar el razonamiento. Una fórmula aislada sin definición de variables, pasos, interpretación o limitaciones no se considera contenido desarrollado.