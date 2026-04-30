from atlas_governance.core.domain_registry import get_domain
def route_intent(intent):
    d=get_domain(intent.get('domain','navigation')) or {}
    allowed=d.get('allowed_directories',[])
    req=intent.get('files_requested',[])
    allowed_files=[f for f in req if any(a in f for a in allowed)]
    forbidden_files=[f for f in req if f not in allowed_files]
    decision='ALLOW' if not forbidden_files else 'HUMAN_REVIEW'
    return {"allowed_files":allowed_files,"forbidden_files":forbidden_files,"required_tests":["atlas_test.sh"],"risks":["scope drift"] if forbidden_files else [],"decision":decision}
