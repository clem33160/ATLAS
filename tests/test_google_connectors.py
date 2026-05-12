from pathlib import Path
from core.connectors.gmail import search_attachments, import_pdf_attachments
from core.connectors.google_oauth import OAuthToken, refresh_access_token

def test_oauth_refresh_mock():
    t = OAuthToken('a','r','x')
    n = refresh_access_token(t, lambda rt: {'access_token':'new','expires_in':3600})
    assert n.access_token == 'new'

def test_gmail_import(tmp_path: Path):
    msgs=[{'id':'m1','from':'x','subject':'s','date':'2026-01-01','attachments':[{'id':'a1','filename':'f.pdf'}]}]
    m = search_attachments(msgs)
    rows = import_pdf_attachments(m, tmp_path, lambda mid,aid: b'pdf')
    assert rows[0]['sha256']
