# `.tldr` File Format Reference

A `.tldr` file is a JSON document containing a `tldrawFileFormatVersion`, a `schema` describing the data shape, and a `records` array that is the actual document.

> **Heads up**: tldraw's schema evolves. When the user opens an older `.tldr` in a newer tldraw version, migrations run automatically. If you hand-author a file and unusual props get dropped on import, update the record to match the current shape prop list in `shape-templates.md`.

---

## Top-Level Structure

```json
{
  "tldrawFileFormatVersion": 1,
  "schema": {
    "schemaVersion": 2,
    "sequences": {
      "com.tldraw.store": 5,
      "com.tldraw.asset": 1,
      "com.tldraw.camera": 1,
      "com.tldraw.document": 2,
      "com.tldraw.instance": 26,
      "com.tldraw.instance_page_state": 5,
      "com.tldraw.page": 1,
      "com.tldraw.instance_presence": 6,
      "com.tldraw.pointer": 1,
      "com.tldraw.shape": 4,
      "com.tldraw.user": 1,
      "com.tldraw.asset.image": 6,
      "com.tldraw.asset.video": 5,
      "com.tldraw.asset.bookmark": 2,
      "com.tldraw.shape.group": 0,
      "com.tldraw.shape.text": 4,
      "com.tldraw.shape.bookmark": 2,
      "com.tldraw.shape.draw": 4,
      "com.tldraw.shape.geo": 11,
      "com.tldraw.shape.note": 12,
      "com.tldraw.shape.line": 5,
      "com.tldraw.shape.frame": 1,
      "com.tldraw.shape.arrow": 8,
      "com.tldraw.shape.highlight": 3,
      "com.tldraw.shape.embed": 4,
      "com.tldraw.shape.image": 5,
      "com.tldraw.shape.video": 4,
      "com.tldraw.binding.arrow": 1
    }
  },
  "records": [
    { /* document */ },
    { /* page */ },
    { /* shapes */ },
    { /* bindings */ }
  ]
}
```

---

## Required Records

Every `.tldr` file needs at least a document and a page.

### Document

```json
{
  "id": "document:document",
  "typeName": "document",
  "gridSize": 10,
  "name": "",
  "meta": {}
}
```

Exactly one `document` record per file. `id` is always `"document:document"`.

### Page

```json
{
  "id": "page:page",
  "typeName": "page",
  "name": "Page 1",
  "index": "a1",
  "meta": {}
}
```

At least one `page` record. `index` is a fractional index key (`"a1"`, `"a2"`, … — use `"a1"` for a single-page doc); the same rules as for shapes apply, see below. Shape `parentId`s point at this page's `id`.

---

## Shape Record Shape

Every shape record shares this outer structure. Only `props` differs per shape type.

```json
{
  "id": "shape:<unique-id>",
  "typeName": "shape",
  "type": "geo",
  "x": 100,
  "y": 100,
  "rotation": 0,
  "index": "a1",
  "parentId": "page:page",
  "isLocked": false,
  "opacity": 1,
  "meta": {},
  "props": { /* type-specific, see shape-templates.md */ }
}
```

Field notes:
- **`id`**: `"shape:"` prefix required. Use descriptive suffixes: `shape:trigger_rect`, `shape:arrow_main`. Must be unique across the file.
- **`type`**: one of `geo`, `text`, `note`, `arrow`, `line`, `draw`, `frame`, `group`, `image`, `video`, `bookmark`, `embed`, `highlight`.
- **`x` / `y`**: top-left position in the page's coordinate system. Units = px.
- **`rotation`**: radians. Leave `0` unless you mean it.
- **`index`**: fractional index key for z-order within the parent — **not a counter**.
  Valid keys run `a1`…`a9`, then `aA`…`aZ`, then `aa`…`az` (base62 after the leading `a`),
  giving 61 slots per parent; beyond that go two digits (`b10`, `b11`, …). A fractional part
  must **never end in `0`**, so naive numbering breaks at the tenth shape: tldraw rejects
  `a10` with `At shape(type = geo).index: Expected an index key, got "a10"`, and a single bad
  record aborts the entire import — the user sees an empty document, no error. The local PNG
  renderer does not check this, so a perfect render proves nothing here. Generate keys like:

  ```python
  B62 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
  def index_key(n):        # n starts at 1, one counter per parentId
      return "a" + B62[n]  # a1, a2, ... a9, aA, aB, ... aZ, aa, ... az
  ```
- **`parentId`**: usually the page id (`"page:page"`). For a shape inside a frame, use the frame's `id`.
- **`props`**: shape-specific — see `shape-templates.md`.

---

## Arrow Bindings

An `arrow` shape's `start` / `end` props carry coordinates. To make an arrow **stick** to another shape (so it moves with it), add a `binding` record.

### Arrow shape

```json
{
  "id": "shape:arrow_main",
  "typeName": "shape",
  "type": "arrow",
  "x": 0,
  "y": 0,
  "rotation": 0,
  "index": "aA",
  "parentId": "page:page",
  "isLocked": false,
  "opacity": 1,
  "meta": {},
  "props": {
    "kind": "elbow",
    "elbowMidPoint": 0.5,
    "dash": "solid",
    "size": "m",
    "fill": "none",
    "color": "black",
    "labelColor": "black",
    "bend": 0,
    "start": { "x": 0, "y": 0 },
    "end": { "x": 200, "y": 0 },
    "arrowheadStart": "none",
    "arrowheadEnd": "arrow",
    "font": "sans",
    "richText": {
      "type": "doc",
      "content": [{ "type": "paragraph" }]
    },
    "labelPosition": 0.5,
    "scale": 1
  }
}
```

> **Note**: Since tldraw.com v4, arrow shapes use `richText` (ProseMirror format) for labels, just like geo/text/note shapes. For an arrow with a label, use `{"type": "paragraph", "content": [{"type": "text", "text": "Label"}]}`. For no label, use `{"type": "paragraph"}` (empty paragraph).

### Binding records (one per bound end)

```json
{
  "id": "binding:arrow_main_start",
  "typeName": "binding",
  "type": "arrow",
  "fromId": "shape:arrow_main",
  "toId": "shape:source_rect",
  "props": {
    "terminal": "start",
    "normalizedAnchor": { "x": 0.5, "y": 0.5 },
    "isExact": false,
    "isPrecise": false,
    "snap": "none"
  },
  "meta": {}
},
{
  "id": "binding:arrow_main_end",
  "typeName": "binding",
  "type": "arrow",
  "fromId": "shape:arrow_main",
  "toId": "shape:target_rect",
  "props": {
    "terminal": "end",
    "normalizedAnchor": { "x": 0.5, "y": 0.5 },
    "isExact": false,
    "isPrecise": false,
    "snap": "none"
  },
  "meta": {}
}
```

- `fromId` is the arrow's id, `toId` is the shape it binds to.
- `terminal` is `"start"` or `"end"`.
- `normalizedAnchor` is `{x: 0..1, y: 0..1}` inside the target shape's bounding box. `{0.5, 0.5}` = center.
- `isPrecise: false` lets tldraw auto-route to the nearest edge — usually what you want.

Arrows without bindings are fine too (floating arrows). Add bindings only when the arrow should follow a shape.

---

## Rich Text (`richText`)

Shapes that carry text (`geo`, `note`, `text`, `arrow` label) use ProseMirror-style rich text, not plain strings:

```json
"richText": {
  "type": "doc",
  "content": [
    {
      "type": "paragraph",
      "content": [
        { "type": "text", "text": "Your label here" }
      ]
    }
  ]
}
```

For an empty label use `{"type": "doc", "content": [{"type": "paragraph"}]}`.

For multiple lines, use multiple `paragraph` entries in `content`.

---

## Minimal Example

A page with two rectangles connected by an arrow:

```json
{
  "tldrawFileFormatVersion": 1,
  "schema": {
    "schemaVersion": 2,
    "sequences": {
      "com.tldraw.store": 5,
      "com.tldraw.asset": 1,
      "com.tldraw.camera": 1,
      "com.tldraw.document": 2,
      "com.tldraw.instance": 26,
      "com.tldraw.instance_page_state": 5,
      "com.tldraw.page": 1,
      "com.tldraw.instance_presence": 6,
      "com.tldraw.pointer": 1,
      "com.tldraw.shape": 4,
      "com.tldraw.user": 1,
      "com.tldraw.asset.image": 6,
      "com.tldraw.asset.video": 5,
      "com.tldraw.asset.bookmark": 2,
      "com.tldraw.shape.group": 0,
      "com.tldraw.shape.text": 4,
      "com.tldraw.shape.bookmark": 2,
      "com.tldraw.shape.draw": 4,
      "com.tldraw.shape.geo": 11,
      "com.tldraw.shape.note": 12,
      "com.tldraw.shape.line": 5,
      "com.tldraw.shape.frame": 1,
      "com.tldraw.shape.arrow": 8,
      "com.tldraw.shape.highlight": 3,
      "com.tldraw.shape.embed": 4,
      "com.tldraw.shape.image": 5,
      "com.tldraw.shape.video": 4,
      "com.tldraw.binding.arrow": 1
    }
  },
  "records": [
    {
      "id": "document:document",
      "typeName": "document",
      "gridSize": 10,
      "name": "",
      "meta": {}
    },
    {
      "id": "page:page",
      "typeName": "page",
      "name": "Page 1",
      "index": "a1",
      "meta": {}
    },
    {
      "id": "shape:a",
      "typeName": "shape",
      "type": "geo",
      "x": 100,
      "y": 100,
      "rotation": 0,
      "index": "a1",
      "parentId": "page:page",
      "isLocked": false,
      "opacity": 1,
      "meta": {},
      "props": {
        "geo": "rectangle",
        "w": 200,
        "h": 100,
        "color": "blue",
        "labelColor": "black",
        "fill": "solid",
        "dash": "solid",
        "size": "m",
        "font": "sans",
        "align": "middle",
        "verticalAlign": "middle",
        "growY": 0,
        "url": "",
        "scale": 1,
        "richText": {
          "type": "doc",
          "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Start" }] }]
        }
      }
    },
    {
      "id": "shape:b",
      "typeName": "shape",
      "type": "geo",
      "x": 500,
      "y": 100,
      "rotation": 0,
      "index": "a2",
      "parentId": "page:page",
      "isLocked": false,
      "opacity": 1,
      "meta": {},
      "props": {
        "geo": "rectangle",
        "w": 200,
        "h": 100,
        "color": "green",
        "labelColor": "black",
        "fill": "solid",
        "dash": "solid",
        "size": "m",
        "font": "sans",
        "align": "middle",
        "verticalAlign": "middle",
        "growY": 0,
        "url": "",
        "scale": 1,
        "richText": {
          "type": "doc",
          "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "End" }] }]
        }
      }
    },
    {
      "id": "shape:arrow1",
      "typeName": "shape",
      "type": "arrow",
      "x": 0,
      "y": 0,
      "rotation": 0,
      "index": "a3",
      "parentId": "page:page",
      "isLocked": false,
      "opacity": 1,
      "meta": {},
      "props": {
        "kind": "elbow",
        "elbowMidPoint": 0.5,
        "dash": "solid",
        "size": "m",
        "fill": "none",
        "color": "black",
        "labelColor": "black",
        "bend": 0,
        "start": { "x": 0, "y": 0 },
        "end": { "x": 0, "y": 0 },
        "arrowheadStart": "none",
        "arrowheadEnd": "arrow",
        "font": "sans",
        "richText": {
          "type": "doc",
          "content": [{ "type": "paragraph" }]
        },
        "labelPosition": 0.5,
        "scale": 1
      }
    },
    {
      "id": "binding:arrow1_start",
      "typeName": "binding",
      "type": "arrow",
      "fromId": "shape:arrow1",
      "toId": "shape:a",
      "props": {
        "terminal": "start",
        "normalizedAnchor": { "x": 0.5, "y": 0.5 },
        "isExact": false,
        "isPrecise": false,
        "snap": "none"
      },
      "meta": {}
    },
    {
      "id": "binding:arrow1_end",
      "typeName": "binding",
      "type": "arrow",
      "fromId": "shape:arrow1",
      "toId": "shape:b",
      "props": {
        "terminal": "end",
        "normalizedAnchor": { "x": 0.5, "y": 0.5 },
        "isExact": false,
        "isPrecise": false,
        "snap": "none"
      },
      "meta": {}
    }
  ]
}
```

Save this as `example.tldr`, then open via File → Open in [tldraw.com](https://tldraw.com).
