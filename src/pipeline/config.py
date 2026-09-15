"""Pipeline configuration loading.

WIRED: calls yaml.load with the default Loader on pyyaml 5.3.1, which is the
exact sink for CVE-2020-14343 (arbitrary code execution). Reachability should
resolve this one as genuinely reachable, and it is called from run().
"""
from pathlib import Path

import yaml


def load_settings(path: str = "config/pipeline.yaml") -> dict:
    raw = Path(path).read_text(encoding="utf-8")
    return yaml.load(raw)  # noqa: S506 - deliberately the vulnerable sink


def resolve_window(settings: dict) -> tuple[str, str]:
    window = settings.get("window", {})
    return window.get("start", "1970-01-01"), window.get("end", "2099-12-31")
