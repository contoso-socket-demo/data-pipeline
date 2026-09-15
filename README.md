# data-pipeline

Contoso settlement reconciliation pipeline. Python 3.9, uv.

Second ecosystem for the reachability story, so the demo is not Java-only.

## The shape

| Package | Placement | Expected verdict |
|---|---|---|
| `pyyaml==5.3.1` | direct, WIRED (`yaml.load` default Loader) | reachable |
| `jinja2==2.11.2` | TRANSITIVE via flask, WIRED (`Template().render`) | reachable, Tier 2 resolvable |
| `urllib3==1.26.4` | TRANSITIVE via requests | partially reachable |
| `pillow==8.1.0` | direct, never imported outside dead code | **unreachable, ~40 CVEs** |
| `cryptography==3.2` | direct, never imported | **unreachable, ~12 CVEs** |
| `lxml==4.6.2` | direct, never imported | **unreachable, ~4 CVEs** |

`src/pipeline/imaging.py` exists solely to hold pillow's CVE volume in an
unreachable function. Nothing imports it. Wiring it up changes the
percentages, so re-measure if you do.

## Two constraints that are load-bearing

**Python is pinned to 3.9.** `pillow 8.1.0` and `cryptography 3.2` ship no
wheels for 3.11+. On a newer interpreter the `--reach` install fails and the
run silently degrades to Tier 2 results.

**`[tool.uv] constraint-dependencies` pins the transitive tree.** Without it,
uv resolves `jinja2` to 3.1.x and `werkzeug` to 3.1.x, because flask 1.1.2
only sets loose lower bounds. The transitive tree comes out clean and Tier 2
has nothing to resolve. Constraints pin those versions without promoting them
to direct dependencies, which is the distinction the whole demo rests on.

Resolved tree: 6 direct, 14 transitive, 20 total.

## Measured reality, 2026-09-15, and a limitation worth knowing

**Use checkout-service (Java) for the Tier 2 demo, not this repo.**

Two things work against a Python Tier 2 story, and neither is fixable by
picking different packages:

**1. Socket expands each PyPI package into one artifact per wheel.**
13 distinct packages produced 122 pypi artifacts. `pillow@8.1.0` appears many
times, each copy carrying all 40 of its CVEs, which is why the CVE alert count
reads ~1,700 rather than ~60. This is not caused by the lockfile: it persisted
after replacing `uv.lock` with a plain `requirements.txt` (307 artifacts to
127, but still 122 for 13 packages).

**2. Old CVE-carrying transitives require pinning, and pinning makes them
direct.** Tier 2 only ever resolves TRANSITIVE CVEs. With `uv.lock` plus
`[tool.uv] constraint-dependencies`, jinja2 2.11.2 and werkzeug 1.0.1 stayed
transitive and carried CVEs, but every artifact came back `direct=True` and
Tier 2 measured **0%**. With `requirements.txt`, transitives are correctly
classified non-direct, but resolution picks jinja2 3.1.6 and werkzeug 3.1.8,
both with **zero CVEs**. Either way Tier 2 has nothing to resolve.

Measured with `uv.lock`: Tier 2 **0.0%** noise reduction (98.4%
`direct_dependency`), Tier 1 **2.1%** with 95.1% carrying no verdict at all.

### What this repo is still good for

A second-ecosystem Tier 1 run, and proving Python reachability works at all.
Coana resolved 27 reachable and 37 unreachable findings here.

If you need a strong Python noise-reduction number, the repo needs rebuilding
around a direct dependency whose own metadata forces old transitives, rather
than around constraint pins. That has not been done.
