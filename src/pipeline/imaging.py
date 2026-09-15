"""Merchant logo thumbnailing.

DELIBERATELY UNREACHABLE. pillow carries ~40 CVEs at 8.1.0, and nothing in
this package ever calls thumbnail_logo(). It is not imported by __init__,
not referenced by run.py, and has no test. Reachability analysis should
report every one of those CVEs as unreachable, which is the number worth
talking over in a demo.

Do not wire this up without re-measuring the noise-reduction percentages.
"""


def thumbnail_logo(source_path: str, dest_path: str, size: int = 128) -> None:
    from PIL import Image  # noqa: PLC0415 - import kept local and unreached

    with Image.open(source_path) as img:
        img.thumbnail((size, size))
        img.save(dest_path)
