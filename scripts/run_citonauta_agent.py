#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from citonauta_agent.config import load_config  # noqa: E402
from citonauta_agent.orchestrator import CitonautaAgent  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Completa, valida, publica y fusiona asignaturas de CitoNauta con Ollama."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=ROOT / "agent-config.toml",
        help="Ruta al archivo TOML de configuración.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    run = subparsers.add_parser("run", help="Procesa una o varias asignaturas.")
    run.add_argument("--subject", action="append", default=[], help="ID de asignatura; repetible.")
    run.add_argument("--area", help="Procesa únicamente un área.")
    run.add_argument("--limit", type=int, help="Número máximo de asignaturas en esta ejecución.")
    run.add_argument("--dry-run", action="store_true", help="Genera una vista previa sin modificar Git.")
    run.add_argument("--no-publish", action="store_true", help="Escribe y valida localmente, sin commit ni PR.")
    run.add_argument("--retry-failed", action="store_true", help="Reintenta asignaturas fallidas.")

    subparsers.add_parser("preflight", help="Comprueba Ollama, Git, GitHub CLI y el repositorio.")
    subparsers.add_parser("status", help="Muestra el estado persistente de la cola.")
    subparsers.add_parser("reset-failed", help="Devuelve las asignaturas fallidas a pending.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    config = load_config(ROOT, args.config)
    agent = CitonautaAgent(config)

    if args.command == "preflight":
        agent.preflight(publish=True)
        print("Preflight completado: Ollama, Git, gh y repositorio disponibles.")
        return 0
    if args.command == "status":
        agent.state.register(agent.catalog.all_subjects())
        print(json.dumps(agent.state.summary(), ensure_ascii=False, indent=2))
        return 0
    if args.command == "reset-failed":
        print(f"Asignaturas reiniciadas: {agent.state.reset_failed()}")
        return 0
    if args.command == "run":
        agent.run(
            subject_ids=args.subject or None,
            area_id=args.area,
            limit=args.limit,
            dry_run=args.dry_run,
            publish=not args.no_publish,
            retry_failed=args.retry_failed,
        )
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
