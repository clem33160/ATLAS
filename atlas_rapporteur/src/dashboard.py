import json
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
from .config import BASE

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        p=BASE/'runtime/exports/leads_ranked.json'
        leads=json.loads(p.read_text(encoding='utf-8')) if p.exists() else []
        top=leads[:20]
        html='<h1>Atlas Dashboard</h1><p>Leads: %d</p>'%len(leads)
        html+='<p><a href="/export/json">Export JSON</a> | <a href="/export/csv">Export CSV</a> | <a href="/report">Rapport Markdown</a></p>'
        html+='<table border=1><tr><th>Score</th><th>Catégorie</th><th>Métier</th><th>Ville</th><th>URL</th></tr>'
        for l in top: html+=f"<tr><td>{l['score']}</td><td>{l['tier']}</td><td>{l['trade']}</td><td>{l['city']}</td><td><a href='{l['url']}'>source</a></td></tr>"
        html+='</table>'
        if self.path=='/export/json':
            self.send_response(302); self.send_header('Location','/static/leads_ranked.json'); self.end_headers(); return
        self.send_response(200); self.send_header('Content-Type','text/html; charset=utf-8'); self.end_headers(); self.wfile.write(html.encode())

def run_dashboard(port=8080):
    HTTPServer(('0.0.0.0',port),H).serve_forever()
