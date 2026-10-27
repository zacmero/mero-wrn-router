# Agent instructions — mero-wrn-router

Read `README.md`, `HANDOFF.md`, `firmware/README.md` and the latest actual experiment reports first.

## Target and goal

- Target is **Intelbras WRN 240, hardware V:1.0** from the owner's label photograph. The owner explicitly corrected an earlier TP-Link misidentification.
- WRN 240 v2, WRN 240i, WRN 240 Slim, WIN 240 and similar TP-Link models are not interchangeable targets.
- Goal is a genuine OS shell, followed by verified native program execution. Web pages, vendor CLI access and laptop-side JavaScript do not satisfy it.
- Do not assume Linux, CPU architecture, RAM/flash capacity, pinout or recovery from a similar model. The TP-LINK header string in the official binary is an image observation, not cross-flash authorization.

## Preserve the archive

- The owner explicitly authorized archiving the official vendor ZIP and original BIN in Git. They are the narrow exception to the normal exclusion of firmware/private dumps.
- Verify `firmware/wrn240-v1/SHA256SUMS` before analysis. Keep original bytes, filenames, source attribution and acquisition metadata immutable.
- Never replace original bytes with modified firmware, silently recompute expected hashes or substitute v2 firmware.
- Analyze copies under `.local/analysis/`. Treat firmware as untrusted input; do not execute extracted binaries or auto-launch emulation during archival work.
- Locally computed hashes are integrity evidence, not a vendor signature. An update package is not the owner's complete device backup.
- No blanket open-source license is applied to the vendor firmware. Preserve source/rights statements.

## Practical session rules

- Current workstation is the owner's Linux Mint laptop. Do not issue Arch `pacman` commands or assume RTK/interface names/old SSH paths.
- Establish target, cable-facing interface and route before traffic; preserve the owner's control/internet path. No DHCP/DNS impersonation, bridge or household-network redirection by default.
- Begin with offline image analysis or bounded read-only Ethernet inventory. Avoid repeated scans/probe loops with no new question.
- The CH341A has approximately 5 V signal measurements and is not approved for direct connection to these router targets. ESP32 has not arrived; female–female jumpers and soldering equipment are absent. Do not silently depend on them.
- The WRN label specifies 9 V input. Do not substitute a 12 V Vivo adapter. Verify polarity and connector before powering.
- Keep owner observations, external claims, measured output and hypotheses distinct. The preservation operation did not run a WRN scan/login, flash operation or shell.
- Device writes, service activation, resets, bootloader changes, hardware connections and firmware uploads need a specific plan and explicit owner instruction. Documentation/preservation is not blanket permission to run them.
- No credential guessing or speculative hidden-handler invocation. Use intended owner credentials privately and record exact access boundaries.

## Repository hygiene

Store raw captures, passwords, tokens, settings exports, private device dumps and modified binaries under ignored `.local/`. Commit reviewed results and genuine hashes. Do not copy credentials or target defaults from MitraStar/Askey/GVT. Keep older evidence intact and do not mark proposed experiments as completed.
