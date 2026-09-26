# Contribuir a CitoNauta

## Flujo

1. Abra una rama específica.
2. Delimite asignatura, unidad, resultados y riesgos afectados.
3. Registre fuentes y localizadores de las afirmaciones importantes.
4. Añada o actualice pruebas y validadores.
5. Ejecute los controles locales.
6. Abra una pull request y declare limitaciones y estado de revisión.

## Requisitos científicos

- No presentar disponibilidad de archivos como validación.
- Distinguir observación, asociación, predicción, causalidad y utilidad.
- No inventar referencias, DOI, resultados, datos ni revisiones.
- Usar el vocabulario oficial de verificación de fuentes.
- Añadir `claim_id` y localizador para afirmaciones de riesgo medio o alto.
- Mantener `ai_review_provisional` si no existe un manifiesto `validated_for_scope` coincidente.
- No cambiar registros históricos de revisión para simular evidencia nueva.

## Controles mínimos

```bash
python -m pip install -r requirements-dev.txt
python scripts/run_quality.py
python scripts/audit_scientific_traceability.py --strict
```

La auditoría científica estricta informa brechas pendientes en los registros migrados; no debe interpretarse un CI técnico verde como aprobación científica. La revisión documental no requiere un proveedor de modelos.

La pull request debe explicar qué cambió, por qué, qué evidencia lo respalda, qué pruebas se ejecutaron y qué permanece provisional.
