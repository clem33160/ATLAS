from core.backup.snapshot import build_snapshot_manifest
from core.backup.restore_check import simulate_restore

def test_backup_restore_contracts():
    m=build_snapshot_manifest('A',['doc1'])
    assert m['checksum'] and simulate_restore(m)['verified']
