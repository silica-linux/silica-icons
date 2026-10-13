# Formato delle icone

Versione 1. Vale per `apps/` e `files/`. I simboli di sistema (`symbols/`) avranno una
specifica a parte.

## Principio

L'icona di un'app è **contenuto a livelli**, non un'immagine finita. Lo sviluppatore
fornisce il fondo e il primo piano; la shell applica la forma, il bordo, le ombre, il vetro
e i temi. Così ogni icona del Dock ha la stessa forma e reagisce agli stessi temi.

Le icone dei file (`files/`) sono invece oggetti a forma libera (cartelle, documenti,
Cestino): la shell non applica maschera né corpo, solo l'ombra del contesto.

## Tela e griglia

Tutte le misure sono su una tela di **1024 × 1024**.

| Elemento | Misura |
| --- | --- |
| Corpo (dove la shell ritaglia) | 824 × 824 a (100, 100) |
| Angoli del corpo | smooth, raggio 215, smoothing 0,55 |
| Keyline quadrato | 600 × 600 a (212, 212) |
| Keyline cerchio grande | Ø 600, centro (512, 512) |
| Keyline cerchio piccolo | Ø 424, centro (512, 512) |
| Keyline verticale | 520 × 680 a (252, 172) |
| Keyline orizzontale | 680 × 520 a (172, 252) |
| Keyline documento (icone dei file) | 648 × 824 a (188, 100) |
| Keyline cartella | 824 × 648 a (100, 188) |

Il contenuto principale sta in uno dei keyline; le icone a tutta tela (un fondo disegnato,
come Calendar o Photos) occupano il corpo intero.

## Sistema di proporzioni (φ = 1,618)

È il sistema dei simboli ([`symbol-format.md`](symbol-format.md)) scalato alla tela 1024 con
**1 u = 30 px**: la keyline cerchio Ø 600 è il cerchio Ø 20 u dei simboli, il tratto Regular
(1,5 u) vale 45 px. In `design/app-icons.sketch` il simbolo `Grid / Golden 1024` (azzurro) lo
disegna sopra `Grid / Overlay` (rosa): pagina Grid e livello `Golden overlay` in ogni artboard
di Grid Check.

### Le keyline esistenti

| Keyline | Da dove viene |
| --- | --- |
| Corpo 824 | tela − 2 × 100; raggio 215 ≈ 0,26 × lato (smoothing 0,55) |
| Quadrato e cerchio 600 | grandezza base (20 u) |
| Cerchio 424 | 600 / √2: cerchio inscritto nel quadrato inscritto nel cerchio 600 |
| Verticale 520 × 680, orizzontale 680 × 520 | stesso perimetro del quadrato 600 (520 + 680 = 2 × 600), area 98 %; rapporto 1,31, non aureo |
| Documento 648 × 824, cartella 824 × 648 | il lato lungo è il corpo (824), il corto 824 / √φ: le icone dei file e delle cartelle arrivano al bordo della griglia, come il corpo delle app, e a 16–32 px non sembrano più piccole delle app accanto |

Restano tutte: il sistema aureo le completa, non le sostituisce.

### Grandezze

| Grandezza | Valori | Uso |
| --- | --- | --- |
| Serie A (dalla keyline) | **600 · 371 · 229 · 142 · 87 · 54** (600 / φⁿ); passi intermedi √φ: 472 · 292 · 180 · 112 · 69 | lati e diametri dei pezzi principali |
| Serie B (dal corpo) | 824 · 509 · 315 · 194 | pezzi che si misurano sul corpo (lente di Photo Viewer 316, carta di Mail 508, baffo di Mustache 522 entro tolleranza) |
| Rettangoli | aureo 600 × 371 (largo, a (212, 326,5)) e 371 × 600 (alto); √2 (424 × 300); keyline orizzontale e verticale | schede, schermi, foto, dischi |
| Linee auree del corpo | x e y = 415 e 609 (100 + 824 / φ² e 100 + 824 / φ) | divisori, orizzonti, pezzi decentrati |
| Spessori | 13,5 · 17 · 22 · 28 · 35 · 45 · 57 (45 × √φⁿ, come i pesi dei simboli) | righe di testo, contorni, lancette, aste, manici |
| Luci fra pezzi ripetuti | uguale allo spessore (1 : 1) per righe fitte (Mail, Terminal, file); spessore × φ per testo arioso (Text Editor); pezzo / φ² o pezzo / φ³ fra tessere e tasti | ritmo |
| Raggi | 215 · 169 · 133 · 104 · 82 · 64 · 51 · 40 · 31 · 25 · 19 · 15 (215 / √φⁿ); capsula = metà altezza; pezzo annidato = raggio esterno − distanza | angoli |
| Centro | ingombro del primo piano centrato su (512, 512) | composizione |

Rapporti interni ammessi: φ, √φ, √2, 1 : 1, 1 : 2. Tolleranza: una misura rispetta il
sistema se sta entro il 3 % della grandezza o entro 4 px. Le lunghezze delle singole righe di
testo e le posizioni dei dettagli illustrativi non sono vincolate.

Eccezioni volute:

- le icone dei file stanno sulla keyline documento (foglio 648 × 824, da y 100 a 924) e le
  cartelle sulla keyline cartella (824 × 648, da x 100 a 924, centrata su y 512): il disegno
  di prima (foglio 520 × 680, cartella 680 × 520) è stato scalato di 824 / 680 e portato al
  rapporto √φ allargando il foglio (le righe, le figure e le estensioni non si deformano) e
  alzando la cartella (2,8 %, entro tolleranza); il contenuto del foglio è centrato su y 473,
  sopra l'estensione; il pannello anteriore della cartella è 824 × 483,5 da y 352,5;
- il Cestino è largo 584 (≈ 600) e alto 734 (h : l ≈ √φ), con la base del cestello a y 914,
  quasi sul fondo del corpo delle app (924): nel Dock poggia sulla stessa linea;
- la piega dei fogli (165 × 160: la 132 di prima scalata con il foglio) non è sulla serie: cambiarla vuol dire ridisegnare il tracciato di ogni foglio; resta finché i
  fogli non si ridisegnano;
- il Cestino e Stack Close non sono né fogli né cartelle e non cambiano.

### Correzioni ottiche e scostamenti dal rapporto puro

| Icona | Rapporto puro | Scelto | Motivo |
| --- | --- | --- | --- |
| Clock | quadrante sulla keyline Ø 600 | a tutto corpo (tacche fino a Ø 740) | un orologio piccolo nel corpo bianco perde leggibilità; i numeri stanno su Ø 480 ≈ 472 |
| Fonts | blocco maiuscole centrato su y 512 | 335…655 (centro 495) | centro ottico sopra quello geometrico; in x l'ingombro dei glifi è centrato su 512 |
| Help | punto interrogativo centrato sull'ingombro | centro x 508 | la massa del ricciolo sta a destra |
| Calendar | disco Ø 472 | Ø 460 (entro tolleranza) | la base del disco resta sulla keyline 812 e la luce mese–disco a 54 |
| Text Editor | composizione centrata | foglio a x 248…736, penna in diagonale fino a x 905 | la penna è il secondo soggetto; resta dentro il corpo |
| Store, lucchetto | centro dell'ingombro sul centro | centro su 512 con il manico incluso | sacchetto e lucchetto hanno la stessa base (794) |
| Mustache | primo piano in una keyline | profilo a filo del corpo (margine 64), occhiali da x 182 a 842, lenti Ø 229 (tratto 22) centrate sulla linea aurea y 415, baffo largo 522 | ritratto a tutta tela: il profilo segue gli angoli del corpo |

## Cartella di un'icona

```
apps/<id>/
  icon.json              manifest
  background.svg         fondo (tela 1024, riempie almeno il corpo)
  foreground.svg         primo piano (tela 1024)
  background-dark.svg    facoltativo: fondo per i temi scuri
  foreground-dark.svg    facoltativo: primo piano per i temi scuri
  preview.png            anteprima 256 px del tema Default, composta (solo documentazione)
```

`<id>` è in minuscolo con trattini (`text-editor`). Tutti gli SVG hanno
`viewBox="0 0 1024 1024"`; le coordinate sono quelle della tela, quindi i livelli si
sovrappongono senza spostamenti.

### Cosa NON va nei livelli

La shell li aggiunge da sé; se ci sono, il risultato raddoppia:

- la maschera del corpo e il suo bordo luminoso (il "Rim");
- l'ombra del primo piano sul fondo e l'ombra dell'icona sul Dock;
- la sfocatura del vetro e il riflesso dei temi Clear.

Le ombre e le sfumature **interne** al disegno (fra due parti del primo piano) fanno parte
dell'illustrazione e restano.

### Testo

Il testo negli SVG usa solo Inter (fornito dalla shell). Meglio convertirlo in tracciati
quando non deve cambiare.

## Manifest `icon.json`

```json
{
  "format": 1,
  "id": "mail",
  "name": "Mail",
  "kind": "app",
  "keyline": "landscape",
  "layers": [
    { "role": "background", "file": "background.svg" },
    { "role": "foreground", "file": "foreground.svg", "shadow": "neutral" }
  ],
  "variants": {
    "dark": { "background": "background-dark.svg", "foreground": "foreground-dark.svg" }
  },
  "dynamic": null
}
```

| Campo | Valori |
| --- | --- |
| `kind` | `app` (forma imposta dalla shell) o `file` (forma libera) |
| `keyline` | `square`, `circle`, `circle-small`, `portrait`, `landscape`, `full` |
| `layers` | dal basso verso l'alto: un `background` e da 1 a 4 livelli di primo piano |
| `shadow` | ombra che la shell disegna sotto il livello: `neutral`, `chromatic` (presa dal colore del livello) o `none` |
| `variants.dark` | livelli sostitutivi per Dark, Clear Dark e Tinted Dark |
| `dynamic` | contenuto aggiornato a runtime, vedi sotto |

Le icone `file` hanno un solo livello `artwork` (`icon.svg`, `icon-dark.svg`) e nessun
fondo.

## Temi

La shell genera sei temi dai livelli:

| Tema | Fondo | Primo piano |
| --- | --- | --- |
| Default | `background` | `foreground` |
| Dark | `background-dark`, altrimenti grafite `#3a3a3c → #161618` | `foreground-dark`, altrimenti `foreground` |
| Clear Light | vetro chiaro (bianco 50 % → 25 % sopra lo sfondo sfocato) | `foreground` in scala di grigi, luminanza mappata su 105–255 |
| Clear Dark | vetro scuro (grafite 50 % → nero 55 %) | come sopra, mappata su 150–255 |
| Tinted Light | tinta schiarita al 90 % → 76 % | luminanza mappata sulla tinta (scura → tinta → bianco) |
| Tinted Dark | tinta scurita al 62 % → 84 % | luminanza mappata da tinta scura a tinta chiara |

Nei temi scuri il fondo è neutro e il colore resta sul primo piano (Mail, Store, Help):
è la regola del set.

## Contenuto dinamico

`dynamic` descrive i livelli che la shell aggiorna a runtime.

### Orologio

```json
"dynamic": {
  "type": "clock",
  "hands": [
    { "unit": "hour",   "file": "hand-hour.svg" },
    { "unit": "minute", "file": "hand-minute.svg" },
    { "unit": "second", "file": "hand-second.svg", "min_size": 64 }
  ],
  "cap": "cap.svg"
}
```

Ogni lancetta è disegnata verso le 12 e ruota attorno a (512, 512):
ore = (h mod 12 + m/60 + s/3600) × 30°, minuti = (m + s/60) × 6°, secondi = s × 6°.
`cap` (mozzo e perno) va sopra le lancette. La lancetta dei secondi si mostra solo da
`min_size` pt in su; aggiornamento ogni secondo se visibile, altrimenti ogni minuto, mai
con l'icona fuori schermo.

### Calendario

```json
"dynamic": {
  "type": "calendar",
  "month": { "font": "Inter", "size": 92, "weight": 900, "tracking": 4,
             "color": "#f2382e", "dark_color": "#ff5248",
             "box": [100, 206, 824, 120], "case": "upper", "max_width": 560 },
  "day":   { "font": "Inter", "size": 280, "weight": 700, "tracking": -10,
             "color": "#ffffff", "box": [100, 410, 824, 460] }
}
```

Mese per intero, localizzato; se supera `max_width` il corpo scende in proporzione e la
linea di base di 0,6 × la riduzione. Giorno senza zero iniziale. Aggiornamento a
mezzanotte locale e al cambio di data o fuso.

### File generico

`files/file-generic` è il foglio vuoto su cui la shell scrive l'estensione, per i tipi di
file senza un'icona propria (`.json`, `.docx`, `.blend`…).

```json
"dynamic": {
  "type": "file-label",
  "label": { "font": "Inter", "size": 160, "weight": 900, "tracking": 0,
             "box": [245, 376, 534, 194], "case": "upper",
             "max_chars": 4, "max_width": 534 },
  "colors": { "document": {...}, "data": {...}, "code": {...},
              "archive": {...}, "media": {...}, "other": {...} },
  "overrides": {},
  "fallback": "file-unknown"
}
```

- Etichetta: l'estensione senza punto, in maiuscolo, centrata nel `box` (centro ottico
  del foglio, y 473 come le altre icone dei file).
- Se l'estensione supera `max_width` il corpo scende in proporzione; oltre `max_chars`
  caratteri, o senza estensione, si usa `fallback` (il foglio con il punto di domanda).
- Colore dalla categoria del tipo MIME (shared-mime-info): `text/*` e documenti da ufficio
  → `document`; JSON, XML, YAML, CSV, database → `data`; sorgenti e script → `code`;
  archivi e pacchetti → `archive`; `image/*`, `audio/*`, `video/*`, font → `media`;
  il resto → `other`. `overrides` associa a una singola estensione una categoria o un
  colore (`{"json": "data"}`, `{"sketch": {"color": "#f7b500"}}`).
- Il tipo di file con un'icona propria (PDF, testo, archivio, immagine, audio, video,
  codice) usa sempre quella.

### Cartella generica

`files/folder-generic` è la cartella su cui la shell (e Mustache) incide un simbolo di
`symbols/`: le cartelle speciali (Documenti, Download, Immagini, Home…) e le cartelle con una
tinta. I livelli sono quelli della cartella (`files/folder`), senza simbolo.

```json
"dynamic": {
  "type": "folder-symbol",
  "symbol": {
    "box": [374, 456, 276, 276],
    "sizes": [
      { "min_size": 128, "weight": "light",    "scale": 1 },
      { "min_size": 64,  "weight": "regular",  "scale": 1 },
      { "min_size": 32,  "weight": "semibold", "scale": 1,     "highlight": false },
      { "min_size": 16,  "weight": "semibold", "scale": 1.272, "highlight": false }
    ]
  },
  "effect": {
    "light": { "color": "#1a64c8", "opacity": 0.78, "highlight": "#ffffff",
               "highlight_opacity": 0.5, "offset": 4 },
    "dark":  { "color": "#0b3f94", "opacity": 0.8,  "highlight": "#ffffff",
               "highlight_opacity": 0.2, "offset": 4 }
  },
  "tint": {
    "light": { "luminance": [0.35, 0.85], "shade": 0.72, "glow": 0.5 },
    "dark":  { "luminance": [0.28, 0.75], "shade": 0.58, "glow": 0.35 },
    "labels": { "red": "#f2382e", "orange": "#ff8a00", "yellow": "#f5c400", "green": "#2fb350",
                "blue": "#2f7cf6", "purple": "#a052e0", "gray": "#8e8e93" }
  },
  "folders": { "HOME": "house", "DESKTOP": "display", "DOCUMENTS": "doc-text",
               "DOWNLOAD": "arrow-down-circle", "MUSIC": "music-note", "PICTURES": "photo",
               "VIDEOS": "film", "TEMPLATES": "doc-plus", "PUBLICSHARE": "share",
               "APPLICATIONS": "square-grid-2x2", "LIBRARY": "book", "SHARED": "person-2",
               "NETWORK": "network" },
  "fallback": "folder"
}
```

Proporzioni (tela 1024, keyline cartella):

| Misura | Valore | Da dove viene |
| --- | --- | --- |
| Pannello anteriore | 824 × 483,5 da (100, 352,5), centro (512, 594) | la cartella |
| Area viva del simbolo (Ø 20 u) | 230 ≈ 229 | serie A (600 / φ²); è pannello / φ^1,5 |
| Tela del simbolo (24 u), `box` | 276 × 276, centrata sul pannello: 1 u = 11,5 px | area viva × 24 / 20 |
| Tratto | Light 13,6 · Regular 17,3 · Semibold 24,7 | 1,18 · 1,5 · 2,15 u: Light e Regular cadono sugli spessori 13,5 e 17 della serie |
| Simbolo piccolo (`scale` 1,272) | tela 351, area viva 292 | × √φ, serie A |
| Scavo (`offset`) | 4 px, almeno mezzo pixel reso | ≈ tratto Light / φ³ |

- **Simbolo**: `symbols/<weight>/<nome>.svg` dello stesso repo, colorato al posto di
  `currentColor`, centrato in `box` e scalato di `scale` attorno al centro. La fascia è la prima
  di `sizes` con `min_size` ≤ lato dell'icona in pt (il lato del corpo, come per l'orologio);
  sotto l'ultima (16 pt) il simbolo non si disegna. Il peso cresce mentre l'icona rimpicciolisce
  perché il tratto reso resti fra 1 e 4 px circa: Light da 128, Regular da 64, Semibold sotto,
  e sotto 32 anche più grande (× √φ).
- **Effetto inciso** (`effect`, per tema): prima la copia del simbolo in `highlight` con
  `highlight_opacity`, spostata in basso di `offset` (il bordo inferiore dello scavo prende luce),
  poi il simbolo in `color` con `opacity`. Sotto 64 pt (`"highlight": false`) solo il simbolo:
  il riflesso di mezzo pixel lo impasterebbe.
- **Cartelle speciali** (`folders`): le chiavi sono quelle di `xdg-user-dirs`
  (`XDG_<CHIAVE>_DIR` in `~/.config/user-dirs.dirs`: DESKTOP, DOCUMENTS, DOWNLOAD, MUSIC,
  PICTURES, VIDEOS, TEMPLATES, PUBLICSHARE) più cinque chiavi di Silica: `HOME` (la cartella
  dell'utente), `APPLICATIONS` (`~/Applications` e le cartelle `applications` dei dati XDG),
  `LIBRARY` (`~/.local/share`, la libreria dell'utente), `SHARED` (cartella condivisa) e
  `NETWORK` (cartella di rete). Le ultime due non hanno un percorso fisso: le dà chi conosce la
  cartella (Mustache sa se è un mount di rete o una condivisione). Una cartella che non è fra
  queste, o un simbolo che non esiste in `symbols/`, prende `fallback` (la cartella semplice).
  Il Cestino ha un'icona propria. Mustache può anche passare un simbolo qualsiasi di `symbols/`.
- **Tinta** (`tint`): un colore `#rrggbb` personalizzato o il nome di un'etichetta di `labels`.
  La cartella composta (base e simbolo) passa per una rampa sulla luminanza: L = 0,2126 R +
  0,7152 G + 0,0722 B (sRGB, 0–1); da `luminance[0]` a `luminance[1]` il colore va da
  tinta × `shade` a tinta schiarita verso il bianco di `glow` (fuori dall'intervallo si ferma
  agli estremi). È lineare, quindi è una matrice di colore 4 × 5 (`ColorFilter.matrix`): il
  simbolo resta più scuro del pannello e il riflesso più chiaro, con lo stesso colore. Senza
  tinta la cartella resta il disegno blu, senza rampa.
- **Altri temi**: Clear e Tinted (Light e Dark) applicano la loro regola alla cartella già
  composta con il simbolo (luminanza mappata, vedi Temi), quindi il simbolo resta lo scavo più
  scuro del pannello; nei temi Clear il riflesso dello scavo si toglie (`highlight_opacity` 0),
  perché il vetro ha già il suo bordo. La tinta personale vale solo in Default e Dark: Tinted
  usa la tinta del tema per tutte le cartelle.

`design/app-icons.sketch`: Folder Generic (pagina Icons, accanto a File Generic) con gli esempi
Documents, Downloads e Music con tinta #e8336d, e sotto una cartella per ogni chiave di `folders`; in Grid Check i riquadri del simbolo (276 e 351)
e l'area viva; in Showcase Files le stesse cartelle in Default e Dark.

## Icone senza livelli

Un'app che ha solo un'icona freedesktop (PNG o SVG già composto) viene ridotta al keyline
quadrato e appoggiata su un fondo neutro (bianco in chiaro, grafite in scuro).
