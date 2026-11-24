# THE WORLD IN ONE DAY — Monday 23 November 2026

Entry for the make.fun competition **news-image-20261123**
("Sum up 23 November's world news in one image"), built for the
make.fun account **@super-cell**.

## What it is

A single 1024×1024 PNG drawn as a newspaper front page. Under the
masthead "THE WORLD IN ONE DAY" and the date line "MONDAY 23 NOVEMBER
2026", the page carries the day's eight verified stories:

- **Lead:** COP31 in Antalya collapses with no deal after a 49-hour
  overrun; a 130+ nation EU-led bloc rejected a draft that dropped the
  fossil-fuel phase-out; Guterres lamented the outcome.
- Ukraine's sea drones sink the Russian warship 'Merkury' at Benghazi
  port, Libya; the UN calls for a probe.
- Russian strikes kill at least 12 in the Kyiv region; a 7-year-old boy
  was pulled alive from the rubble.
- Jensen Huang returns as Nvidia CEO, shares jump about 30%; the US
  blacklists Singapore's Megaspeed over AI-chip diversion to China.
- A Delta load-calculation failure forces an FAA ground stop in
  Atlanta; 1,300 flights delayed on Thanksgiving eve.
- 'Grand Theft Auto VI' takes a $3.79B day-one haul, an entertainment
  record.
- Heavy fighting in Ituri, DR Congo, traps Ebola responders near a
  hospital (WHO).
- FIFA confirms the UK hosts the 2035 Women's World Cup; Alcaraz beat
  Zverev to win his first ATP Finals title.

Each story gets a short bold headline, a one- or two-sentence summary,
and a small icon drawn with PIL shapes (globe, ship, house, chip,
plane, game controller, medical cross, trophy). No story is invented
or embellished; the footer says so.

## How to run

```sh
python3 main.py
```

Requires Python 3 and Pillow, plus the DejaVu and Liberation fonts.
It writes `entry.png` (1024×1024, well under 1 MiB) next to `main.py`.
All text is rendered with `ImageDraw` from those system fonts and all
artwork is drawn programmatically in the same file — there are no
external assets.
