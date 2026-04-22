---
name: tldraw-diagram
description: Create tldraw `.tldr` JSON files and tldraw SDK snippets that argue visually. Use when the user wants to visualize workflows, architectures, or concepts with tldraw.
---

# tldraw Diagram Creator

Generate `.tldr` JSON files (importable into tldraw.com / tldraw.dev) or tldraw SDK code (`editor.createShapes(...)`) that **argue visually**, not just display information.

**Setup:** See `README.md` for installation notes. Rendering requires the tldraw web app or SDK — see the **Render & Validate** section below.

## Customization

Colors and semantic styles live in `references/color-palette.md`. Read it before generating a diagram. tldraw ships a fixed semantic palette (`black`, `blue`, `green`, `red`, `orange`, `violet`, `light-blue`, `light-green`, `light-red`, `light-violet`, `yellow`, `grey`) — you can't invent hex colors, so the palette file maps each semantic purpose to a tldraw color token.

---

## Core Philosophy

**Diagrams should ARGUE, not DISPLAY.**

A diagram isn't formatted text. It's a visual argument that shows relationships, causality, and flow that words alone can't express. The shape should BE the meaning.

**The Isomorphism Test**: If you removed all text, would the structure alone communicate the concept? If not, redesign.

**The Education Test**: Could someone learn something concrete from this diagram, or does it just label boxes? A good diagram teaches — it shows actual formats, real event names, concrete examples.

---

## Depth Assessment (Do This First)

Before designing, determine what level of detail this diagram needs:

### Simple/Conceptual Diagrams
Use abstract shapes when:
- Explaining a mental model or philosophy
- The audience doesn't need technical specifics
- The concept IS the abstraction

### Comprehensive/Technical Diagrams
Use concrete examples when:
- Diagramming a real system, protocol, or architecture
- The diagram will be used to teach or explain
- The audience needs to understand what things actually look like

**For technical diagrams, include evidence artifacts** — real event names, sample JSON, actual API method names. tldraw's `note` shape (sticky note) and `text` shape are ideal for these.

---

## Two Output Modes

tldraw supports two workflows. Choose based on user intent.

### Mode A — `.tldr` file (default)
A JSON document that can be imported via **File → Open** on tldraw.com / tldraw.dev, or loaded into the SDK with `loadSnapshot()`.
- Best for: one-off diagrams, sharing, archiving, Obsidian / Notion attachments.
- Output: a single `.tldr` file.
- See `references/json-schema.md` for the full record structure.

### Mode B — SDK code snippet
TypeScript/JavaScript that calls `editor.createShapes([...])` inside a tldraw SDK app.
- Best for: users embedding tldraw in a React app, generating diagrams at runtime, or building custom tools.
- Output: a code block with `createShapes` / `createBindings` calls.
- See `references/shape-templates.md` for shape prop templates.

If the user didn't specify, ask: *"`.tldr` file to open in tldraw, or SDK code for a React app?"* Default to `.tldr` if they just said "make a diagram."

---

## tldraw Shape Vocabulary

tldraw has a smaller, more opinionated shape set than generic drawing tools. Use this mapping to choose the right shape for each concept:

| Concept | Shape type | `geo` variant (if geo) |
|---------|-----------|------------------------|
| Process, action, step | `geo` | `rectangle` |
| Start, input, origin | `geo` | `ellipse` or `oval` |
| End, output, result | `geo` | `ellipse` or `oval` |
| Decision, branch | `geo` | `diamond` |
| External system | `geo` | `cloud` |
| Data / storage | `geo` | `cylinder` (if needed) or `rectangle` |
| Comment, callout, evidence | `note` (sticky note) | — |
| Label, annotation | `text` (free-floating) | — |
| Container / group | `frame` | — |
| Connection | `arrow` | — |
| Freeform path | `line` or `draw` | — |
| Code snippet, JSON sample | `note` with monospace font (`mono`) | — |

**tldraw geo variants**: `rectangle`, `ellipse`, `triangle`, `diamond`, `pentagon`, `hexagon`, `octagon`, `star`, `rhombus`, `rhombus-2`, `oval`, `trapezoid`, `arrow-right`, `arrow-left`, `arrow-up`, `arrow-down`, `x-box`, `check-box`, `heart`, `cloud`.

---

## Visual Pattern Library

Map each concept to a pattern that mirrors its behavior. No uniform card grids.

### Fan-Out (One-to-Many)
Central `geo` with `arrow`s radiating to multiple targets. Use for: sources, root causes, hubs.

### Convergence (Many-to-One)
Multiple `geo`s with arrows merging into one. Use for: aggregation, synthesis, funnels.

### Timeline
A horizontal/vertical `line` shape with small `geo` ellipses (~20px) as markers and `text` shapes as free-floating labels. No boxes around labels.

### Tree / Hierarchy
`line` shapes as trunk + branches, `text` shapes as labels. Avoid boxing every node.

### Cycle
3–5 `geo`s arranged in a loop with arrows returning to the start. Use for: feedback loops, iterations.

### Assembly Line
`geo` (input) → `geo` (process, wider) → `geo` (output), all connected with arrows. Use for: transformations.

### Grouped Sections
Wrap related shapes in a `frame` with a descriptive `name`. Frames give you labeled regions without drawing borders manually.

### Evidence Block
A `note` shape (sticky note) containing a code snippet or JSON sample, placed next to the element it explains. Use `font: 'mono'` for code.

---

## Container Discipline

tldraw makes it easy to box everything — resist the urge.

- Default to free-floating `text` shapes for labels, annotations, section titles.
- Use `geo` containers only when the shape carries meaning (decision diamond, process rectangle) or when arrows need to bind to it.
- Use `frame` to group related shapes — it's cleaner than manually drawing a big rectangle behind them.
- Use `note` (sticky) for evidence artifacts (code, JSON, quotes) — its colored background reads as "this is a concrete example."

**Target**: fewer than 30% of text elements inside containers.

---

## Color as Meaning

Every color choice pulls from `references/color-palette.md`. tldraw's palette is semantic — each token has a defined purpose:

- `black` / `grey` — neutral, structural
- `blue` — primary action, main flow
- `green` — success, output, positive
- `red` / `light-red` — error, blocker, warning
- `orange` — caution, intermediate state
- `violet` / `light-violet` — AI, ML, abstract
- `yellow` — evidence, notes, callouts (natural for `note` shape)
- `light-blue` / `light-green` — secondary/supporting variants

**Do not invent hex colors** — tldraw shapes use these named tokens only. If you need a color outside the palette, use `grey` and rely on size/position for emphasis.

---

## Style Defaults

| Prop | Default | When to change |
|------|---------|----------------|
| `size` | `m` | `s` for dense labels, `l`/`xl` for headings |
| `font` | `draw` | `sans` for modern, `serif` for formal, `mono` for code |
| `dash` | `draw` | `solid` for clean/technical, `dashed` for hypothetical/future, `dotted` for weak connection |
| `fill` | `solid` | `semi` for subtle emphasis, `none` for outline-only, `pattern` for texture |
| `color` | `black` | Pull from palette based on semantic purpose |

Default to `font: 'draw'` and `dash: 'draw'` only if the user wants the classic tldraw hand-drawn aesthetic. For technical/professional diagrams use `font: 'sans'`, `dash: 'solid'`, and **`fill: 'solid'`** — shapes without fills look like wireframes and are hard to read. Follow the Excalidraw principle: lighter fill + darker stroke for contrast.

**Arrow kind**: Default to `kind: 'elbow'` (right-angle connections) for flowcharts and technical diagrams. Use `'arc'` only when you need curved arrows, `'line'` for straight diagonal connections.

---

## Layout Principles

### Hierarchy Through Scale
tldraw shapes have `w` and `h` props. Suggested sizes:
- **Hero**: 300×150
- **Primary**: 200×100
- **Secondary**: 140×70
- **Small / marker**: 40×40

### Whitespace
Most important element has the most empty space around it (≥200px).

### Flow Direction
Left→right or top→bottom for sequences. Radial for hub-and-spoke. Don't mix.

### Alignment & Centering
For vertical flowcharts, pick a center x-coordinate and align all main-flow shapes so their horizontal center sits on it: `x = center_x - w/2`. Side branches offset left or right. This creates a clean visual spine.

### Connections Required
Position alone doesn't show relationships. If A relates to B, draw an `arrow`. For `.tldr` files, arrows can bind to shapes via a `binding` record — see `references/json-schema.md`. Use `normalizedAnchor: {x: 0.5, y: 0.5}` and `isPrecise: false` so tldraw auto-routes to the nearest edge midpoint.

---

## Design Process

### Step 0: Assess Depth
Simple/conceptual, or comprehensive/technical? Research actual specs for the latter.

### Step 1: Understand Deeply
For each concept: what does it DO? What connects to what? What would someone need to SEE?

### Step 2: Map to Patterns
Each major concept → a different visual pattern (fan-out, timeline, cycle, etc.). No uniform grids.

### Step 3: Sketch the Flow
Mentally trace how the eye moves. There should be a clear visual story.

### Step 4: Generate Output
- **Mode A (`.tldr`)**: Build the JSON from `references/json-schema.md` + `references/shape-templates.md`. For large diagrams, build one section at a time — see below.
- **Mode B (SDK)**: Write `editor.createShapes([...])` calls using the templates.

### Step 5: Render & Validate
See **Render & Validate** below.

---

## Large Diagram Strategy (`.tldr` Mode)

For comprehensive diagrams, **build the records array one section at a time.** A full file easily exceeds token limits in one pass.

1. Create the base file with `tldrawFileFormatVersion`, `schema`, and the required `document` + `page` records.
2. Add shapes section by section. Use readable string IDs like `shape:trigger_rect`, `shape:arrow_fan_left`.
3. Namespace IDs by section prefix to avoid collisions.
4. Update `bindings` records as you add arrows that connect shapes across sections.
5. After all sections are in place, read through and verify every `fromId`/`toId` in bindings references a real shape.

---

## Render & Validate (MANDATORY)

You cannot judge a diagram from JSON alone. After generating or editing a `.tldr`, render it to PNG, view the image, and fix what you see — in a loop until it's right.

### How to Render

```bash
cd references && uv run python render_tldraw.py <path-to-file.tldr>
```

This writes a PNG next to the `.tldr` file. Then use the **Read tool** on the PNG to view it.

The renderer works by launching headless Chromium, loading `render_template.html` (which imports tldraw from esm.sh), calling `editor.createShapes` + `editor.createBindings` with the records from your file, and exporting to PNG via tldraw's `exportToBlob`. It needs network access on first run to fetch tldraw from esm.sh.

### The Loop

**1. Render & View** — Run the script, then Read the PNG.

**2. Audit against your original vision** — Does the visual structure match the plan? Does the eye flow where you intended? Do hero elements dominate?

**3. Check for visual defects**:
- Text clipped or overflowing a geo's bounds
- Arrows missing their target shapes (binding ids wrong, or `parentId` mismatch)
- Shapes overlapping unintentionally
- Frames not grouping what you expected
- Color semantics unclear (errors don't look urgent, AI doesn't look distinct)

**4. Fix** — Edit the JSON. Common fixes:
- Increase `w`/`h` on a `geo` when text is clipped
- Adjust `x`/`y` to fix spacing
- Recheck `fromId`/`toId` in bindings — they must reference real shape ids
- Remap `parentId: "page:page"` if you renamed the page

**5. Re-render & re-view** — Typically 2–4 iterations.

### Alternative: User opens in the tldraw web app
If the headless renderer can't reach esm.sh (offline, restricted network), fall back to: *"Open [tldraw.com](https://tldraw.com) → File → Open → pick the `.tldr` file."*

### Version Compatibility
The local renderer uses tldraw v3 (via esm.sh), while tldraw.com runs v4+. The renderer's `__renderTldr` function automatically converts v4 props (arrow `richText` → `text`, strips `textFirstEditedBy` from notes, strips `snap` from bindings) so files authored for tldraw.com also render locally. **Always author files using the current tldraw.com format** (described in `references/json-schema.md`). The renderer handles backward compat automatically.

### Shape Prop Validation Gotchas
If the renderer errors with `ValidationError: At shape(type = X).props.Y: Unexpected property`, you used a prop that doesn't exist on that shape. To inspect real defaults for any shape, run this one-liner against the rendered harness:

```bash
cd references && uv run python -c "
from playwright.sync_api import sync_playwright
import pathlib, json
with sync_playwright() as p:
    b = p.chromium.launch(headless=True); page = b.new_context().new_page()
    page.goto('file://' + str(pathlib.Path('render_template.html').resolve()))
    page.wait_for_function('window.__editorReady === true')
    print(json.dumps(page.evaluate(\"() => window.__editor.getShapeUtil('arrow').getDefaultProps()\"), indent=2))
    b.close()
"
```

Replace `'arrow'` with the shape type you need defaults for.

### First-Time Setup
```bash
cd references
uv sync
uv run playwright install chromium
```

---

## Quality Checklist

### Depth & Evidence
1. Research done for technical content?
2. Evidence artifacts (real code/JSON in `note` shapes)?
3. Multi-zoom: overview + sections + details?

### Conceptual
4. Isomorphism: structure mirrors concept?
5. Each major concept uses a different pattern?
6. No uniform card grids?

### Container Discipline
7. Free-floating `text` used for labels (not every text in a geo)?
8. `frame` used for grouping (not manual background rectangles)?
9. `note` used for evidence artifacts?

### tldraw-Specific
10. All colors from `references/color-palette.md` (no custom hex)?
11. `font`, `dash`, `fill` consistent with the diagram's tone?
12. Arrow bindings connect to real shape IDs?
13. Frame `name` props set for grouped sections?

### Structural
14. Every relationship has an arrow
15. Clear flow direction (left→right, top→bottom, or radial)
16. Hero elements larger and more isolated

### Technical
17. `.tldr` file has `tldrawFileFormatVersion`, valid `schema`, and `records` array
18. Exactly one `document` record and at least one `page` record
19. Shape `parentId` points to a valid page or frame
20. Every binding references existing shape IDs
