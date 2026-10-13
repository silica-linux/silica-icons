# silica-icons

Icone di Silica: app, cartelle e file, simboli di sistema. Tutte originali, disegnate
per il progetto.

## Struttura

```
apps/      icone delle app, a livelli: la shell applica forma, ombre, vetro e temi
files/     cartelle, tipi di file, Cestino, controlli del Dock: a livelli, forma libera
symbols/   glifi di sistema (Centro di controllo, barra dei menu, impostazioni, barre
           degli strumenti): monocromi, vettoriali, più pesi, colorati dal tema
tools/     esportazione dal file di design e build dei pacchetti
docs/      specifiche: formato delle icone, griglia, temi
```

## Modello

- Le icone delle app non contengono forma né ombra: lo sviluppatore fornisce un fondo e
  fino a quattro gruppi di livelli SVG sulla griglia 1024; la shell ritaglia con la
  maschera (corpo 824, angoli smooth r 215), aggiunge bordo, ombre e vetro e genera i temi
  Default, Dark, Clear Light, Clear Dark, Tinted Light, Tinted Dark.
- Le icone senza livelli (tema freedesktop esistente) vengono ridotte al keyline 600 e
  appoggiate su una base neutra.
- Specifica del formato: [`docs/icon-format.md`](docs/icon-format.md).

## Sorgente di design

`design/app-icons.sketch` è la sorgente di design (pagine Grid, Icons, Grid Check,
Showcase, Showcase Files, Showcase Desktop, Dynamic Icons). Da lì si esportano i livelli
SVG di ogni icona; i file esportati sono quelli che fanno fede per la build.

## Strumenti

```
python3 -m venv venv && venv/bin/pip install pillow resvg-py
venv/bin/python tools/compose.py --fonts <cartella con Inter> --out build/sheet-light.png
venv/bin/python tools/compose.py --dark --fonts <cartella con Inter> --out build/sheet-dark.png
```

`compose.py` ricompone ogni icona dai suoi livelli come farebbe la shell e scrive un
foglio di controllo.

## Contenuto

- `apps/`: 17 app (apps, calculator, calendar, clock, disks, fonts, help, mail, mustache,
  notes, password-manager, photo-viewer, photos, settings, store, terminal, text-editor)
  con varianti scure; calendar e clock sono dinamiche.
- `files/`: cartella, 8 tipi di file, file generico (estensione scritta dalla shell),
  Cestino vuoto e pieno, Stack Close.
- `symbols/`: 303 simboli in 11 categorie, generati da `tools/symbols/symbols.py`
  (`export_svg.py --check` verifica che gli SVG corrispondano alla sorgente). Specifica:
  [`docs/symbol-format.md`](docs/symbol-format.md); sorgente di design `design/symbols.sketch`.

## Licenza

- Icone e file grafici: [CC BY-SA 4.0](LICENSE). Si possono usare e modificare, anche
  per scopi commerciali, citando Silica e rilasciando le modifiche con la stessa licenza.
- Codice in `tools/`: MIT OR Apache-2.0, come il repo `silica`.

## Regole

Valgono le regole clean-room di `silica/AGENTS.md`: nessun asset, nome o file di sistema
Apple; ogni asset ha una riga in `ASSETS.md`.
