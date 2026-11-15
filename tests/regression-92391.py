#!/usr/bin/env python3
"""Bounded local regression for recursive curl_mime_free stack exhaustion."""
import argparse, pathlib, resource, signal, subprocess, tempfile

SOURCE = pathlib.Path(__file__).parent / "fixtures" / "CVE-2026-92391-mime-free-depth.c"

def run_child(binary, depth):
    def limits():
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
        resource.setrlimit(resource.RLIMIT_STACK, (64 * 1024, 64 * 1024))
    return subprocess.run([str(binary), str(depth)], text=True, capture_output=True,
                          timeout=10, preexec_fn=limits)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--expect", choices=("vulnerable", "fixed"), required=True)
    ap.add_argument("--curl-config", default="curl-config")
    ap.add_argument("--cc", default="gcc")
    args = ap.parse_args()
    cflags = subprocess.check_output([args.curl_config, "--cflags"], text=True).split()
    libs = subprocess.check_output([args.curl_config, "--static-libs"], text=True).split()
    with tempfile.TemporaryDirectory(prefix="cve-2026-92391-") as td:
        binary = pathlib.Path(td) / "mime-depth"
        subprocess.run([args.cc, "-O2", *cflags, str(SOURCE), "-o", str(binary), *libs],
                       check=True, timeout=60)
        control = run_child(binary, 50)
        if control.returncode != 0 or "curl_mime_free returned" not in control.stdout:
            raise SystemExit(f"depth-50 control failed: rc={control.returncode} out={control.stdout!r} err={control.stderr!r}")
        deep = run_child(binary, 2000)
        reached_free = "constructed=2000; freeing root" in deep.stdout
        if not reached_free:
            raise SystemExit(f"deep tree construction failed: rc={deep.returncode} out={deep.stdout!r} err={deep.stderr!r}")
        if args.expect == "vulnerable":
            if deep.returncode not in (-signal.SIGSEGV, -signal.SIGBUS):
                raise SystemExit(f"baseline did not signal during recursive free: rc={deep.returncode} out={deep.stdout!r} err={deep.stderr!r}")
        else:
            if deep.returncode != 0 or "curl_mime_free returned" not in deep.stdout:
                raise SystemExit(f"patched deep free failed: rc={deep.returncode} out={deep.stdout!r} err={deep.stderr!r}")
        print(f"PASS expectation={args.expect} control_depth=50 deep_depth=2000 deep_exit={deep.returncode}")

if __name__ == "__main__": main()
