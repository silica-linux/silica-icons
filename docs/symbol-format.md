# Symbol format

Version 1. Applies to `symbols/`: the monochrome system glyphs (menu bar, Control Center,
menus, toolbars, settings). App and file icons follow
[`icon-format.md`](icon-format.md).

Design source: `design/symbols.sketch` (pages Grid, Symbols, Weights, Check, Sheet, Styles), a copy of
the Sketch library "Silica 1.0 Amalfi Icon Kit". Every symbol is a Sketch symbol master `<Weight> / <name>`
(Light, Regular, Semibold) at 24 × 24 pt. Layers scale with the instance; stroke thickness comes from shared
layer styles `<Weight>/<Size>/<Role>` (sizes 12–32, roles Stroke, Fill, Fill Stroke and their Secondary
forms), so an instance resized to N pt takes the `<Weight>/<N>/…` styles as overrides.

## Canvas and units

| Element | Measure |
| --- | --- |
| Canvas | 24 × 24 u, drawn at 4× on a 96 × 96 px artboard (1 u = 4 px) |
| Live area | 20 × 20 u, 2 u margin; no ink outside, except terminals of 0.5 u at most |
| Center | (12, 12) = center of Inter's capital letters |
| Circle keyline | Ø 20 (outer ink) |
| Square keyline | 18 × 18 (≈ Ø 20 × √π/2: same area as the circle, optical correction) |
| Wide keyline | 20 × 12.36 (1 : φ) |
| Tall keyline | 12.36 × 20 (φ : 1) |

Keylines are measured on the outer edge of the ink, not on the stroke axis: a Regular circle
on the Ø 20 keyline has a path with radius 9.25 (10 − 0.75).

## Proportion system (φ = 1.618)

All measures derive from two quantities: the live area (20 u) and the Regular stroke (1.5 u).

| Quantity | Value | Where it is used |
| --- | --- | --- |
| Golden circles | Ø 20 · 12.36 · 7.64 · 4.72 (20 / φⁿ) | lens of `search` (Ø 12.36), rings of `share-nearby` (Ø 12.36), core of `sun` and head of `person` (≈ Ø 7.64), hole of `gear` |
| Golden rectangle | 1 : φ | `keyboard`, `sidebar`, `battery` (body 18 × 11.12), `lock` (body), `folder` (≈), `doc` (≈ φ : 1) |
| Golden section | 1/φ² and 1/φ of the width | divider of `sidebar` (1/φ²), fold of `doc` (width / φ² + 1) |
| Concentric step | stroke × φ² = 3.93 u (axis to axis) | arcs of `wifi`, waves of `volume`, waves of `hotspot` |
| Gap between strokes | stroke × φ = 2.43 u | consequence of the step: free space between two parallel strokes |
| Levels | 1 · 1/φ · 1/φ³ | fill of `battery`, `battery-50`, `battery-10` |
| Pentagram | inner radius = outer / φ² | `star` (holds for any regular 5-point star) |
| Clock hands | radius / φ (minutes), radius / φ² (hours) | `clock` |
| Scales | ratio √φ = 1.272 | small, medium, large |
| Weights | ×φ^½ and ×φ^¾ from Regular | Light, Semibold |

Useful coincidence: Inter's cap height (0.7275 em) equals 12.36 u at the medium scale. The
wide golden rectangle 20 × 12.36 therefore matches the band between cap height and baseline:
a wide symbol (keyboard, sidebar) has the same height as the capital letters of the text next
to it.

### Optical corrections to the pure ratio

| Symbol | Pure ratio | Chosen | Reason |
| --- | --- | --- | --- |
| Square | 20 | 18 | same area as the Ø 20 circle, otherwise the square looks heavier |
| `wifi`, `volume` | radii in φ progression (r, rφ, rφ²) | constant step 3.93 u (= stroke × φ²) | with radii in φ progression the gap between the first and second arc drops below 1 u and closes in Semibold |
| `sun` | core Ø 7.64 | Ø 8.04 (+0.4) | the short rays lighten the drawing; the core grows to compensate |
| `gear` | hole Ø 7.64 | axis Ø 7.24 (−0.4) | the inner ring at Ø 7.64 came too close to the tooth roots |
| `doc` | 12.36 × 20 | 13.96 × 20 | the narrow sheet looks smaller than the other tall symbols |
| `folder` | 20 × 12.36 | 20 × 12.93 | the tab takes weight away from the body; the body grows by 0.6 u |
| `star` | center (12, 12) | center (12, 12.85) | optical centering: the star has more mass at the bottom |
| `play` | centered box (x 6.5–17.5) | centroid near the center (x 8–19, centroid 11.67) | centered on the box, the triangle looks shifted to the left |
| `share-nearby` | — | two Ø 12.36 circles with centers at ±3.82 | envelope exactly Ø 20 |

## Weights

Stroke centered on the path, round terminals and joins (terminal radius = half the stroke).

| Weight | Stroke (u) | em at medium scale | Matching Inter stem |
| --- | --- | --- | --- |
| Light | 1.18 (1.5 / φ^½) | 0.069 | to be verified when the package includes Inter Light |
| Regular | 1.5 | 0.088 | Inter Regular "l" 0.088 |
| Semibold | 2.15 (1.5 × φ^¾) | 0.127 | Inter SemiBold "l" 0.127 |

On the icon stroke scale (`icon-format.md`, 1 u = 30 px: 45 × √φⁿ) Light is 35 and Regular
45; Semibold (64.6) falls between 57 and 73 because it follows the stem of Inter SemiBold, not
the √φ series.

The drawing is the same in all three weights: only the stroke changes. Bar and badge cuts are
recomputed per weight so that the gap stays 1.5 u (axis to axis = stroke + 1.5: Light 2.68,
Regular 3, Semibold 3.65); for this reason, in Semibold the pieces that sit entirely within
the bar band disappear (the pupil of `eye-slash`). In `symbols.py` the weight is chosen with
`SILICA_SYMBOL_WEIGHT` (`light`, `regular`, `semibold`; stroke in `WSW`).

A symbol has the same weight as the text next to it: a Regular symbol goes with Inter
Regular, a Semibold one with Inter SemiBold. Other weights (Thin, Medium, Bold) are added
with the same criterion: stroke = Inter stem of that weight, converted to medium-canvas units.

Filled shapes (`play`, `pause`, `moon`, `airplane`, dots) have fill **and** stroke of the
same color: they grow with the weight like lines and have their corners rounded by the stroke.
Inner fills that must not grow (battery level, bolt) are fill only.

## Scales

Three scales with ratio √φ. The canvas is measured in em of the text next to it:

| Scale | Canvas | At 13 pt | Square keyline at 13 pt | Use |
| --- | --- | --- | --- | --- |
| small | 1.111 em | 14.4 pt | 10.8 pt | menu items with icon, shortcuts, small labels |
| medium | 1.4126 em | 18.4 pt | 13.8 pt | menu bar, menus, toolbars |
| large | 1.797 em | 23.4 pt | 17.5 pt | Control Center (36 pt discs), large buttons |

The stroke in points stays that of the weight at every scale: in small-canvas units = stroke
× √φ, large = stroke / √φ (Regular: small 1.91 u, medium 1.5 u, large 1.18 u). Whoever exports
a scale other than medium recomputes the stroke instead of scaling it with the drawing.

Check against the reference measurements (notes in `silica/plan/reference/`): at the large
scale at 13 pt `wifi` measures 19.9 × 15.5 pt (observed Control Center: 20 × 15); at the
medium scale the menu bar icons are between 12 and 16 pt tall (observed: 12–18).

## Alignment to text

- The canvas center sits on the center of the capital letters: baseline + 0.3638 em.
- At the medium scale: cap height at y 5.82 u, baseline at y 18.18 u.
- The symbol is positioned like a glyph: `y_canvas = baseline − 0.3638 em − canvas / 2`.
- Horizontal spacing between symbol and text: decided by the component, not the symbol (the
  canvas already has a 2 u margin).

## Color

- Monochrome: a single color, taken from the theme (`currentColor` in the SVGs). Never fixed
  colors in the symbol.
- Secondary parts (inactive arcs of `wifi-1`, waves of `volume-1`): layer named
  `secondary`, opacity 35 % of the symbol color. The shell may replace it with a secondary
  theme color.
- No shadow, gradient or glass in the symbol: the context adds them (Control Center disc,
  button).

## Outline and fill variants

- The base shape is **outline** (stroke). The name without suffix is the outline: `bell`,
  `folder`.
- The filled variant has the suffix `-fill`: `bell-fill`, `folder-fill`, `heart-fill`. It is
  drawn for symbols that become "active" or selected (sidebars, tab bars, favorites). They
  exist for `location`, `mic`, `bolt`, `house`, `house-door`, `folder`, `doc`, `photo`, `bookmark`,
  `trash`, `bell`, `message`, `phone`, `video`, `paperplane`, `megaphone`, `person`, `lock`,
  `shield`, `cloud`, `drop`, `umbrella`, `circle`, `square`, `triangle`, `diamond`, `star`,
  `heart`, `flag`, `lightbulb`, `puzzle`, `leaf`, `pointer`, `circle-stack`,
  `books-vertical`. In the fill variant the inner detail
  is cut out (subtraction), with a minimum gap of 1.5 u.
- Inherently filled symbols (`play`, `pause`, `moon`, `airplane`) have no outline variant.
- Until Sketch preserves subtractions between subpaths, `-fill` is drawn only for shapes
  with no inner detail to cut out, or with the detail omitted (`folder-fill` without
  divider, `doc-fill` without fold, `house-fill` without door, `leaf-fill` without vein); open
  parts (handle of `umbrella`, base of `lightbulb`, clapper of `bell`) remain strokes. There
  are still no `envelope-fill`, `tag-fill`, `checkmark-circle-fill`, `gear-fill`, `camera-fill`,
  `eye-fill` (the inner detail is the symbol).

## Names

- English kebab-case, from general to specific: `chevron-left`, `lock-open`,
  `battery-charging`.
- Variants as a suffix, in this order: state or level, then `-fill`.
  - levels: `wifi-0`, `wifi-1`, `wifi-2`, `wifi` (full); `volume-1`, `volume-2`, `volume`;
    `battery-10`, `battery-50`, `battery` (charge).
  - slashed or disabled: `-slash` (`wifi-slash`, `volume-slash`, `bell-slash`).
  - states: `-open`, `-charging`; fill: `-fill`.
- Names that describe the shape or the system function, never Apple product names:
  `share-nearby` (not "airdrop"), `screen-cast` (not "airplay"), `airplane` for airplane
  mode, `moon` for focus.

## Drawing rules

1. Start from the right keyline (circle, square, wide, tall) and from the golden quantities in
   the table; document every optical correction on the Check page.
2. One stroke width per symbol; no halved strokes for details.
3. Minimum gap between strokes: 1.5 u in Regular (stays ≥ 1.2 u in Semibold).
4. Round terminals; inner corners of containers r 2.4 u (≈ stroke × φ), capsules with
   radius = half the height.
5. Coordinates preferably on multiples of 0.25 u for horizontal and vertical strokes
   (at 1× medium 1 u ≈ 0.77 px: no pixel alignment is possible, consistency is what counts).
6. Every subpath is a separate layer (`primary` or `secondary`), so Sketch does not merge
   or subtract the paths.
7. Before closing: Check (overlaid grid), Weights (three weights and three scales), check
   sheet at 1× and 2× on light and dark next to Inter.

## Files in the repository

```
symbols/<weight>/<name>.svg   weight light, regular, semibold; viewBox 0 0 24 24, stroke of the weight
                              (1.18 · 1.5 · 2.15), stroke-linecap/linejoin round,
                              color currentColor, secondary layers with opacity 0.35
```

The paths are described in `tools/symbols/symbols.py` (single source for Sketch and for the
SVGs). `tools/symbols/export_svg.py` writes the three weights to `symbols/<weight>/*.svg`; with
`--check` it verifies that the files match the source. `tools/symbols/gen2.py` generates the
scripts that create the artboards in `design/symbols.sketch`; `compose_sheet.py` recomposes
the check sheet of the Sheet page from the PNGs exported by Sketch; `sheet.py sheet.png 48
semibold` renders the sheet of one weight. In `design/symbols.sketch` the symbols are drawn in
Regular.

## Views and stacks

File manager toolbar symbols (phase 4 in `symbols.py`, after the categories). The icon and
list views are `square-grid-2x2` and `list-bullet`; sidebar and right panel are `sidebar` and
`sidebar-right`.

- `window-split-3` (column view): WN container of `window-split` divided into three equal
  columns.
- `gallery` (gallery view): 18.5 × 9.5 r 2.4 frame and a row of three filled thumbnails
  (fill and stroke, like the small window of `pip`) as wide as the frame; gap 2 u in
  Regular, 1.35 in Semibold.
- `square-stack` (group): three r 2.4 squares offset by 3.35 u toward the top right, ink
  within the square keyline; of the squares behind only the uncovered sides remain, like
  `window-stack`.
- `circle-stack` (tag): three r 4.25 circles in a row, the left one in front; the others
  break where the axis is less than stroke + gap from the front circle (recomputed per
  weight, like the bar cuts). `circle-stack-fill`: filled discs, the ones behind become
  crescents with the same gap.

## File manager sidebar

Symbols for the sidebar rows (phase 5 in `symbols.py`, after the categories).

- `desktop` (Desktop): screen without a stand, 18.5 × 13 r 2.4 rectangle (20 × 14.5 ink,
  centered) with a filled band at the bottom 3 u tall on the axis, the bar of `menubar`
  flipped. `display` remains the monitor with the stand.
- `photo-fill` (Pictures): outlined frame of `photo`, filled sun and hills (fill and
  stroke). The hills follow the ridges of `photo` and go down to the bottom of the frame; the
  detail is not cut out, it is filled.
- `house-door`: roof, walls and door of `house` (same proportion, swapped), with the door
  filled and a filled chimney on the right slope (x 14.75–17, top at y 4.5, base on the slope).
  `house-door-fill`: filled body with the door as a notch in the bottom outline (no
  subtraction: the door touches the edge), filled chimney; the door stays open 2.5 u in Regular.

## Library

Symbol of the Library folder (`LIBRARY` of the generic folder; phase 6 in `symbols.py`, after
the categories).

- `books-vertical`: two upright books and a tilted one on a shelf (line from x 2.75 to 21.25
  on y 20.25). The upright books are 4 and 3.5 u wide on the axis, 15.5 and 13 u tall, r 1,
  open at the bottom on the shelf; 3.35 u axis to axis between them (gap 1.85 in Regular, 1.2
  in Semibold). The third (3 × 12, r 1) is tilted by 18°, rests on the bottom left corner and
  touches the side of the second; the first has two bands on the spine (y 8.25 and 16.75).
  Ink from x 2.6 to 21.5.
- `books-vertical-fill`: filled books (fill and stroke), stroked shelf, bands omitted.

## Slashed variants and badges

- `-slash`: bar from (4.25, 4.25) to (19.75, 19.75), above the symbol, always the same
  straight 45° stroke with round terminals. Strokes under the bar break where the axis is
  less than 3 u from the bar axis (0.75 + gap 1.5 + 0.75): the minimum gap also applies to
  crossings. Filled shapes are cut the same way (`slashed_fill`: the cut outline stays 3 u
  from the bar axis), like the speaker of `volume-slash`.
- Badge (`bell-badge`): filled disc; the stroke underneath breaks with the same gap.
- The cuts are computed in `symbols.py` (functions `cut`, `slashed`, `outside_shape`), never
  by hand.

## Font

The three weights are also built as an icon font, so the same glyphs work in Sketch (installed
font) and in Flutter (`IconData`). The font is derived from `symbols/` and has the same licence
(CC BY-SA 4.0); it contains no third-party glyphs.

```
fonts/SilicaSymbols-Light.otf     weight 300    (+ .woff2)
fonts/SilicaSymbols-Regular.otf   weight 400    (+ .woff2)
fonts/SilicaSymbols-Semibold.otf  weight 600    (+ .woff2)
fonts/codepoints.json             name -> hex codepoint, stable
fonts/flutter/silica_symbols.dart generated IconData constants
fonts/build-report.json           dropped secondary layers, weight compatibility
```

Family "Silica Symbols" (name IDs 16/17 group the three weights in Sketch and macOS; IDs 1/2
give Light and Semibold their own legacy family names).

### Build

```
tools/symbols-font/build.sh                   # venv in tools/symbols-font/.venv, deps pinned in requirements.txt
tools/symbols-font/build.sh --verify OUTDIR   # also renders every glyph against the SVG (resvg)
```

`build.py` outlines every stroke with Skia (`skia-pathops`: round caps and joins, as in the
SVGs), keeps fills, unions all layers of a symbol and removes overlaps (nonzero winding), and
writes CFF OpenType. `verify.py` renders each glyph with FreeType and the SVG with resvg at 24
and 96 px, lists glyphs whose alpha differs by more than 50 % on more than 0.4 % of the pixels,
checks that every name shapes to its own glyph, and writes contact sheets.

### Metrics

- 1 em = the 24 u canvas (units per em 2400, 100 per u). Font size N pt draws the symbol box of
  N pt, including its 2 u margin. Advance width = 1 em.
- Ascender = 2400, descender = 0, line gap 0 (hhea, OS/2 typo and win): the baseline is the
  bottom edge of the canvas and the line box is exactly the canvas. To centre a symbol in a
  box, centre a line box of height 1 em (Flutter `Icon` does this).
- To align with text instead, use the rule in "Alignment to text": canvas centre = baseline +
  0.3638 em of the text next to it.

### Secondary layers

A font cannot carry opacity. Layers with `opacity="0.35"` are dropped from the glyph:
`wifi-1`, `wifi-2`, `signal-1`, `signal-2`, `signal-3`, `volume-0`, `volume-1`, `volume-2` and
`progress` show only their active part. Symbols made only of secondary layers (`wifi-0`) keep
them at full ink, otherwise the glyph would be empty. Use the SVGs when the faded ghost is needed.

### Codepoints

BMP Private Use Area from U+E000, assigned in name order the first time and then never changed:
`build.py` reads `fonts/codepoints.json`, keeps existing assignments and appends new names after
the highest one. A removed symbol keeps its entry (its codepoint is never reused) but gets no
glyph. Commit `codepoints.json` with every new symbol. Light, Regular and Semibold share the
codepoints.

### Ligatures (Sketch and any text engine)

Type the symbol name in a text layer set in Silica Symbols and the `liga` feature turns it into
the glyph: `wifi`, `arrow-down-circle`, `wifi-slash`. The letters a-z, digits and the hyphen exist
as zero-width, empty glyphs (capital letters map to the same glyphs, so `WiFi` works too), so
unmatched text draws nothing. The longest name wins (`wifi-1` before `wifi`); while typing
`wifi-1`, the intermediate `wifi` glyph appears and is replaced when the name is complete.
Alternatively paste the PUA character from `codepoints.json`.

### Sketch

Install the three `.otf` files (double click, Font Book, or copy to `~/Library/Fonts`) and restart
Sketch. "Silica Symbols" appears with Light, Regular and Semibold. Set the font size to the
symbol size in pt (24 for the 24 u canvas); the text colour is the symbol colour.

### Variable font

Not built. The outlines are outlined strokes with overlaps removed, and the three weights are
not point-compatible (308 of 324 glyphs differ in segment structure; a union changes topology
between 1.18 u and 2.15 u strokes), so a `wght` axis would need manual redrawing of the masters.

### Flutter

Weights are static files. Flutter's `Icon(..., weight:)` only sets the `wght` variation, which a
static font ignores, and `Icon` does not use `fontWeight` of its style to choose a file. So each
weight is declared as its own family, and `silica_symbols.dart` has one class per weight with
the same names and codepoints:

```yaml
# pubspec.yaml
flutter:
  fonts:
    - family: SilicaSymbolsLight
      fonts:
        - asset: fonts/SilicaSymbols-Light.otf
    - family: SilicaSymbols
      fonts:
        - asset: fonts/SilicaSymbols-Regular.otf
    - family: SilicaSymbolsSemibold
      fonts:
        - asset: fonts/SilicaSymbols-Semibold.otf
```

```dart
Icon(SilicaSymbols.wifi, size: 18)               // Regular
Icon(SilicaSymbolsLight.arrowDownCircle)         // Light
Icon(SilicaSymbolsSemibold.gear, color: c)       // Semibold
```

When the fonts live in a package, pass its name by setting `kSilicaSymbolsPackage` at the top of
the file and prefix the asset paths with `packages/<package>/` in the consumer's pubspec if
needed. Dart names are camelCase of the symbol name (`arrow-down-circle` -> `arrowDownCircle`,
`wifi-0` -> `wifi0`); names that are Dart keywords get a `Symbol` suffix (`returnSymbol`,
`switchSymbol`). Text works too: `Text(String.fromCharCode(SilicaSymbols.wifi.codePoint), style: TextStyle(fontFamily:
'SilicaSymbols'))`. A weight that follows the surrounding text is chosen in code by mapping
`FontWeight` to the class.

## Catalog

324 symbols in 11 categories, in the order of the sections of the Symbols page (12 columns,
144 px step; each category has a 960 px band, i.e. up to 5 rows).

| Category | Symbols |
| --- | --- |
| Status & Connectivity | 37 |
| Control Center & Media | 32 |
| Windows & Navigation | 45 |
| Editing & Text | 37 |
| Files & Documents | 33 |
| Communication | 25 |
| People & Security | 21 |
| Devices | 22 |
| Weather & Time | 23 |
| Shapes & Indicators | 29 |
| Settings | 20 |

Full list of names: `symbols/regular/` (one file per symbol) or the Sheet page of
`design/symbols.sketch`, ordered by category.
