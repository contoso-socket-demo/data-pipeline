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
