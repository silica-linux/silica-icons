# Formato delle icone

Versione 1. Vale per `apps/`, `files/` e `badges/`. I simboli di sistema (`symbols/`) avranno una
specifica a parte.

## Principio

L'icona di un'app è **contenuto a livelli**, non un'immagine finita. Lo sviluppatore
fornisce il fondo e il primo piano; la shell applica la forma, il bordo, le ombre, il vetro
e i temi. Così ogni icona del Dock ha la stessa forma e reagisce agli stessi temi.

Le icone dei file (`files/`) sono invece oggetti a forma libera (cartelle, documenti,
Cestino): la shell non applica maschera né corpo, solo l'ombra del contesto. Per le icone dei
file **il lato è la tela intera**: un'icona di file da 64 pt è la tela 1024 disegnata a 64 pt,
senza riduzioni (niente corpo 824, niente fattori come il 92 % di prima); le fasce che
dipendono dal lato (`min_size` del simbolo della cartella, dell'etichetta e dei badge) si
confrontano con questo lato. Nel Dock un luogo (cartella, Cestino) usa la tela delle app
accanto, quella che sborda di 100/824 dal corpo.

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
| Keyline documento (icone dei file) | 684 × 904 a (170, 60) |
| Keyline cartella | 944 × 760 a (40, 132) |
| Keyline volume (dischi e server) | 944 × 583 a (40, 220,4) |
| Keyline Cestino | 656 × 824 a (184, 100): cestello con la base a y 924, bordo 667 |
| Badge | disco Ø 824 centrato sulla propria tela 1024 (vedi Badge) |

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
| Documento 684 × 904, cartella 944 × 760 | misurate sul Finder a icone grandi (cattura a 1×, icone da 128 pt): corpo del foglio 86 × 114 (0,668 × 0,883 della tela, senza l'ombra di ≈ 5 pt per lato che mette la shell; 96 × 124 con l'ombra), cartella 118 × 94 (0,922 × 0,734); a 64 pt 42 × 56 e 59 × 47, stessi rapporti. Il foglio è il disegno di prima (648 × 824) scalato di 904 / 824 = 1,0971 attorno al centro e ristretto in larghezza a 684 (rapporto 1,32 misurato, non più √φ): le righe, le figure e le estensioni scalano di 1,0971 senza deformarsi, solo il contorno e la piega seguono la larghezza. La cartella è quella di prima (824 × 663) scalata di 944 / 824 = 1,1456 attorno al centro: 944 × 760 contro 944 × 752 misurato (1 %, entro tolleranza). Nel Dock la cartella misura 1,13 volte il corpo delle app accanto (54 contro 48 px a 2×), cioè 0,905 della tela: torna con 944 / 1024 |
| Volume 944 × 583 | la lastra di prima (824 × 509: lato lungo il corpo, corto 824 / φ, fascia frontale 509 / φ² da y 572) scalata di 1,1456 attorno al centro come la cartella: il volume del Finder è una scatola verticale (0,71 × 0,86 della tela sulla Scrivania), una forma diversa dalla lastra, quindi non si misura direttamente; fascia frontale 222,8 da y 580,7 |
| Disco ottico Ø 944 | Ø 824 scalato come la cartella; zona di fermo Ø 361, anello interno Ø 264, foro Ø 128 (le misure di prima × 1,1456) |
| Cestino 656 × 824 | misurato nel Dock (cattura a 2×): il cestello è alto quanto il corpo delle app (49 contro 48 px) e poggia sulla stessa base, largo 0,86 del corpo; con i fogli dentro è alto 1,10 del corpo. Il disegno di prima (584 × 734, base a 914) è scalato di 824 / 734 = 1,1226 e la base portata a 924: cestello 656 × 824 (bordo 667), con i fogli 913 (1,11 del corpo); resta più stretto del riferimento (0,81 del corpo) perché la forma è nostra |
| Badge 315 e 509 | corpo / φ² e corpo / φ: il riquadro del badge va dal bordo del corpo alla linea aurea (x e y 415 e 609) |

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

- le icone dei file escono dal corpo delle app e occupano quasi tutta la tela, come nel
  riferimento (vedi Le keyline esistenti): foglio 684 × 904 da (170, 60), cartella 944 × 760 da
  (40, 132), entrambi centrati su (512, 512). Storia: il disegno di partenza (foglio 520 × 680,
  cartella 680 × 520) era stato portato al corpo 824 (foglio 648 × 824 al rapporto √φ, cartella
  824 × 663), poi alla tela intera con le misure del Finder (v0.2.0). Il contenuto del foglio è
  centrato su y 469 (473 prima), sopra l'estensione; il pannello anteriore della cartella è
  944 × 619 da y 273,1 (0,815 dell'altezza; nel riferimento 0,82);
- il Cestino è largo 656 (bordo 667) e alto 824, con la base del cestello a y 924, sul fondo del
  corpo delle app: nel Dock poggia sulla stessa linea e ha la stessa altezza;
- la piega dei fogli (174 × 176: la 165 × 160 di prima, scalata in larghezza di 684 / 648 e in
  altezza di 904 / 824) non è sulla serie: cambiarla vuol dire ridisegnare il tracciato di ogni
  foglio; resta finché i fogli non si ridisegnano;
- il Cestino non è né foglio né cartella: ha la sua keyline, misurata nel Dock;
- Stack Close (il pulsante che prende il posto della cartella nel Dock a pila aperta) è un'icona
  `file` a forma libera che segue la **griglia delle app**: quadrato arrotondato 824 × 824 a
  (100, 100), centro (512, 512), angoli 174,42. Nella cattura a 1× il pulsante è 52 pt contro
  49 pt del corpo delle app, con il centro 2,5 pt più in alto; per scelta di progetto sta nella
  griglia come le icone vicine, e la geometria misurata (874, angoli 185, centro a 470) è scalata
  di 824/874 e ricentrata. Fondo bianco traslucido da 0,35 (alto) a 0,08
  (basso) sul Dock (129, 130, 137), che dà 173 in alto e 139 in basso; chevron in giù #1B1B1D
  largo 19 pt e alto 10, tratto 2,5 pt (39,6 dopo la scala) con estremi tondi, centrato sul
  pulsante (punti (381,42, 452,6), (512, 571,4), (642,58, 452,6)). Il tema
  scuro è misurato (sessione M6, `dock-stacks.md`): stesso quadrato 51 × 52 pt, ma **più scuro**
  del Dock (104, 105, 110): fondo **nero traslucido** da 0,12 (alto, dà 92) a 0,56 (basso, dà 48),
  coerente sui tre canali entro ±0,02 (a differenza di un opaco, segue il Dock); chevron
  **bianco #FFFFFF**, stessa geometria;
- i tipi di file aggiunti per Mustache (foglio di calcolo, presentazione, font, immagine disco,
  eseguibile, documento, pagina web) hanno la figura nel riquadro 461 × 292 centrato su
  (512, 473), come Code e Image (la larghezza delle righe di testo dei fogli, 461 ≈ 472 entro
  tolleranza; 292 serie A); la tabella del foglio di calcolo ha luci di 13,5, la diapositiva è
  461 × 285 (rapporto φ), il globo Ø 292 con meridiani di 13,5, "Aa" è Inter SemiBold in
  tracciati con la maiuscola alta 292, il disco dell'immagine disco è 461 × 229 (serie A).
  Queste misure sono sul foglio da 824 e negli SVG scalano tutte di 1,0971 attorno a (512, 512)
  (riquadro 506 × 320 centrato su (512, 469));
- i volumi sono lastre 824 × 509 con raggio 64 e il server è tre unità alte 155 con luci di 22,
  sul disegno da 824; negli SVG scalano di 1,1456 attorno al centro (lastra 944 × 583, raggio 73).

Negli SVG la scala sta in un solo attributo: `transform` sul gruppo `icon` (`icon-dark`) per
cartelle, volumi e Cestino; per i fogli il gruppo scala il tutto di 1,0971 e il contorno
(`Page`) e la piega (`Corner`) hanno in più una riduzione orizzontale di 684 / 711 attorno
all'asse del foglio. I tracciati restano quelli del disegno da 824.

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

Vale anche per le icone `file`: tutte (fogli, cartelle, Cestino, volumi e badge) sono
**piatte**, solo riempimenti, sfumature interne e un filo di contorno del foglio o della
lastra, senza ombra a terra né ombre esterne o interne fatte con i filtri: l'ombra del
contesto la mette la shell (IC-01). Negli SVG di `files/` non c'è nessun `filter`. I fogli, le
cartelle e il Cestino disegnati prima dei tipi di file per Mustache avevano l'ombra a terra e le
ombre dei pezzi: sono stati appiattiti con la stessa regola, senza cambiare forma, colori o
proporzioni.

Sfumatura verticale dei fogli e delle cartelle: misurata sul Finder a icone grandi (luminanza
Rec. 709 fra il 10 % e il 90 % dell'altezza del pannello anteriore, lontano da bordi e
simboli), la cartella cala di circa 27 su 255 (RGB 127 200 243 in alto, 96 174 225 in basso) e
il foglio senza anteprima non cala (245 uniforme). I fogli vanno quindi da `#FFFFFF` a
`#F8F9FB` (scuro `#3A3A3E` a `#333337`, calo ≈ 4 e ≈ 5) e le cartelle hanno due soli passi
(pannello `#8FCDFF` a `#5AA7F8`, scuro `#7DBBF6` a `#4D93E6`, calo ≈ 31; dietro `#4A9EFB` a
`#2F84EE`, scuro `#3786E6` a `#1F68CC`), contro un calo di ≈ 64 delle cartelle e ≈ 12 dei fogli
di prima.

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
| `keyline` | `square`, `circle`, `circle-small`, `portrait`, `landscape`, `full`; per i volumi `volume` (solo documentazione: la shell non ritaglia le icone `file`) |
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
  "label": { "font": "Inter", "size": 175.53, "weight": 900, "tracking": 0,
             "box": [219.08, 362.8, 585.84, 212.83], "case": "upper",
             "max_chars": 5, "max_width": 585.84, "overflow": "shrink" },
  "colors": { "document": {...}, "data": {...}, "code": {...},
              "archive": {...}, "media": {...}, "other": {...} },
  "overrides": { "json": "data", "epub": "document", "blend": "media", ... },
  "icons": {
    "mime": { "application/pdf": "file-pdf", "text/csv": "file-spreadsheet",
              "font/*": "file-font", "image/*": "file-image", ... },
    "extensions": { "pdf": "file-pdf", "xlsx": "file-spreadsheet", "sh": "file-executable", ... }
  },
  "fallback": "file-unknown"
}
```

- Etichetta: l'estensione senza punto, in maiuscolo, centrata nel `box` (centro ottico
  del foglio, y 469 come le altre icone dei file).
- Se l'estensione supera `max_width` il corpo scende in proporzione; oltre `max_chars`
  caratteri, o senza estensione, si usa `fallback` (il foglio con il punto di domanda).
- Colore dalla categoria, nell'ordine: `overrides` dell'estensione, poi la `category` della
  voce di `icons.mime` che ha scelto il file generico, poi la categoria del tipo MIME
  (shared-mime-info): `text/*` e documenti da ufficio → `document`; JSON, XML, YAML, CSV,
  database → `data`; sorgenti e script → `code`; archivi e pacchetti → `archive`; `image/*`,
  `audio/*`, `video/*`, font → `media`; il resto → `other`. `overrides` associa a una singola
  estensione una categoria o un colore (`{"json": "data"}`, `{"sketch": {"color": "#f7b500"}}`).
  Categorie e `overrides` valgono **solo per il file generico**: un'icona di tipo ha il colore
  del proprio manifest (vedi Icone dei tipi di file) e non lo prende mai da qui.
- Il tipo di file con un'icona propria usa sempre quella. `icons` è **la** mappa del repo (tipo →
  icona); chi risolve l'icona di un file (SilicaIcon, Mustache, il Dock) non ne tiene una sua.
  Una voce di `icons.mime` è il nome di un'icona (`"text/csv": "file-spreadsheet"`) oppure il
  file generico con la sua categoria (`"application/json": {"icon": "file-generic",
  "category": "data"}`). Ordine di risoluzione per un file regolare:
  0. il tipo MIME si porta al nome canonico con gli `aliases` di shared-mime-info
     (`text/xml` → `application/xml`, `text/x-yaml` → `application/yaml`);
  0b. se il tipo viene solo dal nome e `globs2` dà per quell'estensione più tipi con lo stesso
     peso (nome ambiguo: `.ts` è TypeScript, Qt Linguist o MPEG-TS a seconda del sistema), il
     passo 4 (`icons.extensions`) vale prima dei passi 1–3; se il contenuto decide il tipo
     (magic), resta l'ordine normale;
  1. il tipo MIME (shared-mime-info, dal contenuto e dal nome) in `icons.mime`, esatto;
  2. lo stesso con il sottotipo `*` (`image/*`, `audio/*`, `video/*`, `font/*`);
  3. i genitori del tipo (`sub-class-of` di shared-mime-info, in ordine), ripetendo 1 e 2: un
     tipo `text/x-…` senza voce resta così testo e non codice solo se nessun genitore è in mappa;
  4. l'estensione in minuscolo in `icons.extensions` (l'ultima dopo il punto; per i nomi
     `.tar.<x>` vale l'estensione finale, che è già in mappa come archivio);
  5. altrimenti `file-generic` con l'etichetta e il colore di categoria; senza estensione o
     oltre `max_chars`, `fallback`.
  Un eseguibile senza estensione (bit `x` e tipo `application/x-executable`,
  `application/x-pie-executable`, `application/x-shellscript`) prende `file-executable` al
  passo 1; un file con bit `x` ma di un altro tipo (un `.py`) tiene l'icona del suo tipo.
- Icone dei tipi e categoria della loro estensione nel file generico:

  | Icona | Estensioni (sintesi) | Categoria |
  | --- | --- | --- |
  | `file-pdf` | pdf | document |
  | `file-text` | txt, md, log, rst | document |
  | `file-document` | rtf, odt, doc, docx, pages | document |
  | `file-spreadsheet` | xlsx, xls, ods, numbers, csv, tsv | document |
  | `file-presentation` | pptx, ppt, odp, key | document |
  | `file-font` | ttf, otf, ttc, woff, woff2 | media |
  | `file-disk-image` | iso, img, dmg, qcow2, vdi, vmdk | archive |
  | `file-executable` | sh, bash, zsh, fish, run, bin, appimage | code |
  | `file-web` | html, htm, xhtml, mhtml | code |
  | `file-code` | rs, dart, py, js, ts, c, go, java, css… | code |
  | `file-archive` | zip, tar, gz, xz, zst, 7z, rar, deb, rpm… | archive |
  | `file-image`, `file-audio`, `file-video` | i formati comuni | media |

  L'elenco completo è nel manifest.
- **Una voce esplicita vince sempre sui genitori.** Il passo 3 segue `sub-class-of`, e in
  shared-mime-info molti formati di dati discendono da tipi di codice o di testo:
  `application/json` è sottoclasse di `application/json5` → `application/ecmascript` →
  `text/javascript` (prenderebbe `file-code`), `application/xml`, `application/yaml`,
  `application/toml`, `application/sql`, `text/calendar` e `text/vcard` di `text/plain`
  (prenderebbero `file-text`), EPUB, i documenti ODF senza icona e i formati Apple di
  `application/zip` (prenderebbero `file-archive`). Per questi `icons.mime` ha una voce
  esplicita, perché è deterministica: non dipende dalla versione del database né da quale
  genitore si incontra prima, e un `"json": "data"` in `overrides` da solo non basterebbe mai,
  perché `overrides` conta solo quando l'icona è già il file generico. Una voce esplicita copre
  anche i figli (`application/geo+json`, `application/ld+json` passano da `application/json`;
  i tipi `+xml` da `application/xml`). Le voci aggiunte (dal database di shared-mime-info, ramo principale, ottobre 2026):
  - file generico `data`: `application/json`, `application/json5`, `application/xml`,
    `application/xml-dtd`, `application/yaml`, `application/toml`, `application/sql`,
    `text/calendar`, `text/vcard`, KMZ, database ODF;
  - file generico `document`: notebook Jupyter (`application/x-ipynb+json`), EPUB, FictionBook,
    fumetti CBZ/CBR, PostScript, XPS e OpenXPS, TeX, e-mail (`message/rfc822`), disegni,
    grafici e formule ODF, Visio, Draw e Math di OpenOffice 1, HWPX;
  - file generico `media`: immagine ODF, `model/3mf`;
  - icone di tipo: ODF flat XML (`fodt`, `fods`, `fodp`), modelli e varianti con macro di
    Office (`dotx`, `dotm`, `xltx`, `xltm`, `potx`, `potm`, `ppsx`, `ppsm`, `sldx`, `sldm`),
    Pages, Numbers e Keynote, Writer, Calc e Impress di OpenOffice 1 → documento, foglio di
    calcolo, presentazione; TypeScript (`application/typescript`, che shared-mime-info fa
    discendere da `application/x-executable`), Dart, C#, Julia, Elixir, Erlang, Haskell, Nim,
    OCaml, Sass e Scala → `file-code` (altrimenti `text/plain` li farebbe testo, anche se la
    loro estensione è in `icons.extensions`).

  Restano ai genitori, di proposito: i pacchetti ZIP (`appx`, `msix`, `xpi`, `oxt`, `pkpass`)
  sono archivi; gli altri sorgenti senza voce (Fortran, Pascal, Lisp…) e i formati di testo
  (sottotitoli, patch, unità systemd) restano `file-text`; i tipi che derivano da un'icona di
  tipo (`pptm` da `pptx`, EXE e DLL da `application/x-executable`) ne prendono l'icona.

### Icone dei tipi di file

Le icone dei tipi (`file-pdf`, `file-text`, `file-image`, `file-code`…) disegnano solo la
figura: l'estensione la scrive la shell, come sul file generico, perché la stessa icona vale per
`.jpg` e `.png`, `.ttf` e `.otf`, `.rs` e `.py`. Il tipo è `file-type-label`, distinto da
`file-label`: non ha la mappa (`icons`), le categorie né `overrides`, e il colore è uno solo.

```json
"dynamic": {
  "type": "file-type-label",
  "label": { "font": "Inter", "size": 111.67, "weight": 500, "tracking": 0,
             "box": [270.64, 763.7, 482.72, 136.04], "case": "upper",
             "max_chars": 5, "max_width": 482.72, "overflow": "shrink",
             "color": "#30b0c7", "dark_color": "#30b0c7",
             "no_extension": null, "min_size": 32 }
}
```

| Campo | Significato |
| --- | --- |
| `box` | riquadro dell'etichetta, tela 1024: `[x, y, larghezza, altezza]`. L'altezza è la riga naturale di Inter (1,2102 × `size`); il testo è centrato in orizzontale e la riga centrata in verticale, quindi la linea di base cade a y + h/2 − 0,605 × corpo + 0,96875 × corpo |
| `font`, `size`, `weight`, `tracking` | Inter (asse `opsz` 14), corpo in unità della tela, peso 500 (Medium) |
| `case` | `upper`: l'estensione senza punto in maiuscolo |
| `max_chars` | oltre questo numero di caratteri l'estensione non si scrive e vale `no_extension` |
| `max_width` | larghezza massima del testo, uguale alla larghezza del `box` |
| `overflow` | `shrink`: un'estensione entro `max_chars` più larga di `max_width` riduce il corpo in proporzione, sempre centrata nel `box`; `truncate` (non usato dalle icone del repo) taglierebbe ai primi `max_chars` caratteri |
| `color`, `dark_color` | colore nei temi chiari e in Dark; Clear e Tinted passano l'icona composta (figura ed etichetta) per la loro mappatura, come la cartella generica |
| `no_extension` | cosa scrivere se il file non ha estensione o l'ha più lunga di `max_chars`: `null` = niente etichetta, la figura basta (un eseguibile senza estensione, un `README`); una stringa la scrive tale e quale |
| `min_size` | sotto questo lato dell'icona in pt (la tela intera, vedi Principio) l'etichetta non si disegna: a 16 pt sarebbe alta meno di 2 px |

L'estensione è la stessa del passo 4 della risoluzione (l'ultima dopo il punto, in minuscolo,
poi in maiuscolo per `case`); per i nomi `.tar.<x>` la finale (`GZ`, `XZ`). Il riquadro è misurato
sul testo che c'era negli SVG (centro x 512, riga da y 741,43; corpo 101,79, Medium; largo 440,
la pagina da 648 meno due margini di 104) e scalato con il contenuto del foglio (× 1,0971 attorno
a (512, 512)): riga da y 763,7, corpo 111,67, largo 482,72 su una pagina di 684 (margini 100).
`XHTML`, `WOFF2`, `QCOW2` ci stanno a corpo pieno.

| Icona | `box` | `color` | `dark_color` | `no_extension` |
| --- | --- | --- | --- | --- |
| `file-pdf` | 314,52, 755,73, 394,95, 136,04 (`max_chars` 4, `max_width` 394,95) | `#ffffff` | `#ffffff` | `"PDF"` |
| `file-text` | 270,64, 763,7, 482,72, 136,04 | `#8e8e93` | `#aeaeb2` | null |
| `file-document` | 270,64, 763,7, 482,72, 136,04 | `#2f7cf6` | `#5aa0ff` | null |
| `file-spreadsheet` | 270,64, 763,7, 482,72, 136,04 | `#1f9d55` | `#3fd07f` | null |
| `file-presentation` | 270,64, 763,7, 482,72, 136,04 | `#f2780c` | `#ff9f40` | null |
| `file-code` | 270,64, 763,7, 482,72, 136,04 | `#ff6a00` | `#ff8a3d` | null |
| `file-executable` | 270,64, 763,7, 482,72, 136,04 | `#ff6a00` | `#ff8a3d` | null |
| `file-web` | 270,64, 763,7, 482,72, 136,04 | `#ff6a00` | `#ff8a3d` | null |
| `file-archive` | 270,64, 763,7, 482,72, 136,04 | `#8e8e93` | `#aeaeb2` | null |
| `file-disk-image` | 270,64, 763,7, 482,72, 136,04 | `#8e8e93` | `#aeaeb2` | null |
| `file-image` | 270,64, 763,7, 482,72, 136,04 | `#30b0c7` | `#30b0c7` | null |
| `file-audio` | 270,64, 763,7, 482,72, 136,04 | `#ff2d55` | `#ff2d55` | null |
| `file-video` | 270,64, 763,7, 482,72, 136,04 | `#5e5ce6` | `#7d7aff` | null |
| `file-font` | 270,64, 763,7, 482,72, 136,04 | `#e8336d` | `#ff5c8a` | null |

- **PDF**: anche l'etichetta del PDF è dinamica, bianca sulla pastiglia rossa (il `box` è la
  pastiglia meno i margini). Un `.pdf` scrive `PDF`; un tipo che deriva da `application/pdf`
  con un'altra estensione scrive la sua (`AI`); senza estensione resta `PDF`, perché la
  pastiglia vuota sembrerebbe un errore. Così nessun SVG contiene testo.
- I grigi (testo, archivio, immagine disco) e il viola del video si schiariscono in Dark,
  perché sul foglio scuro avevano poco contrasto; arancio del codice e degli eseguibili come
  la categoria `code` del file generico.
- `file-unknown` non ha etichetta: è il foglio con il punto di domanda.

`design/app-icons.sketch`: nella pagina Icons (e in Showcase Files) ogni tipo ha ancora il
livello di testo `Extension` come esempio (`PNG`, `DOCX`…), nel colore del manifest; non va
nell'esportazione, come `JSON` del file generico. Riferimento: `tools/compose.py`,
`compose_file(icona, lato, scuro, estensione)`.

### Volumi

`files/volume-*` sono i dischi e i server montati, sulla keyline volume (944 × 583). Non hanno
contenuto dinamico: chi mostra un volume (barra laterale e finestre di Mustache, Scrivania,
Dock) sceglie l'icona così, dal primo caso che vale:

| Icona | Quando |
| --- | --- |
| `volume-network` | mount di rete: tipo di file system `nfs`, `nfs4`, `cifs`, `smb3`, `9p`, `fuse.sshfs`, `fuse.rclone`, `davfs`; oppure un mount GVfs con schema `smb`, `sftp`, `ftp`, `ftps`, `dav`, `davs`, `nfs`, `afp`; vale anche per un server nella barra laterale non ancora montato |
| `volume-disk-image` | dispositivo loop con un file dietro (`/dev/loop*`, interfaccia `org.freedesktop.UDisks2.Loop` con `BackingFile`): un'immagine montata, anche se è un ISO |
| `volume-optical` | unità ottica: `Drive.Optical` vero in UDisks2, oppure supporto `optical_*` in `Drive.MediaCompatibility` o dispositivo `/dev/sr*` |
| `volume-external` | unità rimovibile o esterna: `Drive.Removable` o `Drive.MediaRemovable` veri, oppure `Drive.ConnectionBus` `usb`, `sdio` o `ieee1394`; schede SD e chiavette comprese |
| `volume-internal` | tutto il resto: la radice `/`, le altre partizioni dei dischi interni (`ConnectionBus` vuoto, NVMe e SATA) e un volume di cui non si sa niente |

Senza UDisks2 (o per un mount che UDisks2 non conosce) si usano `/proc/self/mountinfo` (tipo di
file system e dispositivo) e `/sys/block/<disco>/removable`. Il nome è quello del volume
(`IdLabel`), non l'icona. La cartella `NETWORK` della cartella generica resta per le *cartelle*
di rete dentro un volume; il volume stesso è `volume-network`.

### Badge

`badges/` contiene i badge che la shell sovrappone a un'icona di file o di cartella già
composta. Non sono icone con un manifest: ogni badge è un SVG chiaro e uno scuro
(`alias.svg`, `alias-dark.svg`…) sulla tela 1024, disegnato come un disco Ø 824 centrato
(il corpo) con il simbolo nelle keyline 600 e 424. `badges/badges.json` riassume le regole sotto
per chi le implementa.

| Badge | Disegno | Angolo | Quando |
| --- | --- | --- | --- |
| `alias` | freccia curva su disco bianco (grafite in scuro) | basso a sinistra | il file è un collegamento simbolico (`lstat`); un collegamento rotto prende in più `unreadable` |
| `unreadable` | divieto (barra bianca su disco rosso) | basso a destra | l'utente non può leggerlo: `access(R_OK)` falso, per le cartelle `R_OK` o `X_OK` falso |
| `locked` | lucchetto su disco bianco (grafite in scuro) | basso a destra | il file è bloccato: attributo immutabile o solo aggiunta (`STATX_ATTR_IMMUTABLE`, `STATX_ATTR_APPEND`, `chattr +i`/`+a`); non basta che manchi il permesso di scrittura, sennò mezzo sistema avrebbe il lucchetto |
| `cloud` | nuvola blu con freccia in giù | basso a destra | il contenuto non è sul disco: lo dice chi elenca i file (un fornitore di sincronizzazione, un mount GVfs o rclone con file solo in rete). Non c'è uno standard freedesktop: Mustache lo mostra solo quando la sorgente lo riporta |

Posizione e dimensione (tela 1024 dell'icona; lato dell'icona in pt, cioè la tela intera come
per la cartella generica e l'etichetta, vedi Principio):

| Lato dell'icona | Lato del badge | Riquadro, basso a sinistra | Riquadro, basso a destra | Quanti |
| --- | --- | --- | --- | --- |
| da 32 pt | 315 = 824 / φ² | x 100…415, y 609…924 | x 609…924, y 609…924 | uno per angolo |
| 16–31 pt | 509 = 824 / φ | x 100…609, y 415…924 | x 415…924, y 415…924 | uno solo |
| sotto 16 pt | — | — | — | nessuno |

- Il riquadro va dal bordo del corpo delle app (100…924) alla linea aurea: il badge è appoggiato
  a quell'angolo, non al disegno. Il foglio (x 170…854, y 60…964) è più stretto e più alto del
  corpo, quindi il badge ne esce un poco a sinistra e sta sopra il fondo del foglio; cartelle
  (x 40…984) e volumi sono più larghi del corpo, quindi il badge sta dentro il disegno.
- Da verificare con la nuova regola del lato: nel Finder a icone da 128 pt il badge dell'alias
  misura Ø ≈ 34 (0,27 della tela, da x ≈ 0,08 e fino a ≈ 1 pt dal fondo della tela), qui Ø 315 /
  1024 = 0,31. Prima Mustache disegnava le icone dei file al 92 %, quindi il badge resa era 0,28;
  la geometria non è cambiata in questa versione.
- Composizione: la tela 1024 del badge si scala di k = lato / 824 e si sposta perché il suo
  corpo (100, 100, 824, 824) coincida con il riquadro: origine della tela del badge =
  (x₀ − 100 k, y₀ − 100 k). Si disegna dopo l'icona, dopo la tinta della cartella e dopo la
  mappatura del tema: il badge non si tinge e non passa per Clear o Tinted.
- Varianti: `-dark` nei temi Dark, Clear Dark e Tinted Dark; la chiara negli altri.
- Precedenze: in basso a destra vince `unreadable`, poi `locked`, poi `cloud` (gli altri non
  si mostrano). Sotto 32 pt resta un solo badge, il primo di `order`: `unreadable`, `alias`,
  `locked`, `cloud`.
- Nessuna ombra né bordo luminoso dalla shell: il disco ha già il suo filo di contorno (nero
  15 % in chiaro, bianco 20 % in scuro, bianco pieno attorno al divieto).
- Il badge segue lo stato dell'icona (selezione, trascinamento, ombra della cella): fa parte
  dell'icona composta. Nel Dock e in Faro non si mostra.

Riferimento: `tools/compose.py`, `compose_badges(icona, nomi, scuro)`.

`design/app-icons.sketch`: i tipi di file, i volumi e i badge sono nella pagina Icons (righe da
y 15280: file, volumi, badge), in Grid Check con le griglie e in Showcase Files in chiaro e
scuro (da y 19200, una riga per icona).

### Cartella generica

`files/folder-generic` è la cartella su cui la shell (e Mustache) incide un simbolo di
`symbols/`: le cartelle speciali (Documenti, Download, Immagini, Home…) e le cartelle con una
tinta. I livelli sono quelli della cartella (`files/folder`), senza simbolo.

```json
"dynamic": {
  "type": "folder-symbol",
  "symbol": {
    "box": [353.9, 424.36, 316.19, 316.19],
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
               "APPLICATIONS": "square-grid-2x2", "LIBRARY": "books-vertical", "SHARED": "person-2",
               "NETWORK": "network" },
  "fallback": "folder"
}
```

Proporzioni (tela 1024, keyline cartella):

| Misura | Valore | Da dove viene |
| --- | --- | --- |
| Pannello anteriore | 944 × 619 da (40, 273,1), centro (512, 582,5) | la cartella: 0,815 dell'altezza 760 |
| Area viva del simbolo (Ø 20 u) | 263,5 | 230 (serie A, 600 / φ²) sulla cartella da 824, × 1,1456 |
| Tela del simbolo (24 u), `box` | 316,2 × 316,2 a (353,9, 424,4), centrata sul pannello: 1 u = 13,2 px | area viva × 24 / 20 |
| Tratto | Light 15,6 · Regular 19,8 · Semibold 28,3 | 1,18 · 1,5 · 2,15 u: sulla cartella da 824 erano 13,6 · 17,3 · 24,7, gli spessori 13,5 e 17 della serie |
| Simbolo piccolo (`scale` 1,272) | tela 402, area viva 335 | × √φ |
| Scavo (`offset`) | 4 px, almeno mezzo pixel reso | ≈ tratto Light / φ³ |

- **Simbolo**: `symbols/<weight>/<nome>.svg` dello stesso repo, colorato al posto di
  `currentColor`, centrato in `box` e scalato di `scale` attorno al centro. La fascia è la prima
  di `sizes` con `min_size` ≤ lato dell'icona in pt (la tela intera, vedi Principio);
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
