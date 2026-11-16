# GetPatched curl packaging candidate

This repository contains a clean unpatched Debian Trixie amd64 baseline and target-specific development recipes for curl.

## CVE-2026-94266 candidate

The candidate backports upstream commit `7a6bd027d0de2b6857472d35da090ef60cc29f19` to source `8.14.1-2+deb13u7`. The exact installed vulnerable baseline was reproduced using a loopback HTTP redirect and synthetic `.netrc` credentials; `CURLINFO_EFFECTIVE_URL` exposed those credentials. Patch application was checked with zero fuzz.

Candidate status: the target-specific patch compiles in a local static OpenSSL source build, and the focused patched-source regression passes. This is not a Debian `.deb` build or installed patched package. The Debian package build, package test suite, installed patched regression, compatibility, scans, hosted verifier/CI, independent review, signed APT and merge remain pending. Do not count this CVE as verified or publish production artifacts.

- Baseline provenance: [`baseline/source-pin.json`](baseline/source-pin.json)
- Retained baseline result: [`baseline/verification.json`](baseline/verification.json)
- Candidate target: [`targets/debian/trixie-amd64.json`](targets/debian/trixie-amd64.json)
- Regression: [`tests/regression.py`](tests/regression.py)
- Source patch: [`patches/CVE-2026-94266-debian.patch`](patches/CVE-2026-94266-debian.patch)
