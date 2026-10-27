# WRN router handoff — Intelbras WRN 240 hardware v1.0

Prepared **2026-10-27, America/Sao_Paulo**. Repository: `zacmero/mero-wrn-router`, branch `main`.

## Start with the corrected identity

The owner explicitly corrected the brand: **Intelbras, not TP-Link**. Earlier enclosure-label photographs identify **WRN 240, hardware V:1.0**, supply **9 V DC / 0.85 A**, labelled default management address **10.0.0.1**. These are photo/history observations, not a new powered inspection. Use the matching supply and verify polarity; never substitute the 12 V supplies belonging to the Vivo routers.

Do not confuse this device with WRN 240 v2, WRN 240i, WRN 240 Slim, WIN 240, or a similar-looking TP-Link. CPU, RAM, physical flash chip/capacity, UART pinout, installed software version and recovery method remain unverified on this unit. Similar chipset reports are research leads, not a compatible flashing recipe.

## Mission and practical constraints

**Obtain a genuine OS shell, identify its privileges/runtime/ABI, then execute a tiny native program in temporary storage.** A web admin panel, vendor command menu, or JavaScript running in the laptop browser does not satisfy the goal. Linux should be established by actual firmware/runtime evidence, not assumed from the enclosure.

The owner is using a **Linux Mint laptop**. Use native Mint commands and `apt` where genuinely needed, not `pacman`; do not assume RTK is installed. The current network interface, IP, route, router identity and credentials are not yet inventoried for WRN.

Equipment constraints inherited from the current lab session:

- The CH341A works over USB, but owner measurements showed approximately 5 V on reported data contacts. It is not approved for direct 3.3 V-target connection.
- The SOIC8 clip is present but physically obstructed on the MitraStar. WRN chip identification and clip clearance have not been inspected; do not assume it fits here.
- ESP32 is ordered but not yet arrived. No female–female jumpers or soldering equipment are currently available.
- Do not make software/firmware analysis wait for another hardware purchase or repeat the unsuccessful multimeter loop.
- The owner wants shell/native execution, not more GVT/Ekioh UI experiments.

Related records: [MitraStar hardware session](https://github.com/zacmero/mero-mitrastar/blob/master/docs/experiments/mitra-hardware-020.md), [minimal buying list](https://github.com/zacmero/mero-mitrastar/blob/master/BUYING-LIST.md), [Askey handoff](https://github.com/zacmero/mero-askey/blob/main/HANDOFF.md). Device-specific results and credentials do not transfer between targets. The Askey remains the previously selected immediate live target; this handoff makes WRN ready as another independent investigation.

## Firmware preservation — already completed, not a future task

The owner explicitly requested downloading and saving the original manufacturer firmware in this repository. That operation completed on **2026-10-27 at 03:22:12 UTC** through [the successful archival run](https://github.com/zacmero/mero-wrn-router/actions/runs/40443767071).

Both **real binary files** are committed to Git, not external-link placeholders, Git LFS pointers or expiring Actions artifacts:

| Preserved object | Repository path / facts |
| --- | --- |
| Untouched vendor ZIP | `firmware/wrn240-v1/firmware_wrn240_v1.0.0_2014-10-24.zip` — 2,881,621 bytes |
| Exact extracted BIN | `firmware/wrn240-v1/extracted/Firmware_WRN240_v1.0.0_2014-10-24/wrn240_1_0_2(111122).bin` — 3,932,160 bytes |
| Provenance and ZIP-member metadata | [manifest.json](firmware/wrn240-v1/manifest.json) |
| Integrity list | [SHA256SUMS](firmware/wrn240-v1/SHA256SUMS) |

The source [Intelbras download page](https://www.intelbras.com/pt-br/ajuda-download/download/roteador-wireless-flexivel-wrn-240) labels its v1 entry **firmware 1.0.2**, with displayed date **21/12/2018**. It links to an archive named `v1.0.0_2014-10-24`; the internal member is named `wrn240_1_0_2(111122).bin`, with ZIP timestamp 2011-11-22 (timezone not specified). Preserve these different fields rather than rewriting filenames or claiming all dates are a release date. The v2 image was not substituted or archived as this unit's firmware.

ZIP CRC and SHA-256 verification passed. The stored Git blob IDs also match the hashes calculated from the downloaded bytes. No independent manufacturer signature/checksum was located: our digest establishes the archived bytes' integrity, not independent authenticity or safe-to-flash compatibility.

### Observed header detail, not a brand reversal

The archived BIN's first 64 bytes, recorded in the manifest, contain the ASCII string `TP-LINK Technologies` beginning at byte offset 4. This is **an observation about the Intelbras-hosted image**, not proof that the owner's branded router is TP-Link or that a TP-Link firmware is interchangeable. It is a useful format/OEM research lead. Do not infer a safe cross-flash from that string.

The BIN size is **not proof of physical flash capacity**. This is a manufacturer update package, **not a full read of the owner's chip**; it does not back up unit-specific bootloader/configuration/calibration data or prove those regions are present. No device firmware has been changed.

## Immediate software-only work available

### WRN-FW-001 — offline image inventory, next proposed analysis

The archive is now independent of vendor-link availability. Begin locally from a clone and verify it:

```sh
git pull --ff-only
sha256sum --check firmware/wrn240-v1/SHA256SUMS
fw='firmware/wrn240-v1/extracted/Firmware_WRN240_v1.0.0_2014-10-24/wrn240_1_0_2(111122).bin'
file "$fw"
od -Ax -tx1 -N128 "$fw"
strings -a -n 8 "$fw" | head -n 60
```

These commands inspect bytes; they do not run firmware or access the router. Work on copies under ignored `.local/analysis/`. Next determine container/header identifiers, image region offsets, compression/filesystem type and any available executable architecture. Do not assume SquashFS, endianness, Linux or a filesystem offset without evidence. Run parsers as an unprivileged user in an isolated analysis environment; firmware is untrusted input.

If a filesystem can be safely extracted, inspect init/startup scripts, account shell fields, management services, the web backend, and any telnet/SSH service configuration. Record what is present versus actually running. A login binary or a string containing `telnet` does not prove an enabled service or usable credentials. No extracted binary is to be executed/emulated automatically by this preservation task.

### WRN-NET-001 — live Ethernet baseline, not yet run

Only when the owner resumes this target: connect the Mint laptop directly to one LAN port, use the correct 9 V supply, leave WAN disconnected, and preserve the laptop's control/internet connection. Do not bridge interfaces or connect multiple lab routers together.

```sh
ip -br link
ip -br -4 addr
ip -4 route
ip neigh
```

Identify the cable-facing interface, DHCP/management address and route. The label's `10.0.0.1` is a default candidate, not permission to probe an unverified household gateway. After confirming identity and route, a bounded service check can use:

```sh
nmap -n -Pn -sT --max-retries 1 --host-timeout 45s \
  -p 21,22,23,80,443,2323,8080 CONFIRMED_WRN_IP
```

Replace the placeholder with the verified target. Install `nmap` only if absent. Inspect the real status page for firmware/build and hardware revision using the owner's intended credentials. Record the UI's version **before considering any update**. The archive must not be flashed merely because it has been preserved.

If SSH/Telnet is available, classify an owner-authorized login accurately: vendor CLI, restricted menu, shell, and privilege level are different results. Prefer a documented/native LAN-only service route supported by actual image/UI evidence over guessing hidden commands or uploading modified firmware.

If the network route is blocked, use the archived image for implementation evidence instead of repeating broad scans. A genuine shell milestone should record bounded `id`, `uname -a` where applicable, CPU/memory/storage information and temporary executable-storage behavior. Establish ABI and transfer method before building native code.

## What this handoff does not authorize

No factory reset, service activation, router-policy change, firmware upload, bootloader write, exploit trial or physical connection is included in this documentation/archive operation. A future persistent change needs a concrete plan and explicit owner instruction, plus appropriate rollback/recovery. No root shell, OpenWrt/DD-WRT support, UART access or compatible modified image has been demonstrated for this unit.

Keep original firmware bytes immutable. Do not replace them with edited images or recompute checksums to conceal a change. Keep private device dumps, passwords, cookies, config exports and raw traffic under ignored `.local/`; vendor originals explicitly requested for this archive are the narrow tracked-binary exception. Vendor copyright/licenses remain intact; no blanket open-source license is applied to the firmware.

## Evidence to record next

Create a dated `docs/experiments/wrn-fw-001.md` or `wrn-net-001.md` only for actual analysis/tests. Include the question, inputs and exact hashes, commands, outputs, interpretation limits and one next action. Do not present the proposed steps above as completed. Re-read this handoff and actual latest reports before repeating work.
