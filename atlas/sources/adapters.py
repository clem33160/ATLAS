from datetime import datetime, timezone
from pathlib import Path


def collect_manual_urls(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding='utf-8').splitlines():
        url = line.strip()
        if not url or url.startswith('#'):
            continue
        out.append({
            'url': url,
            'date_collecte': datetime.now(timezone.utc).isoformat(),
            'source_id': 'manual_url',
            'texte': f'Collecte simulée pour {url}',
            'status': 'À_VALIDER',
            'note_conformite': 'Collecte semi-automatique contrôlée, validation humaine requise.'
        })
    return out
