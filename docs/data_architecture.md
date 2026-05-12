# Atlas Business MVP Data Architecture

All private/large data must live outside git under `~/atlas_data`.

## Config-driven paths
Atlas reads `atlas.config.yaml` (copy from `atlas.config.example.yaml`) for:
- wikidata dump
- sirene source
- document root
- index root
- google token
- gmail import
- proof1000 sandbox

## Source registry contract
Each source contains:
`source_id`, `source_type`, `local_path`, `enabled`, `sensitivity`, `allowed_roles`, `provenance_rules`, `test_status`.
