#!/usr/bin/env python3
"""Copy the pre-rendered entry.png to the output directory.

The image was drawn once during the build and ships in this repository
as entry.png. This program only verifies it and copies it to the
directory named by MAKEFUN_OUTPUT_DIR (default /output).

Standard library only.
"""

import binascii
import os
import struct
import sys
from pathlib import Path

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576
MAX_WIDTH = 1024
MAX_HEIGHT = 1024


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def main():
    here = Path(__file__).resolve().parent
    source = here / "entry.png"

    if not source.is_file():
        fail(f"entry.png not found next to main.py ({source})")

    data = source.read_bytes()

    if len(data) > MAX_BYTES:
        fail(f"entry.png is {len(data)} bytes, over the 1048576-byte limit")

    if data[:8] != PNG_SIGNATURE:
        fail("entry.png does not start with the PNG signature")

    if len(data) < 33:
        fail("entry.png is too short to hold a PNG header")

    ihdr_length, ihdr_type = struct.unpack(">I4s", data[8:16])
    if ihdr_type != b"IHDR" or ihdr_length != 13:
        fail("entry.png has no valid IHDR chunk")

    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_WIDTH or height > MAX_HEIGHT:
        fail(f"entry.png is {width}x{height}, over the 1024x1024 limit")
    if width == 0 or height == 0:
        fail("entry.png has a zero dimension")

    # The IHDR chunk carries a CRC over its type and data; a bad CRC
    # means the header itself cannot be trusted.
    ihdr_crc = struct.unpack(">I", data[29:33])[0]
    if binascii.crc32(b"IHDR" + data[16:29]) & 0xFFFFFFFF != ihdr_crc:
        fail("entry.png has a corrupt IHDR checksum")

    # Walk the chunk chain to make sure the file is whole: every chunk
    # must fit inside the file, and the last one must be IEND with
    # nothing after it.
    pos = 33
    seen_iend = False
    while pos < len(data):
        if pos + 8 > len(data):
            fail("entry.png ends in the middle of a chunk header")
        chunk_length, chunk_type = struct.unpack(">I4s", data[pos:pos + 8])
        end = pos + 8 + chunk_length + 4
        if end > len(data):
            fail(f"entry.png chunk {chunk_type!r} is truncated")
        if chunk_type == b"IEND":
            if chunk_length != 0 or end != len(data):
                fail("entry.png has data after its IEND chunk")
            seen_iend = True
            break
        pos = end
    if not seen_iend:
        fail("entry.png has no IEND chunk")

    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / "entry.png"

    with open(destination, "wb") as out:
        out.write(data)

    print(f"wrote {destination} ({len(data)} bytes, {width}x{height})")


if __name__ == "__main__":
    main()
