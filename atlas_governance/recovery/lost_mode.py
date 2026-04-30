from atlas_governance.core.common import runtime_dir

LOST = runtime_dir() / "recovery/LOST_MODE"

def activate_lost_mode():
    LOST.parent.mkdir(parents=True, exist_ok=True)
    LOST.write_text("lost\n", encoding="utf-8")
    return str(LOST)

def deactivate_lost_mode():
    if LOST.exists(): LOST.unlink()

def is_lost_mode_active() -> bool:
    return LOST.exists()

def safe_to_modify() -> bool:
    return not is_lost_mode_active()
