# GetPatched curl baseline

This repository starts with an unpatched Debian Trixie amd64 source baseline for curl. It contains no GetPatched CVE patches and no binary packages.

## Baseline state

- Source package: `curl 8.14.1-2+deb13u7`
- Target: Debian Trixie (`trixie`), amd64
- Source pocket: Debian Security
- Source archive pins and prior signed-index provenance: [`baseline/source-pin.json`](baseline/source-pin.json)
- Current verification state: **installed unpatched baseline regression verified; package build pending**

The source pin was refreshed from current signed Debian indexes on 15 November 2026, and all exact source archive hashes match the signed Sources stanza. The `.dsc` uploader signature was not separately authenticated. The exact installed amd64 unpatched regression is retained under `baseline/regression/`; the package build remains pending. The platform verifier currently has no Curl target support, so patched package acceptance remains unavailable through that workflow.

No CVE remediation is claimed. Do not treat this source-only baseline record as a verified package or release. Production binaries, repository indexes, and releases are out of scope.
