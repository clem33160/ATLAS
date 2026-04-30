from atlas_memory.src.common import RUNTIME_PATHS, ensure_runtime_structure


def test_runtime_not_real_path():
    ensure_runtime_structure()
    assert "atlas_memory/runtime" not in str(RUNTIME_PATHS["raw"])


def test_tests_do_not_pollute_real_runtime():
    ensure_runtime_structure()
    assert "atlas_memory/runtime" not in str(RUNTIME_PATHS["raw"])
