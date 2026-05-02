# SANDBOX NOTIFICATION RULES

## Canaux minimum
1. Mise à jour `atlas/sandbox/evolution/cycle_state.md`.
2. Alerte dans `atlas/reports/`.
3. Entrée append-only dans `atlas/sandbox/evolution/cycle_log.md`.
4. Message terminal explicite.
5. `atlas/sandbox/evolution/ALERT_CURRENT.md` pour arrêt important.
6. Option Termux via `termux-notification` si disponible.

## Fallback
Aucune dépendance externe obligatoire. Si notification externe indisponible,
la notification locale est obligatoire.
