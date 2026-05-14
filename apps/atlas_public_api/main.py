from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class Handler(BaseHTTPRequestHandler):
    def send_json(self, code: int, data: dict) -> None:
        body = json.dumps(data, ensure_ascii=False, sort_keys=True).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        path = self.path.split("?", 1)[0]

        if path in ("", "/"):
            self.send_json(200, {
                "service": "atlas-public-api",
                "status": "online",
                "endpoints": ["/health", "/readiness", "/security", "/version"],
            })
            return

        if path == "/health":
            self.send_json(200, {
                "service": "atlas-public-api",
                "status": "ok",
            })
            return

        if path == "/readiness":
            self.send_json(200, {
                "service": "atlas-public-api",
                "database_secret_present": os.path.isfile(".atlas_secrets/DATABASE_PUBLIC_URL"),
                "r2_secret_present": os.path.isfile(".atlas_secrets/r2.env"),
                "google_credentials_present": os.path.isfile(".atlas_secrets/google_credentials.json"),
                "google_token_present": os.path.isfile(".atlas_secrets/google_oauth_token.json"),
                "production_ready": False,
                "public_saas_ready": False,
            })
            return

        if path == "/security":
            self.send_json(200, {
                "service": "atlas-public-api",
                "secrets_exposed": False,
                "https_required_in_public": True,
                "tenant_isolation_required": True,
                "audit_required": True,
            })
            return

        if path == "/version":
            self.send_json(200, {
                "service": "atlas-public-api",
                "version": "step6-railway-minimal",
                "deployment_target": "railway",
            })
            return

        self.send_json(404, {"error": "not_found", "path": path})


def main() -> None:
    port = int(os.environ.get("PORT", "8080"))
    host = os.environ.get("HOST", "0.0.0.0")
    print(f"ATLAS public API listening on {host}:{port}")
    ThreadingHTTPServer((host, port), Handler).serve_forever()


if __name__ == "__main__":
    main()
