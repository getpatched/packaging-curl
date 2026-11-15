# GetPatched curl baseline

This repository starts with an unpatched Debian Trixie amd64 source baseline for curl. It contains no GetPatched CVE patches and no binary packages.

## Baseline state

- Source package: `curl 8.14.1-2+deb13u7`
- Target: Debian Trixie (`trixie`), amd64
- Source pocket: Debian Security
- Source archive pins and prior signed-index provenance: [`baseline/source-pin.json`](baseline/source-pin.json)
- Current verification state: **unverified baseline seed**

The source pin was recorded from a previous signed Debian index verification dated 7 November 2026. Refresh the signed index and verify every archive hash before using this baseline. The `.dsc` uploader signature was not separately authenticated. This commit does not demonstrate an installed amd64 package regression or package build; the exact installed unpatched regression remains required before proposing any fix. The platform verifier currently has no Curl target support.

No CVE remediation is claimed. Do not treat this source-only baseline record as a verified package or release. Production binaries, repository indexes, and releases are out of scope.
