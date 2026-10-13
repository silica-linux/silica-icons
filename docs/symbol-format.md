# Formato dei simboli

Versione 1. Vale per `symbols/`: i glifi monocromi di sistema (barra dei menu, Centro di
controllo, menu, barre degli strumenti, impostazioni). Le icone delle app e dei file seguono
[`icon-format.md`](icon-format.md).

Sorgente di design: `design/symbols.sketch` (pagine Grid, Symbols, Weights, Check, Sheet).
Tutti i simboli sono disegnati da zero: niente ricalchi, misure o file di altri set di
simboli (vedi le regole clean-room di `silica/AGENTS.md`).

## Tela e unità

| Elemento | Misura |
| --- | --- |
| Tela | 24 × 24 u, disegnata a 4× su artboard 96 × 96 px (1 u = 4 px) |
| Area viva | 20 × 20 u, margine 2 u; nessun inchiostro fuori, salvo terminali di 0,5 u al massimo |
| Centro | (12, 12) = centro delle maiuscole di Inter |
| Keyline cerchio | Ø 20 (inchiostro esterno) |
| Keyline quadrato | 18 × 18 (≈ Ø 20 × √π/2: stessa area del cerchio, correzione ottica) |
| Keyline largo | 20 × 12,36 (1 : φ) |
| Keyline alto | 12,36 × 20 (φ : 1) |

Le keyline si misurano sul bordo esterno dell'inchiostro, non sull'asse del tratto: un cerchio
Regular sulla keyline Ø 20 ha il tracciato con raggio 9,25 (10 − 0,75).

## Sistema di proporzioni (φ = 1,618)

Tutte le misure derivano da due grandezze: l'area viva (20 u) e il tratto Regular (1,5 u).

| Grandezza | Valore | Dove si usa |
| --- | --- | --- |
| Cerchi aurei | Ø 20 · 12,36 · 7,64 · 4,72 (20 / φⁿ) | lente di `search` (Ø 12,36), anelli di `share-nearby` (Ø 12,36), nucleo di `sun` e testa di `person` (≈ Ø 7,64), foro di `gear` |
| Rettangolo aureo | 1 : φ | `keyboard`, `sidebar`, `battery` (corpo 18 × 11,12), `lock` (corpo), `folder` (≈), `doc` (≈ φ : 1) |
| Sezione aurea | 1/φ² e 1/φ della larghezza | divisorio di `sidebar` (1/φ²), piega di `doc` (larghezza / φ² + 1) |
| Passo concentrico | tratto × φ² = 3,93 u (asse-asse) | archi di `wifi`, onde di `volume`, onde di `hotspot` |
| Luce fra tratti | tratto × φ = 2,43 u | conseguenza del passo: spazio libero fra due tratti paralleli |
| Livelli | 1 · 1/φ · 1/φ³ | riempimento di `battery`, `battery-50`, `battery-10` |
| Pentagramma | raggio interno = esterno / φ² | `star` (vale per ogni stella regolare a 5 punte) |
| Lancette | raggio / φ (minuti), raggio / φ² (ore) | `clock` |
| Scale | rapporto √φ = 1,272 | small, medium, large |
| Pesi | ×φ^½ e ×φ^¾ dal Regular | Light, Semibold |

Coincidenza utile: l'altezza delle maiuscole di Inter (0,7275 em) vale 12,36 u alla scala
medium. Il rettangolo aureo largo 20 × 12,36 coincide quindi con la fascia fra altezza delle
maiuscole e linea di base: un simbolo largo (tastiera, barra laterale) ha la stessa altezza
delle maiuscole del testo accanto.

### Correzioni ottiche rispetto al rapporto puro

| Simbolo | Rapporto puro | Scelto | Motivo |
| --- | --- | --- | --- |
| Quadrato | 20 | 18 | stessa area del cerchio Ø 20, altrimenti il quadrato pesa di più |
| `wifi`, `volume` | raggi in progressione φ (r, rφ, rφ²) | passo costante 3,93 u (= tratto × φ²) | con raggi in progressione φ la luce fra il primo e il secondo arco scende sotto 1 u e si chiude in Semibold |
| `sun` | nucleo Ø 7,64 | Ø 8,04 (+0,4) | i raggi corti alleggeriscono il disegno; il nucleo cresce per compensare |
| `gear` | foro Ø 7,64 | asse Ø 7,24 (−0,4) | l'anello interno a Ø 7,64 si avvicinava troppo alle radici dei denti |
| `doc` | 12,36 × 20 | 13,96 × 20 | il foglio stretto sembra più piccolo degli altri simboli alti |
| `folder` | 20 × 12,36 | 20 × 12,93 | la linguetta toglie peso al corpo; il corpo cresce di 0,6 u |
| `star` | centro (12, 12) | centro (12, 12,85) | centratura ottica: la stella ha più massa in basso |
| `play` | riquadro centrato (x 6,5–17,5) | baricentro quasi al centro (x 8–19, baricentro 11,67) | centrato sul riquadro il triangolo sembra spostato a sinistra |
| `share-nearby` | — | due cerchi Ø 12,36 con centri a ±3,82 | inviluppo esattamente Ø 20 |

## Pesi

Tratto centrato sul tracciato, terminali e giunzioni rotondi (raggio del terminale = metà del
tratto).

| Peso | Tratto (u) | em alla scala medium | Asta di Inter corrispondente |
| --- | --- | --- | --- |
| Light | 1,18 (1,5 / φ^½) | 0,069 | da verificare quando il pacchetto includerà Inter Light |
| Regular | 1,5 | 0,088 | Inter Regular "l" 0,088 |
| Semibold | 2,15 (1,5 × φ^¾) | 0,127 | Inter SemiBold "l" 0,127 |

Il simbolo ha lo stesso peso del testo accanto: un simbolo Regular sta con Inter Regular, un
Semibold con Inter SemiBold. Altri pesi (Thin, Medium, Bold) si aggiungono con lo stesso
criterio: tratto = asta di Inter di quel peso, convertita in unità della tela medium.

Le forme piene (`play`, `pause`, `moon`, `airplane`, punti) hanno riempimento **e** tratto
dello stesso colore: crescono con il peso come le linee e hanno gli angoli arrotondati dal
tratto. I riempimenti interni che non devono crescere (livello della batteria, fulmine) sono
solo riempimento.

## Scale

Tre scale con rapporto √φ. La tela si misura in em del testo accanto:

| Scala | Tela | A 13 pt | Keyline quadrato a 13 pt | Uso |
| --- | --- | --- | --- | --- |
| small | 1,111 em | 14,4 pt | 10,8 pt | voci di menu con icona, scorciatoie, etichette piccole |
| medium | 1,4126 em | 18,4 pt | 13,8 pt | barra dei menu, menu, barre degli strumenti |
| large | 1,797 em | 23,4 pt | 17,5 pt | Centro di controllo (dischi da 36 pt), pulsanti grandi |

Il tratto in punti resta quello del peso a ogni scala: in unità della tela small = tratto ×
√φ, large = tratto / √φ (Regular: small 1,91 u, medium 1,5 u, large 1,18 u). Chi esporta
una scala diversa da medium ricalcola il tratto, non lo scala con il disegno.

Verifica con le misure di riferimento (note in `silica/plan/reference/`): alla scala large a
13 pt `wifi` misura 19,9 × 15,5 pt (Centro di controllo osservato: 20 × 15); alla scala
medium le icone della barra dei menu stanno fra 12 e 16 pt di altezza (osservato: 12–18).

## Allineamento al testo

- Il centro della tela sta sul centro delle maiuscole: linea di base + 0,3638 em.
- Alla scala medium: altezza delle maiuscole a y 5,82 u, linea di base a y 18,18 u.
- Il simbolo si posiziona come un glifo: `y_tela = linea_di_base − 0,3638 em − tela / 2`.
- Spaziatura orizzontale fra simbolo e testo: decisa dal componente, non dal simbolo (la
  tela ha già 2 u di margine).

## Colore

- Monocromi: un solo colore, preso dal tema (`currentColor` negli SVG). Mai colori fissi
  nel simbolo.
- Parti secondarie (archi non attivi di `wifi-1`, onde di `volume-1`): livello di nome
  `secondary`, opacità 35 % del colore del simbolo. La shell può sostituirla con un colore
  secondario del tema.
- Nessuna ombra, sfumatura o vetro nel simbolo: li aggiunge il contesto (disco del Centro di
  controllo, pulsante).

## Varianti outline e fill

- La forma base è **outline** (tratto). Il nome senza suffisso è l'outline: `bell`, `folder`.
- La variante piena ha suffisso `-fill`: `bell-fill`, `folder-fill`, `heart-fill`. Si
  disegna per i simboli che diventano "attivi" o selezionati (barre laterali, tab bar,
  preferiti). Nella variante fill il dettaglio interno si ritaglia (sottrazione), con luce
  minima 1,5 u.
- Simboli pieni per natura (`play`, `pause`, `moon`, `airplane`) non hanno variante outline.
- Finché Sketch non conserva le sottrazioni fra sottotracciati, si disegnano `-fill` solo per le
  forme senza dettaglio interno da ritagliare, oppure col dettaglio omesso (`folder-fill` senza
  divisorio, `doc-fill` senza piega, `house-fill` senza porta); non esistono ancora
  `envelope-fill`, `tag-fill`, `checkmark-circle-fill`.

## Nomi

- kebab-case inglese, dal generale al particolare: `chevron-left`, `lock-open`,
  `battery-charging`.
- Varianti come suffisso, in quest'ordine: stato o livello, poi `-fill`.
  - livelli: `wifi-0`, `wifi-1`, `wifi-2`, `wifi` (pieno); `volume-1`, `volume-2`, `volume`;
    `battery-10`, `battery-50`, `battery` (carica).
  - barrato o disattivo: `-slash` (`wifi-slash`, `volume-slash`, `bell-slash`).
  - stati: `-open`, `-charging`; riempimento: `-fill`.
- Nomi descrittivi della forma o della funzione di sistema, mai nomi di prodotti Apple:
  `share-nearby` (non "airdrop"), `screen-cast` (non "airplay"), `airplane` per la modalità
  aereo, `moon` per la concentrazione.

## Regole di disegno

1. Partire dalla keyline giusta (cerchio, quadrato, largo, alto) e dalle grandezze auree della
   tabella; documentare nella pagina Check ogni correzione ottica.
2. Un solo spessore di tratto per simbolo; niente tratti dimezzati per i dettagli.
3. Luce minima fra tratti: 1,5 u in Regular (resta ≥ 1,2 u in Semibold).
4. Terminali rotondi; angoli interni dei contenitori r 2,4 u (≈ tratto × φ), capsule con
   raggio = metà altezza.
5. Coordinate preferibilmente su multipli di 0,25 u per i tratti orizzontali e verticali
   (a 1× medium 1 u ≈ 0,77 px: nessun allineamento al pixel è possibile, conta la coerenza).
6. Ogni sottotracciato è un livello separato (`primary` o `secondary`), così Sketch non unisce
   né sottrae i tracciati.
7. Prima di chiudere: Check (griglia sovrapposta), Weights (tre pesi e tre scale), foglio di
   controllo a 1× e 2× su chiaro e scuro accanto a Inter.

## File nel repository

```
symbols/<nome>.svg      viewBox 0 0 24 24, tratto 1,5, stroke-linecap/linejoin round,
                        colore currentColor, livelli secondari con opacity 0.35
```

I tracciati sono descritti in `tools/symbols/symbols.py` (sorgente unica per Sketch e per gli
SVG). `tools/symbols/export_svg.py` scrive `symbols/*.svg`; con `--check` verifica che i file
siano allineati alla sorgente. `tools/symbols/gen2.py` genera gli script che creano gli artboard
in `design/symbols.sketch`; `compose_sheet.py` ricompone il foglio di controllo della pagina
Sheet dai PNG esportati da Sketch. I pesi Light e Semibold come file separati non sono ancora
esportati: si ottengono ricalcolando il tratto (sezione Pesi).

## Varianti barrate e badge

- `-slash`: barra da (4,25, 4,25) a (19,75, 19,75), sopra il simbolo. I tratti sotto la barra
  si interrompono dove l'asse dista meno di 3 u dall'asse della barra (0,75 + luce 1,5 + 0,75):
  la luce minima vale anche per gli incroci.
- Badge (`bell-badge`): disco pieno; il tratto sotto si interrompe con la stessa luce.
- I tagli si calcolano in `symbols.py` (funzioni `cut`, `slashed`, `outside_shape`), mai a mano.

## Catalogo

303 simboli in 11 categorie, nell'ordine delle sezioni della pagina Symbols (12 colonne,
passo 144 px; ogni categoria ha una banda di 960 px, cioè fino a 5 righe).

| Categoria | Simboli |
| --- | --- |
| Status & Connectivity | 37 |
| Control Center & Media | 32 |
| Windows & Navigation | 40 |
| Editing & Text | 37 |
| Files & Documents | 28 |
| Communication | 24 |
| People & Security | 20 |
| Devices | 21 |
| Weather & Time | 21 |
| Shapes & Indicators | 26 |
| Settings | 17 |

Elenco completo dei nomi: `symbols/` (un file per simbolo) o la pagina Sheet di
`design/symbols.sketch`, ordinata per categoria.
