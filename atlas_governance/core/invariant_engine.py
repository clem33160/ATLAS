from pathlib import Path
from .common import repo_root, read_json, write_json, write_md, suspicious_name


def run_invariants(root: Path | None = None):
    r = repo_root(root)
    cfg = r / "atlas_governance/config"
    auth = read_json(cfg / "atlas_authority_index.json", {}) or {}
    dom = read_json(cfg / "atlas_domain_registry.json", {}) or {}

    checks = []
    checks.append(("manifest_present", (cfg / "atlas_manifest_core.json").exists()))
    checks.append(("constitution_present", (cfg / "atlas_constitution_core.json").exists()))
    checks.append(("authority_index_present", (cfg / "atlas_authority_index.json").exists()))
    checks.append(("domain_registry_present", (cfg / "atlas_domain_registry.json").exists()))
    checks.append(("path_resolver_present", (r / "atlas_governance/core/path_resolver.py").exists()))
    checks.append(("tests_present", any((r / "atlas_governance/tests").glob("test_*.py"))))

    auth_paths = [v for v in auth.values() if isinstance(v, str)]
    checks.append(("mapped_authorities_resolve", all((r / p).exists() for p in auth_paths)))
    forbidden_canon = [v for v in auth_paths if suspicious_name(v)]
    checks.append(("no_forbidden_canon_suffix", len(forbidden_canon) == 0))
    runtime_canon = [v for v in auth_paths if "/runtime/" in v]
    checks.append(("runtime_not_canonical", len(runtime_canon) == 0))
    checks.append(("domain_registry_non_empty", isinstance(dom, dict) and len(dom) > 0))

    data = {"ok": all(v for _, v in checks), "checks": [{"name": k, "ok": v} for k, v in checks], "forbidden_canon": forbidden_canon, "runtime_canon": runtime_canon}
    out = r / "atlas_governance/runtime/reports"
    write_json(out / "invariants.json", data)
    write_md(out / "invariants.md", "# Invariants\n" + "\n".join(f"- {k}: {'OK' if v else 'FAIL'}" for k, v in checks))
    return data
