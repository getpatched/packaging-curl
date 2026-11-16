#!/usr/bin/env python3
"""Safe local regression for CVE-2026-94266; uses synthetic credentials only."""
import argparse, base64, http.server, pathlib, subprocess, tempfile, threading

class Handler(http.server.BaseHTTPRequestHandler):
    requests = []
    def do_GET(self):
        self.__class__.requests.append((self.path, self.headers.get("Authorization")))
        if self.path == "/start":
            self.send_response(301); self.send_header("Location", "/final")
        else:
            self.send_response(200)
        self.send_header("Content-Length", "0"); self.end_headers()
    def log_message(self, *_):
        pass

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--curl", default="curl")
    ap.add_argument("--expect", choices=("vulnerable", "fixed"), required=True)
    args = ap.parse_args()
    Handler.requests = []
    server = http.server.HTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
    try:
        with tempfile.TemporaryDirectory(prefix="cve-2026-94266-") as td:
            netrc = pathlib.Path(td) / "netrc"
            netrc.write_text("machine 127.0.0.1 login fixture-user password fixture-pass\n")
            netrc.chmod(0o600)
            url = f"http://127.0.0.1:{server.server_port}/start"
            proc = subprocess.run([args.curl, "--silent", "--show-error", "--netrc-optional", "--netrc-file", str(netrc), "-L", "-o", "/dev/null", "-w", "EFFECTIVE_URL=%{url_effective}\n", url], text=True, capture_output=True, timeout=15)
            if proc.returncode:
                raise SystemExit(f"curl failed: {proc.returncode}: {proc.stderr}")
            expected_auth = "Basic " + base64.b64encode(b"fixture-user:fixture-pass").decode()
            if [p for p, _ in Handler.requests] != ["/start", "/final"]:
                raise SystemExit(f"unexpected requests: {Handler.requests!r}")
            if any(auth != expected_auth for _, auth in Handler.requests):
                raise SystemExit(".netrc credentials were not used on both local requests")
            effective = proc.stdout.strip().removeprefix("EFFECTIVE_URL=")
            contains = "fixture-user:fixture-pass@" in effective
            if (args.expect == "vulnerable") != contains:
                raise SystemExit(f"wrong effective URL for {args.expect}: {effective}")
            print(f"PASS expectation={args.expect} effective={effective} requests=2 auth=netrc")
    finally:
        server.shutdown(); server.server_close(); thread.join(timeout=2)

if __name__ == "__main__": main()
