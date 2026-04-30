from .common import governance_root, runtime_dir, sha256_file, write_json, write_md, now_iso

FILES = {
 "manifest":"config/atlas_manifest_core.json",
 "authority_index":"config/atlas_authority_index.json",
 "domain_registry":"config/atlas_domain_registry.json",
 "constitution":"config/atlas_constitution_core.json",
 "navigation_rules":"config/navigation_rules.json",
 "forbidden_names":"config/forbidden_names.json",
}

def run():
    g = governance_root()
    hashes = {}
    for k, rel in FILES.items():
        p = g / rel
        hashes[k] = sha256_file(p) if p.exists() else None
    data = {"generated_at": now_iso(), "hashes": hashes}
    write_json(runtime_dir()/"identity/identity_fingerprint.json", data)
    write_md(runtime_dir()/"identity/identity_fingerprint.md", "# Identity Fingerprint\n" + "\n".join(f"- {k}: {v}" for k,v in hashes.items()))
    return data
