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
- Specifica del formato: `docs/icon-format.md` (da scrivere).

## Sorgente di design

Il file Sketch `app-icons.sketch` è la sorgente di design; `tools/` lo esporta nei livelli
SVG di ogni icona. I file esportati sono quelli che fanno fede per la build.

## Licenza

- Icone e file grafici: [CC BY-SA 4.0](LICENSE). Si possono usare e modificare, anche
  per scopi commerciali, citando Silica e rilasciando le modifiche con la stessa licenza.
- Codice in `tools/`: MIT OR Apache-2.0, come il repo `silica`.

## Regole

Valgono le regole clean-room di `silica/AGENTS.md`: nessun asset, nome o file di sistema
Apple; ogni asset ha una riga in `ASSETS.md`.
