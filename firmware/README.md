# Preserved manufacturer firmware

## Scope

This directory contains the original **Intelbras WRN 240 hardware v1** download that the owner explicitly requested be preserved in the repository. It is a manufacturer-distributed update package, not a dump from the owner's device. Do not conflate hardware v1 with firmware-version text, and do not use v2/240i/Slim/other-vendor images interchangeably.

## Acquisition

- Official index: https://www.intelbras.com/pt-br/ajuda-download/download/roteador-wireless-flexivel-wrn-240
- Listing: `WRN 240 v1 - Firmware versão 1.0.2`; displayed date `21/12/2018`.
- Original HTTPS download: https://backend.intelbras.com/sites/default/files/integration/firmware_wrn240_v1.0.0_2014-10-24.zip
- Actual acquisition time: `2026-10-27T03:22:12.241140+00:00` (00:22:12 in America/Sao_Paulo).
- Successful run: https://github.com/zacmero/mero-wrn-router/actions/runs/40443767071
- Original archive was downloaded without content changes. ZIP integrity was checked; the member was extracted as bytes, not executed. The workflow committed both binary objects and the metadata directly into Git.

The conversation workspace could not reach the vendor download, so acquisition was performed by a bounded repository-side job on a standard GitHub-hosted runner. It did not run on the owner's Mint laptop, connect to a router, or execute firmware. The initial automatic trigger was removed after success; the retained workflow is manual-only, with no schedule, caches or expiring artifact dependency.

## Objects and exact digests

| Object | Bytes | SHA-256 |
| --- | ---: | --- |
| `wrn240-v1/firmware_wrn240_v1.0.0_2014-10-24.zip` | 2,881,621 | `351a4f70430274ab58418eb56ee26375f8e9a4af47c560cd1a2533b5070f2a83` |
| `wrn240-v1/extracted/Firmware_WRN240_v1.0.0_2014-10-24/wrn240_1_0_2(111122).bin` | 3,932,160 | `44449e24b648605bfd72366c1d0e8c1d4b89f088a3fe4b4abd2c4e29f7a9eb81` |

Git blob SHA-1 values, calculated with Git's blob header and confirmed against the repository tree:

- ZIP: `888c851fe372fed82a3b52b2dcce9abadf0482c1`.
- BIN: `02daf08f1bd245938756d99fb2fb283bb384f256`.

See [manifest.json](wrn240-v1/manifest.json) for response headers, member CRC and timestamp, source fields and the first 64 payload bytes. The server's Last-Modified date, index date, outer filename date and member timestamp have different meanings; none is automatically the exact release date of the firmware.

## Verify from repository root

```sh
sha256sum --check firmware/wrn240-v1/SHA256SUMS
```

Both entries must report `OK`. Do not silently regenerate checksums after modifying an original. Work on copies under `.local/analysis/` and record their separate hashes. Keep a local clone as an additional copy rather than relying on the vendor link alone.

## Observations and limits

The official download label says **1.0.2**. The ZIP/folder names say **v1.0.0**, but the contained file is named **wrn240_1_0_2(111122).bin**. Those names are all retained verbatim. No installed-device version was measured during archiving.

The BIN header contains `TP-LINK Technologies` at offset 4. This is a format/OEM lead in the Intelbras-hosted image, **not proof of cross-flash compatibility or a correction of the owner's Intelbras brand identification**. Do not substitute a generic TP-Link image.

The ZIP CRC passed and the two SHA-256 values were checked. These are locally computed integrity values; no independent vendor signature/checksum was found. They establish which bytes were archived, not that the package is signed, safe for every revision, bootable on the owner's current unit or equivalent to a complete flash backup.

No factory reset, flash write, firmware execution, emulation or device test occurred. Do not infer full bootloader/calibration coverage, physical flash capacity, an OS shell or an OpenWrt/DD-WRT installation path from this archive.

## Rights and retention

Firmware remains the property of its respective copyright holders and subject to its original license terms. The source ZIP contains one BIN and no separate license file; redistribution permission was not independently established. This repository does not assert authorship of the firmware or apply a blanket open-source license to it. The owner requested this preservation copy; keep the original source attribution and avoid representing it as a vendor-endorsed distribution.

Do not mix private device dumps, settings exports or credentials into this public directory. Those belong in ignored local storage, not alongside the explicitly requested manufacturer archive.
