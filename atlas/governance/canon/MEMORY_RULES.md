# MEMORY RULES

- Les décisions sensibles sont journalisées en append-only.
- Chaque décision inclut date, auteur, contexte, justification.
- Toute mutation majeure compare ancienne/nouvelle version.
- Un rollback doit rester possible via historique.
- Les contradictions doivent être auditées et tracées.
- Toute information est classée : vérité / hypothèse / estimation / imagination / stratégie.
