#!/usr/bin/env bash
set -euo pipefail

# curl's local-file upload, resume, and byte-range tests need no network servers.
cases=(204 205 231 1016 1017 1018 1019 1020)
log=$(mktemp)
trap 'rm -f "$log"' EXIT

status=0
timeout --kill-after=10s 180s make -C debian/build/tests am-test \
  "TFLAGS=-n -c ../src/curl ${cases[*]}" >"$log" 2>&1 || status=$?
cat "$log"

python3 - "$log" "$status" "${cases[@]}" <<'PY'
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

log, status, *cases = sys.argv[1:]
output = Path(log).read_text(errors="replace")
passed = set(re.findall(r"^PASS: (\d+) - ", output, re.MULTILINE))
suite = ET.Element("testsuite", name="curl upstream file transfers")
failures = 0
for number in cases:
    case = ET.SubElement(suite, "testcase", classname="curl.upstream", name=f"test{number}")
    if number not in passed:
        ET.SubElement(case, "failure", message="The upstream harness did not report a pass")
        failures += 1

if status != "0" and failures == 0:
    case = ET.SubElement(suite, "testcase", classname="curl.upstream", name="harness")
    ET.SubElement(case, "failure", message=f"The upstream harness exited with {status}")
    failures += 1

suite.set("tests", str(len(suite)))
suite.set("failures", str(failures))
ET.ElementTree(suite).write("/reports/upstream-junit.xml", encoding="utf-8", xml_declaration=True)
sys.exit(bool(failures))
PY
