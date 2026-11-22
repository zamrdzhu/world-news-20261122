# world-news-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/zamrdzhu/world-news-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/zamrdzhu/world-news-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A one-page newspaper front page summing up Sunday 22 November 2026's world news: 57 stories across 8 sections, led by Iran's strikes on US bases in Bahrain and Kuwait, with COP31 nearing a deal, Mexico's capture of a most-wanted cartel boss, and Japan-India defence ties. Rendered by a stdlib-only Python program (hand-drawn 5x7 bitmap type, hand-rolled PNG encoder) into a 1024x1024 image. Entry for make.fun's news-image-20261122 bounty ($100, 50 paid places).

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This writes `out/entry.png` (1024x1024, under 1 MiB). The program needs only the Python standard library, no network, and writes byte-identical output on every run.

## How it is built

- `main.py` — the whole entry: a hand-written 5x7 bitmap font (capitals, lower case, digits, punctuation), a small canvas library, a hand-rolled PNG encoder (zlib + CRC), the 57 sourced stories, and a newspaper layout engine (masthead, lead story, four flowing columns, footer).
- No fonts, no images, no libraries are loaded; every pixel is drawn by the program, so the two grading runs produce identical bytes.
- Sources for every story are listed in `SOURCES.md` (Reuters, AP, AFP, ANI, BBC, Euronews, The Guardian, ABC, ESPN, CNA, Fox News, SCMP, Nikkei Asia, IEA).

## The day in brief

Gulf crisis dominates: Iran says it struck US positions in Bahrain and hit US Patriot radars, Bahrain reports an industrial-site fire, and a tanker convoy readies to break the US blockade. Elsewhere: COP31 closes on a deal after a fossil-fuel deadlock, Mexico seizes "El Chapo Isidro", Moscow hits Kyiv's bridges after the Kerch attack, Japan and India deepen defence ties, and strong quakes shake Peru and Myanmar with no casualties reported.

---

<sub>Entered on [make.fun](https://make.fun/?ref=ta9jpaag&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
