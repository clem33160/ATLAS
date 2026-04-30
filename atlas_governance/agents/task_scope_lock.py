def validate_scope(intent, changed_files):
    task=intent.get('task_type','scoring')
    bad=[]
    if task=='scoring': bad=[f for f in changed_files if 'search' in f]
    if task=='scraping': bad=[f for f in changed_files if 'governance' in f]
    if task=='report': bad=[f for f in changed_files if 'extraction' in f]
    return {"ok":len(bad)==0,"violations":bad}
def explain_scope_violation(): return "Task scope violation detected"
