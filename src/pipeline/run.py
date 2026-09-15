"""Pipeline entrypoint. Reaches config, ingest and render. Never imaging."""
from pipeline.config import load_settings, resolve_window
from pipeline.ingest import fetch_batch
from pipeline.render import render_report


def main() -> None:
    settings = load_settings()
    start, end = resolve_window(settings)
    payload = fetch_batch(settings["source_url"])
    rows = [{"merchant": "acme", "amount": len(payload)}]
    print(render_report(batch_id=f"{start}..{end}", rows=rows))


if __name__ == "__main__":
    main()
