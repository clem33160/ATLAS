from core.dialog.choices import numbered_choices

def test_choices_format():
    out=numbered_choices([{'label':'fuite évier','amount':267,'location':'Paris','date':'2026-01-01','doc_id':'DOC_x'}])
    assert '1. fuite évier' in out
