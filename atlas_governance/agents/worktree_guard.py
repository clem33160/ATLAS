import subprocess
def worktree_status():
    try: out=subprocess.check_output(['git','status','--porcelain'],text=True).splitlines()
    except Exception: out=[]
    return {"dirty_files_count":len(out),"entries":out}
