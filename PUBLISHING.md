# Publishing loopotel to PyPI

## One-time setup

1. Register the project name **`loopotel`** at [pypi.org](https://pypi.org/).
2. **Preferred:** [trusted publishing](https://docs.pypi.org/trusted-publishers/) on PyPI:
   - **Project:** `loopotel`
   - **Owner:** `KanakMalpani`
   - **Repository:** `loop-observability`
   - **Workflow:** `publish.yml`
3. **Fallback:** add **`PYPI_API_TOKEN`** to this repo's GitHub Actions secrets.

## Publish

Release tag:

```bash
git tag v0.1.0
git push origin v0.1.0
gh release create v0.1.0 --title "v0.1.0" --notes "Initial loopotel release"
```

Or **Actions → Publish to PyPI → Run workflow**.

## Install

```bash
pip install loopotel
pip install "loopotel[loopgym]"   # LoopGym integration
pip install "loopotel[otlp]"       # OTLP export
```

## Verify locally

```bash
pip install build
python -m build
pip install dist/loopotel-*.whl
loopotel-validate --help
pytest tests/ -q
```
