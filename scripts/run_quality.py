#!/usr/bin/env python3
"""Run the complete, model-free validation suite locally and in CI."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def commands() -> list[list[str]]:
    checks = [[sys.executable, str(p.relative_to(ROOT))] for p in sorted((ROOT / 'scripts').glob('validate_*.py'))]
    extras = [
        ['audit_course_readiness.py', '--strict'],
        ['audit_curriculum_completeness.py'],
        ['audit_course_portfolio.py', '--strict'],
        ['audit_generic_content.py'],
        ['audit_scientific_traceability.py'],
        ['audit_public_unit_alignment.py', '--strict'],
        ['audit_developed_courses.py', '--strict'],
        ['audit_course_completion.py', '--fail-on-missing-pages'],
        ['audit_course_workload.py', '--subject-id', 'biologia-desarrollo'],
        ['audit_course_bibliography.py', '--subject-id', 'biologia-desarrollo', '--fail-on-exact-duplicates', '--fail-on-incomplete', '--fail-on-ambiguous'],
        ['audit_course_redundancy.py', '--subject-id', 'biologia-desarrollo'],
        ['repair_course_redevelopment_json.py', '--subject-id', 'biologia-desarrollo', '--require-clean'],
        ['consolidate_course_source_registry.py', '--subject-id', 'biologia-desarrollo', '--check'],
        ['promote_unit_sources_to_registry.py', '--subject-id', 'biologia-desarrollo', '--check'],
        ['preflight_bioinstrumentation_atomic_migration.py'],
        ['build_bioinstrumentation_u2_authoral_unit.py', '--check'],
        ['publish_courses.py', '--all', '--check-public'],
        ['sync_catalog_statuses.py', '--check'],
        ['enrich_generated_pages.py', '--check'],
        ['enrich_authored_unit_pages.py', '--check'],
        ['check_generated_preview.py', '--all'],
    ]
    checks.extend([[sys.executable, 'scripts/' + row[0], *row[1:]] for row in extras])
    checks.extend([[sys.executable, '-m', 'unittest', 'discover', '-s', 'tests'], [sys.executable, '-m', 'pytest', '-q']])
    checks.extend([['node', '--check', str(p.relative_to(ROOT))] for p in sorted((ROOT / 'assets/js').glob('*.js'))])
    return checks


def public_snapshot() -> dict[str, str]:
    paths = []
    for folder in ['ciencias-basicas', 'biologicas-medicas', 'ingenieria-biomedica', 'gestion-etica-comunicacion', 'catalogo', 'mapa', 'data']:
        paths.extend(p for p in (ROOT / folder).rglob('*') if p.is_file())
    paths.extend(p for p in ROOT.glob('*') if p.suffix in {'.html', '.xml'} or p.name == 'robots.txt')
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report-dir', type=Path)
    args = parser.parse_args()
    output = args.report_dir or Path(tempfile.mkdtemp(prefix='citonauta-quality-'))
    output.mkdir(parents=True, exist_ok=True)
    results = []
    for index, command in enumerate(commands(), 1):
        name = f'{index:03d}-' + Path(command[1]).stem
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        (output / f'{name}.log').write_text(result.stdout + result.stderr, encoding='utf-8')
        results.append({'command': command, 'exit_code': result.returncode})
        label = 'PASS' if result.returncode == 0 else 'FAIL'
        if 'scripts/audit_scientific_traceability.py' in command and result.returncode == 0:
            findings = json.loads(result.stdout)
            label = f'REPORT ({findings["errors"]} scientific gaps)'
        print(label, ' '.join(command[1:]), flush=True)
        if result.returncode:
            print((result.stdout + result.stderr)[-2500:], flush=True)
    before = public_snapshot()
    for iteration in (1, 2):
        command = [sys.executable, 'scripts/generate_site.py', '--force', '--with-units']
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        (output / f'generation-{iteration}.log').write_text(result.stdout + result.stderr, encoding='utf-8')
        after = public_snapshot()
        changed = sorted(set(before) ^ set(after) | {p for p in before.keys() & after.keys() if before[p] != after[p]})
        results.append({'command': command, 'iteration': iteration, 'exit_code': result.returncode or int(bool(changed)), 'changed_files': changed})
        print('PASS' if not changed and not result.returncode else 'FAIL', f'generation {iteration}: {len(changed)} changed files', flush=True)
        before = after
    (output / 'summary.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    failures = sum(bool(row['exit_code']) for row in results)
    print(f'{len(results)} checks; {failures} failed. Reports: {output}')
    return int(bool(failures))


if __name__ == '__main__':
    raise SystemExit(main())
