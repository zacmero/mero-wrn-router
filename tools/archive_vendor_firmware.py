#!/usr/bin/env python3
"""Archive the official WRN 240 v1 download; never execute or flash its contents.

Writes the untouched vendor ZIP, bounded safe extraction, SHA-256 checksums,
and provenance. Existing archives are verified rather than overwritten.
"""
from __future__ import annotations

import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import stat
import time
from datetime import datetime, timezone
import urllib.request
from urllib.parse import urlparse
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "firmware/wrn240-v1"
NAME = "firmware_wrn240_v1.0.0_2014-10-24.zip"
URL = "https://backend.intelbras.com/sites/default/files/integration/" + NAME
INDEX = "https://www.intelbras.com/pt-br/ajuda-download/download/roteador-wireless-flexivel-wrn-240"
MAX_DOWNLOAD = 32 * 1024 * 1024
MAX_EXPANDED = 64 * 1024 * 1024


def fingerprint(data: bytes) -> dict:
    return {
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "git_blob_sha1": hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest(),
    }


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != data:
            raise RuntimeError(f"Refusing to overwrite different preserved bytes: {path}")
        return
    temp = path.with_name(path.name + ".partial")
    temp.write_bytes(data)
    temp.replace(path)


def download() -> tuple[bytes, str, dict]:
    error = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(URL, headers={"User-Agent": "Mero-WRN-Preservation/1.0", "Accept": "application/zip,*/*"})
            with urllib.request.urlopen(req, timeout=60) as response:
                resolved = response.geturl()
                if urlparse(resolved).scheme != "https" or urlparse(resolved).hostname != "backend.intelbras.com":
                    raise RuntimeError(f"Unexpected download redirect: {resolved}")
                data = response.read(MAX_DOWNLOAD + 1)
                if len(data) > MAX_DOWNLOAD:
                    raise RuntimeError("Download exceeds preservation size bound")
                headers = {k: response.headers.get(k) for k in ("Content-Type", "Content-Length", "Last-Modified", "ETag")}
            if not data.startswith(b"PK\x03\x04"):
                raise RuntimeError("Official response is not a ZIP; refusing to archive an error/HTML page as firmware")
            return data, resolved, headers
        except Exception as exc:
            error = exc
            if attempt < 2:
                time.sleep(2 * (attempt + 1))
    raise RuntimeError("Official firmware download failed") from error


def verify_existing() -> bool:
    manifest_path = OUT / "manifest.json"
    if not manifest_path.exists():
        return False
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for item in [manifest["archive"], *manifest["members"]]:
        p = ROOT / item["repository_path"]
        if not p.resolve().is_relative_to(OUT.resolve()):
            raise RuntimeError("Manifest path escapes archive directory")
        result = fingerprint(p.read_bytes())
        for key in ("bytes", "sha256", "git_blob_sha1"):
            if result[key] != item[key]:
                raise RuntimeError(f"Archive verification failed: {p}: {key}")
    print("Existing archive verified; original acquisition metadata retained.")
    return True


def main() -> None:
    if verify_existing():
        return
    data, final_url, headers = download()
    archive_path = OUT / NAME
    archive = {"repository_path": archive_path.relative_to(ROOT).as_posix(), **fingerprint(data)}
    members = []
    extracted = []
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        infos = z.infolist()
        if len(infos) > 128 or sum(i.file_size for i in infos) > MAX_EXPANDED:
            raise RuntimeError("ZIP expansion exceeds preservation limits")
        bad = z.testzip()
        if bad is not None:
            raise RuntimeError(f"ZIP CRC validation failed: {bad}")
        seen = set()
        for item in infos:
            name = PurePosixPath(item.filename)
            if name.is_absolute() or ".." in name.parts or "\\" in item.filename or ":" in item.filename:
                raise RuntimeError(f"Unsafe ZIP path: {item.filename!r}")
            if stat.S_ISLNK(item.external_attr >> 16):
                raise RuntimeError("Symlink in vendor archive refused")
            if item.is_dir():
                continue
            path = OUT / "extracted" / str(name)
            if path in seen:
                raise RuntimeError("Duplicate ZIP member path")
            seen.add(path)
            content = z.read(item)
            members.append({
                "original_zip_member": item.filename,
                "repository_path": path.relative_to(ROOT).as_posix(),
                "zip_timestamp_unspecified_timezone": list(item.date_time),
                "crc32_hex": f"{item.CRC:08x}",
                "first_64_bytes_hex": content[:64].hex(),
                **fingerprint(content),
            })
            extracted.append((path, content))
    if not members:
        raise RuntimeError("Archive contains no files")
    manifest = {
        "device_family": "Intelbras WRN 240",
        "manufacturer_target_hardware_revision": "v1",
        "source_index_url": INDEX,
        "source_index_label": "WRN 240 v1 - Firmware versao 1.0.2",
        "source_index_displayed_date": "2018-12-21",
        "source_download_url": URL,
        "resolved_download_url": final_url,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "response_headers": headers,
        "archive": archive,
        "members": members,
        "zip_crc_validation": "passed",
        "version_caution": "Official index says 1.0.2 but original ZIP filename says v1.0.0. Both preserved verbatim; internal build and installed device version must be inspected separately.",
        "limitations": [
            "SHA-256 is computed from received bytes; no independent manufacturer checksum or signature was located.",
            "HTTPS provenance and CRC/checksums do not establish safe-to-flash compatibility or authenticity by independent signature.",
            "Vendor update package is not a full backup of the owner's flash, bootloader, configuration or calibration.",
            "Downloaded content was not executed, emulated, modified or flashed.",
            "Vendor copyright and any original licenses remain in force; archiving does not relicense the firmware."
        ],
        "github_run_id": os.environ.get("GITHUB_RUN_ID"),
    }
    atomic_write(archive_path, data)
    for path, content in extracted:
        atomic_write(path, content)
    records = [archive, *members]
    sums = "".join(f"{item['sha256']}  {item['repository_path']}\n" for item in records)
    atomic_write(OUT / "SHA256SUMS", sums.encode())
    atomic_write(OUT / "manifest.json", (json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode())
    verify_existing()
    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
