"""Distinguish historical preparation records from the current public migration."""
from __future__ import annotations

import json
from pathlib import Path


def public_review_migration(root: Path) -> bool:
    """Accept developed material only with the recorded, non-certified migration.

    Historical preparation/authorization files remain unchanged. Their earlier
    absence-of-files conditions no longer describe the current repository.
    """
    path = root / 'data/course_migrations/bioinstrumentacion-public-canonical-v1.json'
    if not path.exists():
        return False
    migration = json.loads(path.read_text(encoding='utf-8'))
    state = migration.get('publication_state', {})
    if migration.get('status') != 'implemented_public_layer':
        return False
    if state.get('educational_publication') != 'review':
        return False
    for key in ('human_review_executed', 'disciplinary_review_complete',
                'professional_approval_claimed', 'clinical_validity_claimed',
                'safety_conformity_claimed', 'emc_conformity_claimed',
                'regulatory_conformity_claimed', 'accreditation_claimed'):
        if state.get(key) is not False:
            return False
    statuses = json.loads((root / 'data/catalog_statuses.json').read_text(encoding='utf-8'))
    if 'bioinstrumentacion' not in statuses.get('developed', []):
        return False
    if 'bioinstrumentacion' in statuses.get('complete', []) or 'bioinstrumentacion' in statuses.get('pending', []):
        return False
    directory = root / 'data/generated_units/bioinstrumentacion'
    units = sorted(directory.glob('unit-*.json'))
    if len(units) != 10:
        return False
    return all(json.loads(p.read_text(encoding='utf-8')).get('status') == 'review' for p in units)
