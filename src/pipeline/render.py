"""Settlement report rendering.

WIRED: renders untrusted template content through jinja2, which arrives
TRANSITIVELY via flask 1.1.2 rather than as a direct dependency. That
placement is deliberate -- Tier 2 reachability only ever resolves transitive
dependency CVEs, so a transitive jinja2 is resolvable where a direct one
would not be.
"""
from jinja2 import Template

REPORT = """
Settlement {{ batch_id }}
{% for row in rows %}  {{ row.merchant }}  {{ row.amount }}
{% endfor %}
"""


def render_report(batch_id: str, rows: list[dict]) -> str:
    return Template(REPORT).render(batch_id=batch_id, rows=rows)


def render_custom(template_source: str, **context) -> str:
    return Template(template_source).render(**context)
