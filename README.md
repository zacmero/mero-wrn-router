# Mero WRN Router — Intelbras WRN 240 v1

**Intelbras, not TP-Link.** The owner's earlier label photograph identifies **WRN 240, hardware V:1.0**, with **9 V DC / 0.85 A** input. Do not interchange its power supply with the 12 V Vivo-router supplies or substitute firmware for another WRN variant.

Goal: a genuine operating-system shell, then a tiny native program. Start with [HANDOFF.md](HANDOFF.md).

## Original firmware is preserved in Git

Downloaded directly from the official Intelbras link on **2026-10-27**, extracted without modifying the payload, and committed as real binary files. ZIP CRC and SHA-256 verification passed. These are not just URLs or temporary Actions artifacts.

| File | Size | Link |
| --- | ---: | --- |
| Original vendor ZIP | 2,881,621 bytes | [firmware_wrn240_v1.0.0_2014-10-24.zip](firmware/wrn240-v1/firmware_wrn240_v1.0.0_2014-10-24.zip) |
| Firmware BIN, unchanged | 3,932,160 bytes | [wrn240_1_0_2(111122).bin](firmware/wrn240-v1/extracted/Firmware_WRN240_v1.0.0_2014-10-24/wrn240_1_0_2%28111122%29.bin) |
| SHA-256 list | — | [SHA256SUMS](firmware/wrn240-v1/SHA256SUMS) |
| URLs, acquisition time, headers, hashes and ZIP-member metadata | — | [manifest.json](firmware/wrn240-v1/manifest.json) |

The [official page](https://www.intelbras.com/pt-br/ajuda-download/download/roteador-wireless-flexivel-wrn-240) lists **WRN 240 v1 / firmware 1.0.2**. The outer ZIP is named `v1.0.0`; the actual member is named `wrn240_1_0_2(111122).bin`. Both names are preserved. Its first header bytes include `TP-LINK Technologies`, an image-format/OEM lead—not proof that this Intelbras device accepts generic TP-Link firmware.

See [archive notes](firmware/README.md) for provenance and limitations. This is a **vendor update image, not a full backup of the owner's flash**. No router has been updated or reset, and no shell has been obtained by archiving it.

## Terminal access

From a local clone:

```sh
git pull --ff-only
sha256sum --check firmware/wrn240-v1/SHA256SUMS
less HANDOFF.md
```

To create a first clone:

```sh
git clone https://github.com/zacmero/mero-wrn-router.git
cd mero-wrn-router
sha256sum --check firmware/wrn240-v1/SHA256SUMS
```

Once cloned, the binary and its integrity list remain available even if the original vendor link disappears. Verification does not contact the router or require an internet connection.

## Current investigation status

No WRN live network scan, login, installed-build check, board probing, serial capture or flash operation was performed during this initialization. Current host is the owner's Linux Mint laptop; interface/IP details must be measured, not copied from MitraStar or Askey.

The next proposed routes are offline inspection of the preserved image and an independent, bounded Ethernet management check. No soldering equipment or programmer repair is needed for those steps. Firmware presence is useful evidence, not a guaranteed shell route. See [AGENTS.md](AGENTS.md) and the handoff before testing.

Related projects: [MitraStar](https://github.com/zacmero/mero-mitrastar), [Askey](https://github.com/zacmero/mero-askey), [GVT receiver](https://github.com/zacmero/mero-stb-lab). Preserve each device's identity and evidence separately.

## Preservation tooling

[tools/archive_vendor_firmware.py](tools/archive_vendor_firmware.py) verifies the existing archive and refuses to overwrite changed bytes. The archival workflow was run successfully to preserve the files and is retained for manual use, with no scheduled polling. Original vendor copyright and licenses remain in force; these binaries are not relicensed as project code.
