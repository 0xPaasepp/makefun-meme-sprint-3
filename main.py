#!/usr/bin/python3
"""Drop the meme PNG into the folder the grader expects.

The bytes are copied verbatim, so every run lands the same image
in the output directory, no matter how often it is invoked.
"""
from os import environ
from pathlib import Path

ENTRY = Path(__file__).resolve().parent / "entry.png"
TARGET = Path(environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def run():
    TARGET.mkdir(parents=True, exist_ok=True)
    result = TARGET / "entry.png"
    result.write_bytes(ENTRY.read_bytes())
    print(f"copied {result} ({result.stat().st_size} bytes)")


if __name__ == '__main__':
    run()
