# Agente autónomo de CitoNauta

Este agente completa las asignaturas de CitoNauta de forma secuencial, conserva el estado entre ejecuciones y publica un pull request independiente por curso.

## Qué automatiza

Por cada asignatura:

1. Lee el currículo, el overlay existente y cursos semánticamente relacionados.
2. Recupera literatura y recursos mediante OpenAlex y Europe PMC.
3. Genera contenido estructurado con Ollama.
4. Ejecuta una revisión independiente y un bucle de reparación.
5. Guarda el overlay en `data/subjects/<area>/<asignatura>.json`.
6. Regenera únicamente el HTML de esa asignatura.
7. Ejecuta todos los validadores del repositorio.
8. Crea una rama, commit y pull request con GitHub CLI.
9. Espera los checks, fusiona el PR y elimina la rama.
10. Continúa con la siguiente asignatura.

La información de ejecución se guarda en `.citonauta-agent/`, que no se publica.

## Relación con VS Code

VS Code no crea los pull requests por sí mismo. Actúa como panel para lanzar y observar el proceso. El agente ejecuta `git` y `gh` desde la terminal integrada. La extensión **GitHub Pull Requests** permite ver cada PR desde VS Code.

## Requisitos

- Windows 10/11.
- Python 3.11 o posterior.
- Ollama en ejecución.
- Git.
- GitHub CLI (`gh`) autenticado con permiso de escritura en el repositorio.
- Repositorio clonado localmente y sin cambios pendientes.

Modelos predeterminados:

- `qwen3.6:27b`: generación y revisión académica.
- `ornith:9b`: reparación técnica; se puede sustituir por `devstral-small-2:24b` en `agent-config.toml`.
- `qwen3-embedding:0.6b`: recuperación semántica entre asignaturas.

## Instalación desde VS Code

1. Abre la carpeta raíz del repositorio.
2. Abre **Terminal > Run Task**.
3. Ejecuta `CitoNauta: configurar agente`.
4. Si `gh` no está autenticado, ejecuta una vez:

```powershell
gh auth login
```

Para descargar o verificar también los modelos:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/setup_agent.ps1 -PullModels
```

## Primera comprobación

Ejecuta la tarea:

```text
CitoNauta: vista previa de Bioestadística
```

No modifica Git. Guarda el JSON propuesto en:

```text
.citonauta-agent/previews/bioestadistica.json
```

## Ejecución autónoma

Una asignatura:

```powershell
.venv\Scripts\python.exe scripts\run_citonauta_agent.py run --subject bioestadistica
```

La siguiente asignatura pendiente:

```powershell
.venv\Scripts\python.exe scripts\run_citonauta_agent.py run --limit 1
```

Toda la cola:

```powershell
.venv\Scripts\python.exe scripts\run_citonauta_agent.py run
```

Solo un área:

```powershell
.venv\Scripts\python.exe scripts\run_citonauta_agent.py run --area biologicas-medicas
```

Reintentar fallos:

```powershell
.venv\Scripts\python.exe scripts\run_citonauta_agent.py run --retry-failed
```

## Controles automáticos

El agente se detiene para una asignatura si:

- el repositorio contiene cambios ajenos;
- falta un modelo obligatorio;
- el curso no supera el mínimo de profundidad;
- la revisión independiente obtiene menos de 8/10;
- aparecen referencias no incluidas en el conjunto permitido;
- fallan el currículo, la generación, la vista previa o los enlaces;
- GitHub Actions rechaza el pull request.

El fallo queda registrado y la cola continúa con la siguiente asignatura.

## Configuración

`agent-config.toml` controla modelos, contexto, profundidad, reintentos y publicación. Para impedir temporalmente la fusión automática:

```toml
[git]
auto_merge = false
```

Para utilizar Devstral como reparador técnico:

```toml
[models]
technical = "devstral-small-2:24b"
```

## Publicación

El flujo predeterminado es:

```text
rama -> commit -> push -> PR -> checks -> squash merge -> GitHub Pages
```

Cada asignatura queda aislada en su propio PR, por lo que puede auditarse o revertirse posteriormente sin deshacer el resto del sitio.
