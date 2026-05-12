import secrets

def build_oauth_state(tenant_id:str):
    return {"tenant_id":tenant_id,"nonce":secrets.token_hex(8)}
