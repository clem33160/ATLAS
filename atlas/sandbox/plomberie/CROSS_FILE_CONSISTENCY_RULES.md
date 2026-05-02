# CROSS FILE CONSISTENCY RULES

## Fichiers couverts
1. `SCENARIOS_PLOMBERIE.md`
2. `SCORING_LEADS_PLOMBERIE.md`
3. `LIMITES_CONFORMITE.md`
4. `QUESTIONS_QUALIFICATION.md`
5. `WORKFLOW_CLIENT_PLOMBERIE.md`
6. `atlas/sandbox/plomberie/evaluation_rules.md`
7. `atlas/sandbox/plomberie/regression_cases.md`
8. `atlas/governance/safety/ANTI_REGRESSION_RULES.md`

## Incohérences à détecter
- Scénario urgent sans action humaine explicite.
- Danger gaz/eau/électricité sans priorité sécurité.
- Scoring élevé sans preuves suffisantes.
- Danger critique avec scoring bas non justifié par protocole sécurité.
- Scénario sans questions de qualification.
- Réponse client qui promet prix ou délai certain.
- Scénario qui invente budget/client/numéro/source/preuve.
- Conformité qui interdit une action mais scénario qui la propose.
- Scoring qui oublie conformité ou sécurité.
- Workflow qui saute qualification ou validation humaine.
- Sandbox qui accepte mutation sans preuve.
- Regression cases qui omettent les risques majeurs.
- Questions de qualification absentes pour : urgence, localisation, preuves, assurance, accès logement.
- Scénario business utile mais non mesurable (pas d’impact scoring attendu).
- Candidate qui améliore conversion mais dégrade sécurité.

## Décision sandbox
Toute incohérence critique => mutation refusée.
Toute incohérence moyenne => correction obligatoire avant merge.
