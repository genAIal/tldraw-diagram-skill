# tldraw Color Palette (Semantic Mapping)

tldraw uses a **fixed, named palette**. You cannot set custom hex colors on built-in shapes — only these tokens are valid on the `color` / `labelColor` props:

```
black   grey
blue    light-blue
green   light-green
red     light-red
violet  light-violet
orange  yellow
```

This file maps each semantic purpose to a tldraw color token. Use it as the single source of truth.

---

## Semantic Mapping

| Purpose | `color` token | When to use |
|---------|---------------|-------------|
| **Neutral / structural** | `black` | Default for text, borders, generic shapes |
| **Weak / supporting** | `grey` | Secondary text, subdued shapes, dividers |
| **Primary action / main flow** | `blue` | The spine of the diagram — main process, primary pipeline |
| **Secondary flow** | `light-blue` | Alternate path, parallel flow |
| **Success / output / positive** | `green` | Success state, result, "happy path" terminus |
| **Intermediate / ready** | `light-green` | Staging, pending-success, "ready to go" |
| **Error / blocker** | `red` | Failure, error state, hard stop |
| **Warning / at-risk** | `light-red` | Degraded state, soft failure |
| **Caution / transition** | `orange` | Mid-state, in-progress, needs attention |
| **AI / ML / abstract** | `violet` | AI agents, model inference, abstract/conceptual nodes |
| **AI supporting** | `light-violet` | AI-adjacent nodes, prompts, context |
| **Evidence / callout** | `yellow` | `note` (sticky) shapes — code snippets, JSON samples, quotes |

---

## Fill Tokens

`fill` is separate from `color`. Valid values: `none`, `semi`, `solid`, `pattern`, `fill`.

| Fill | When to use |
|------|-------------|
| `solid` | Default — gives shapes visible colored backgrounds. Readable and professional. |
| `semi` | Subtle emphasis. Secondary shapes that shouldn't dominate. |
| `none` | Outline only. Use sparingly — shapes without fills look like wireframes. |
| `pattern` | Texture — useful for "external system" or "not-yet-implemented" shapes. |

**Rule**: Default to `fill: solid` for all primary shapes. Use `semi` for secondary emphasis, `none` only when you deliberately want an outline-only look.

---

## Dash Tokens

`dash` controls stroke style. Valid values: `draw`, `solid`, `dashed`, `dotted`.

| Dash | When to use |
|------|-------------|
| `draw` | Hand-drawn look. Default only if the user wants tldraw's classic sketchy style. |
| `solid` | Clean, technical. Default for architecture / system diagrams. |
| `dashed` | Hypothetical, planned, future state |
| `dotted` | Weak connection, optional flow |

---

## Font Tokens

`font` values: `draw`, `sans`, `serif`, `mono`.

| Font | When to use |
|------|-------------|
| `draw` | Classic tldraw hand-drawn. Informal/brainstorm. |
| `sans` | Technical / professional diagrams. Default for architecture. |
| `serif` | Formal / editorial tone |
| `mono` | Code, JSON, terminal output — always use this inside `note` evidence shapes |

---

## Size Tokens

`size` values: `s`, `m`, `l`, `xl`.

| Size | Use for |
|------|---------|
| `s` | Dense labels, compact annotations |
| `m` | Default shape/text size |
| `l` | Section headings, primary nodes |
| `xl` | Hero / title text only |

---

## Quick Reference — Common Combinations

```
Primary process node:     color=blue,   fill=solid, dash=solid, size=m, font=sans
Hero / main concept:      color=blue,   fill=solid, dash=solid, size=l, font=sans
Success terminus:         color=green,  fill=solid, dash=solid, size=m, font=sans
Error state:              color=red,    fill=solid, dash=solid, size=m, font=sans
AI / agent node:          color=violet, fill=solid, dash=solid, size=m, font=sans
Evidence (note):          color=yellow, font=mono, size=s
Hypothetical / future:    color=grey,   dash=dashed
Section label (text):     color=black,  size=l,    font=sans
Subdued label (text):     color=grey,   size=s,    font=sans
```
