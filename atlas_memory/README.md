# Atlas Memory Core V1

V1 implémente 20 couches mémoire (brute, sémantique, canonique, causale, procédurale, soi, objectifs, incertitude, contradictions, temporelle, simulation, sociale gouvernée, audit, hiérarchique, active, auto-organisatrice, anti-oubli, anti-bruit, valeur, gouvernée).

## V1 réel
- Stockage append-only JSONL pour événements, concepts, audit, conflits, incertitudes, timeline.
- Promotion canon par domaine (détection d'ambiguïté).
- Extraction sémantique simple pour cas plombier/Lyon/fuite/urgence.
- Intégration optionnelle atlas_rapporteur (ingest fichiers si présents).
- Health report JSON + Markdown avec score non-figé.

## TODO V2
- Enrichir extraction sémantique multi-domaines.
- Règles privacy avancées par type de donnée.
- Indexation/quête vectorielle.

## Commandes
```bash
python -m atlas_memory.src.main init
python -m atlas_memory.src.main ingest --kind conversation --domain rapporteur_affaires --content "client cherche plombier Lyon fuite urgente"
python -m atlas_memory.src.main query --domain rapporteur_affaires
python -m atlas_memory.src.main promote-canon --domain rapporteur_affaires --event-id EVENT_ID --reason "validated memory"
python -m atlas_memory.src.main active-context --task "améliorer rapporteur affaires" --domain rapporteur_affaires
python -m atlas_memory.src.main health
python -m atlas_memory.src.main demo
python -m atlas_memory.src.main ingest-rapporteur
```

## Gouvernance/confidentialité
- Pas de donnée sensible sans consentement explicite.
- Pas de canon sans preuve/validation humaine recommandée.
- Référence atlas_governance détectée par health.
