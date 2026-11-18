# GetPatched curl packaging

This recipe builds curl for Debian Trixie amd64 from source `8.14.1-2+deb13u7`. It backports upstream commit `7a6bd027d0de2b6857472d35da090ef60cc29f19` for CVE-2026-94266.

GitHub Actions builds the patched Debian packages, verifies a signed APT install, runs the installed curl CLI and libcurl SDK checks, and compares advisory scans of the pinned baseline and candidate.

- [Source pin](baseline/source-pin.json)
- [Trixie packaging target](targets/debian/trixie-amd64.json)
- [Backport](patches/CVE-2026-94266-debian.patch)

[![advertisement](https://ads.servead.net/i/4f8885b6-55a6-42d8-aaf1-1c1741a51698.svg)](https://ads.servead.net/c/4f8885b6-55a6-42d8-aaf1-1c1741a51698)
