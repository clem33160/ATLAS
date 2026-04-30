from __future__ import annotations

import os
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def isolated_runtime(tmp_path, monkeypatch):
    monkeypatch.setenv("ATLAS_MEMORY_RUNTIME_DIR", str(tmp_path / "runtime"))
    yield
