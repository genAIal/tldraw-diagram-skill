# tldraw Diagram Skill for Claude Code

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill that generates [tldraw](https://tldraw.com) diagrams — either as `.tldr` files (importable into tldraw.com) or as tldraw SDK code snippets (`editor.createShapes(...)`).

**Philosophy: Diagrams should argue visually**, not just display information. The skill designs each diagram around visual patterns (fan-out, convergence, timeline, cycle) rather than uniform card grids.

## What it does

- **`.tldr` file generation** — JSON files you open with File > Open in the tldraw web app or load via `loadSnapshot()`.
- **SDK snippet generation** — TypeScript code for tldraw SDK apps (`editor.createShapes` / `createBindings`).
- **tldraw-native** — Uses tldraw's actual shape vocabulary (`geo`, `note`, `frame`, `arrow`, `text`, `line`, `draw`) and semantic color palette. No custom hex colors, no invented shapes.
- **Evidence-driven** — Technical diagrams include real code snippets and JSON samples inside `note` (sticky) shapes.
- **Headless PNG renderer** — Ships a Playwright-based renderer that launches headless Chromium, loads tldraw from [esm.sh](https://esm.sh), and exports PNG via tldraw's own `exportToBlob`.

## Installation

### 1. Add the skill to your Claude Code project

Add the skill path to your project's `CLAUDE.md` or `.claude/settings.json`:

```markdown
## Skills

| Skill | Path | When to use |
|-------|------|-------------|
| **tldraw** | `path/to/tldraw-skill/SKILL.md` | When the user wants a tldraw diagram (.tldr or SDK code) |
```

### 2. Set up the renderer (optional)

The renderer converts `.tldr` files to PNG for visual verification. It requires Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```bash
cd path/to/tldraw-skill/references
uv sync
uv run playwright install chromium
```

### 3. Render a diagram

```bash
cd path/to/tldraw-skill/references
uv run python render_tldraw.py path/to/diagram.tldr
# -> writes path/to/diagram.png
```

Needs network access to [esm.sh](https://esm.sh) on first run; subsequent runs use Chromium's HTTP cache.

**Fallback**: If esm.sh is blocked, open [tldraw.com](https://tldraw.com) > File > Open > pick the `.tldr` file.

## Files

```
tldraw/
  SKILL.md                         # Design methodology + workflow
  README.md                        # This file
  references/
    color-palette.md               # tldraw's semantic color tokens
    shape-templates.md             # Copy-paste templates per shape type
    json-schema.md                 # .tldr file format reference
    render_template.html           # Headless harness: tldraw via esm.sh
    render_tldraw.py               # Playwright-based .tldr -> PNG renderer
    pyproject.toml                 # uv-managed Python deps
```

## Usage

Ask Claude:

> "Create a tldraw diagram showing the webhook handler flow."

or

> "Generate tldraw SDK code for a decision tree showing the triage flow."

The skill reads the references, picks the right visual pattern, and produces either a `.tldr` file or SDK code.

## Customizing colors

tldraw's palette is fixed (`black`, `blue`, `green`, `red`, `orange`, `violet`, `yellow`, plus `light-*` variants and `grey`). `references/color-palette.md` maps each semantic purpose (start, error, AI, evidence, etc.) to one of these tokens. Edit it to change how the skill uses the palette.

## Version compatibility

- **tldraw.com** runs v4+ — the skill generates files in v4 format (arrow `richText`, binding `snap`, note `textFirstEditedBy`).
- **The local renderer** uses tldraw v3 from esm.sh. The render harness (`render_template.html`) automatically converts v4 props back for the v3 renderer.
- Always author files in the current tldraw.com format. The renderer handles backward compatibility.

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI or IDE extension
- Python 3.11+ and [uv](https://docs.astral.sh/uv/) (for the PNG renderer)
- Network access to esm.sh (first render only)

## License

[MIT](LICENSE)
