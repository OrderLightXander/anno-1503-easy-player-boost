from __future__ import annotations

import re
import struct
from pathlib import Path

MOD = Path(__file__).resolve().parent
GAME = MOD.parent
ARCHIVES = ("Anlagen.dat", "Anlagen.classic", "Anlagen.addon")
PRODUCERS = {1001, 1002, 1004, 1005, 1006, 1008, 1009, 1010, 1012, 1013, 1014, 1017, 1018, 1019, 1022, 1023, 1027, 1028, 1029, 1030, 1034, 1035, 1036, 1037, 1038, 1039}
PRODUCER_TYPES = {b"HANDWERK", b"HANDWERKWAFFEN", b"KANONENBAU"}
SERVICE = {1320, 1321, 1325, 1330, 1335, 1336, 1337, 1339, 1341, 1342, 1346, 1347, 1350, 1376, 1377, 1378, 1379}
SERVICE_TYPES = {b"KAPELLE", b"KIRCHE", b"WIRT", b"ARZT", b"GERICHT", b"BRUNNEN", b"SCHULE", b"FEUERWEHR", b"BADEHAUS", b"BIBLIOTHEK", b"HOCHSCHULE"}
CLAIM = {1301, 1302, 1303, 1304, 1305, 1306}
CLAIM_TYPES = {1301: b"MARKT", 1302: b"KONTOR", 1303: b"MARKT", 1304: b"KONTOR", 1305: b"MARKT", 1306: b"KONTOR"}
CLAIM_TITLES = {1301: b"Markthaupt01", 1302: b"Kontor01", 1303: b"Markthaupt02", 1304: b"Kontor02", 1305: b"Markthaupt03", 1306: b"Kontor03"}


def entries(data: bytes):
    for match in re.finditer(b"PRODTYPE", data):
        p = match.start()
        if p + 16 > len(data):
            continue
        name_len = struct.unpack_from("<I", data, p + 12)[0]
        if name_len > 64:
            continue
        kind = data[p + 16 : p + 16 + name_len].rstrip(b"\0")
        entry = data.rfind(b"ENTRY", 0, p)
        if entry < 0:
            continue
        asset_id = struct.unpack_from("<I", data, entry + 20)[0]
        prod = data.find(b"PROD3", p, p + 100)
        if prod < 0 or struct.unpack_from("<I", data, prod + 12)[0] != 68:
            continue
        yield p, prod, asset_id, kind


def embedded_titles(data: bytes, p: int) -> set[bytes]:
    titles: set[bytes] = set()
    for match in re.finditer(b"TITLE", data[p : min(len(data), p + 2200)]):
        q = p + match.start()
        name_len = struct.unpack_from("<I", data, q + 12)[0]
        if 0 < name_len < 100:
            title = data[q + 16 : q + 16 + name_len].rstrip(b"\0")
            if title and all(32 <= char < 127 for char in title):
                titles.add(title)
    return titles


def patch_archive(data: bytes, filename: str) -> bytes:
    out = bytearray(data)
    prod_seen: set[int] = set()
    service_seen: set[int] = set()
    claim_seen: set[int] = set()

    for p, prod, asset_id, kind in entries(data):
        payload = prod + 16
        if asset_id in PRODUCERS and kind in PRODUCER_TYPES:
            interval = struct.unpack_from("<f", data, payload + 16)[0]
            if interval <= 0:
                raise ValueError(f"{filename}: invalid cycle interval for asset {asset_id}: {interval}")
            struct.pack_into("<f", out, payload + 16, max(0.1, interval / 4.0))
            prod_seen.add(asset_id)

        if asset_id in SERVICE and kind in SERVICE_TYPES:
            coverage = struct.unpack_from("<f", data, payload + 16)[0]
            if coverage < 0:
                raise ValueError(f"{filename}: invalid service coverage for asset {asset_id}: {coverage}")
            struct.pack_into("<f", out, payload + 16, coverage * 2.0)
            service_seen.add(asset_id)

        if asset_id in CLAIM and kind == CLAIM_TYPES[asset_id]:
            if CLAIM_TITLES[asset_id] not in embedded_titles(data, p):
                raise ValueError(f"{filename}: warehouse/market asset {asset_id} title did not match")
            for offset in (8, 12, 16):
                struct.pack_into("<f", out, payload + offset, 30.0)
            claim_seen.add(asset_id)

    if prod_seen != PRODUCERS:
        raise ValueError(f"{filename}: producer record mismatch: {sorted(prod_seen)}")
    if service_seen != SERVICE:
        raise ValueError(f"{filename}: service record mismatch: {sorted(service_seen)}")
    if claim_seen != CLAIM:
        raise ValueError(f"{filename}: warehouse/market record mismatch: {sorted(claim_seen)}")
    if len(out) != len(data):
        raise ValueError(f"{filename}: unexpected output size change")
    return bytes(out)


def double_resident_growth() -> None:
    source = MOD / "Original_BGruppen.dat"
    if not source.is_file():
        source = GAME / "Data" / "BGruppen.dat"
    if not source.is_file():
        raise FileNotFoundError("Original_BGruppen.dat backup or game Data\\BGruppen.dat was not found")
    text = source.read_text(encoding="cp1252")
    count = 0
    updated = []
    for line in text.splitlines(keepends=True):
        if re.match(r"^\s*VermehrTab:", line):
            match = re.match(r"^(\s*VermehrTab:\s*)([^\r\n]*)(\r?\n)?$", line)
            if not match:
                raise ValueError("Could not parse resident growth table")
            values = [float(value.strip()) for value in match.group(2).split(",")]
            if len(values) != 5:
                raise ValueError("Expected five values in each resident growth table")
            values = [value * 2 for value in values]
            newline = match.group(3) or ""
            updated.append(match.group(1) + ",".join(f"{value:g}" for value in values) + newline)
            count += 1
        else:
            updated.append(line)
    if count != 5:
        raise ValueError(f"Expected five resident groups, found {count}")
    (MOD / "BGruppen.dat").write_bytes("".join(updated).encode("cp1252"))


def main() -> None:
    for filename in ARCHIVES:
        original = MOD / f"Original_{filename}"
        if not original.is_file():
            original = GAME / filename
        if not original.is_file():
            raise FileNotFoundError(f"Missing original backup and game archive: {filename}")
        patched = patch_archive(original.read_bytes(), filename)
        (MOD / filename).write_bytes(patched)
    double_resident_growth()
    print("Built Anno 1503 Easy Player Boost: 26 producers, 17 service buildings, 6 warehouses/markets, and 5 resident groups.")
    print("Carrier movement speed is not changed in this build.")


if __name__ == "__main__":
    main()
