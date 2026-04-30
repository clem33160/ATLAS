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

## Lois anti-bruit Atlas Memory

1. Aucun test ne doit écrire dans le runtime réel.
2. Toute donnée demo/test/mock/fixture doit être marquée comme non réelle.
3. Tout conflit placeholder doit être isolé.
4. Toute incertitude sans source réelle doit être isolée.
5. Aucun placeholder ne peut entrer dans le canon.
6. Aucun score mémoire ne doit être gonflé par maquillage.
7. Le bruit peut exister, mais jamais gouverner.
8. Les données utilisateur réelles ne doivent jamais être supprimées sans validation humaine.
9. Les nettoyages doivent produire un rapport.
10. La mémoire active ne charge jamais le bruit.
11. Le canon ne contient que des éléments validés ou explicitement promus.
12. Les tests doivent vérifier l’absence de pollution.
