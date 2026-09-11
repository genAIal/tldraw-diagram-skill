# tldraw Diagram Skill for Claude Code

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill that generates [tldraw](https://tldraw.com) diagrams — either as `.tldr` files (importable into tldraw.com) or as tldraw SDK code snippets (`editor.createShapes(...)`).

> **Unofficial community project.** This skill is not affiliated with, endorsed by, or supported by tldraw Inc. "tldraw" is used purely to describe compatibility with the tldraw file format and SDK.

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

### 3. Validate the file

```bash
cd path/to/tldraw-skill/references
uv run python validate_tldr.py path/to/diagram.tldr   # or plain: python3 validate_tldr.py ...
```

Pure standard library — works without the renderer setup above. Run it before rendering. It catches the faults that make tldraw **silently** refuse a file —
invalid index keys, notes with `fontSizeAdjustment: 0`, bindings pointing nowhere. When such a
file is opened, tldraw shows an empty canvas and no error at all, while the PNG below still
looks perfect. Exit code 1 means errors.

### 4. Render a diagram

```bash
cd path/to/tldraw-skill/references
uv run python render_tldraw.py path/to/diagram.tldr
# -> writes path/to/diagram.png
```

**The PNG is not an import test.** The renderer runs tldraw v3 and builds the document through
`editor.createShapes`, a path that skips the validation tldraw.com applies when importing a
file. A clean render says the layout is right, not that the file opens. See SKILL.md,
*Validate against the target*.

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
    validate_tldr.py               # Static .tldr checks — run before rendering
    render_template.html           # Headless harness: tldraw via esm.sh
    render_tldraw.py               # Playwright-based .tldr -> PNG renderer
    render_svg.py                  # Same harness, exports SVG (vector) instead
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

This skill — its documentation, templates, and renderer scripts — is licensed under [MIT](LICENSE).

**Note on tldraw itself:** The tldraw SDK is **not** MIT-licensed — it is source-available under its own [tldraw license](https://tldraw.dev/community/license). This skill does not redistribute any tldraw code; the headless renderer only loads tldraw at runtime from esm.sh, which is free under the SDK's default terms for development use (the renderer is a local development tool). If you embed tldraw in a production or commercial application, you need your own license from tldraw: a free hobby license (with the "made with tldraw" watermark) or a commercial license — see [tldraw.dev/pricing](https://tldraw.dev/pricing). Opening generated `.tldr` files in the [tldraw.com](https://www.tldraw.com) web app is free.
