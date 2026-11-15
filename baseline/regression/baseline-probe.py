import http.server, json, subprocess, threading
server_ip = "127.0.0.1"
seen = []
class Handler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    def do_GET(self):
        seen.append({"path": self.path, "client_ip": self.client_address[0]})
        self.send_response(200)
        self.send_header("Content-Length", "2")
        self.end_headers()
        self.wfile.write(b"ok")
    def log_message(self, *_):
        pass
server = http.server.ThreadingHTTPServer((server_ip, 0), Handler)
threading.Thread(target=server.serve_forever, daemon=True).start()
base = f"http://{server_ip}:{server.server_port}"
def run(name, first_binding, second_binding):
    seen.clear()
    cmd = ["/usr/bin/curl", "--silent", "--show-error", "--verbose", "--interface", first_binding, base + "/first", "--next", "--silent", "--show-error", "--verbose", "--interface", second_binding, base + "/second"]
    proc = subprocess.run(cmd, text=True, capture_output=True, timeout=8)
    return {"case": name, "bindings": [first_binding, second_binding], "exit": proc.returncode, "reuse_logged": "Re-using existing" in proc.stderr, "connections_created": proc.stderr.count("Connected to "), "requests": list(seen), "stderr": proc.stderr}
def fresh(binding):
    seen.clear()
    proc = subprocess.run(["/usr/bin/curl", "--silent", "--show-error", "--verbose", "--interface", binding, base + "/fresh"], text=True, capture_output=True, timeout=8)
    return {"binding": binding, "exit": proc.returncode, "requests": list(seen), "stderr": proc.stderr}
try:
    result = {
        "installed_versions": subprocess.check_output(["dpkg-query", "-W", "-f=${binary:Package}=${Version}\\n", "curl", "libcurl4t64"], text=True).splitlines(),
        "architecture": subprocess.check_output(["dpkg", "--print-architecture"], text=True).strip(),
        "curl_version": subprocess.check_output(["/usr/bin/curl", "--version"], text=True).splitlines()[0],
        "server_listen_ip": server_ip,
        "different_host_binding": run("different-host-binding", "host!127.0.0.1", "host!127.0.0.2"),
        "same_host_binding_control": run("same-host-binding-control", "host!127.0.0.1", "host!127.0.0.1"),
        "fresh_second_binding_control": fresh("host!127.0.0.2"),
    }
    print(json.dumps(result, indent=2))
finally:
    server.shutdown()
    server.server_close()
