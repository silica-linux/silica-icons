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
| Angoli del corpo | smooth, raggio 215, smoothing 0,6 (superellisse n ≈ 2,6) |
| Keyline quadrato | 600 × 600 a (212, 212) |
| Keyline cerchio grande | Ø 600, centro (512, 512) |
| Keyline cerchio piccolo | Ø 424, centro (512, 512) |
| Keyline verticale | 520 × 680 a (252, 172) |
| Keyline orizzontale | 680 × 520 a (172, 252) |

Il contenuto principale sta in uno dei keyline; le icone a tutta tela (un fondo disegnato,
come Calendar o Photos) occupano il corpo intero.

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

## Icone senza livelli

Un'app che ha solo un'icona freedesktop (PNG o SVG già composto) viene ridotta al keyline
quadrato e appoggiata su un fondo neutro (bianco in chiaro, grafite in scuro).
