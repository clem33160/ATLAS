POLICIES = {
    "owner": {"*"},
    "secretary": {"admin", "invoice", "quote", "job", "contract"},
    "apprentice": {"job", "intervention"},
    "external_client": {"client_doc"},
    "accountant": {"invoice", "tax", "payroll", "payment"},
    "auditor": {"audit", "proof"},
}
