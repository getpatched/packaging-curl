# Exact installed baseline verification

On 15 November 2026, the isolated pinned `linux/amd64` Debian Trixie container refreshed current Debian `trixie`, `trixie-updates`, and `trixie-security` apt indexes. APT accepted the signed Debian indexes and installed the exact Trixie Security `curl` and `libcurl4t64` packages at `8.14.1-2+deb13u7`. The snapshot-fastly source previously recorded in the seed failed TLS validation in this container; it was removed before installation, and the signed live Debian indexes supplied the exact package version.

The local-only HTTP regression served on 127.0.0.1. Two sequential requests using different `host!` bindings reused one connection, and the second request incorrectly originated from 127.0.0.1 rather than 127.0.0.2. Identical-binding reuse and a fresh 127.0.0.2 transfer passed as controls. The raw result and runnable Python fixture are in `regression/`.

This verifies the installed vulnerable baseline for CVE-2026-107929. It does not verify a patched Debian package, Debian package build/tests, compatibility, scans, signed candidate APT, hosted package CI, independent review, or release. No fix is included in this baseline commit. The `.dsc` uploader signature was not separately authenticated; source file hashes match the signed Sources index.
