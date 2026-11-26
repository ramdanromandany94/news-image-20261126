# The World in One Image — 26 November 2026

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/ramdanromandany94/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/ramdanromandany94/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

Entry for the [news-image-20261126 bounty](https://make.fun/bounty/news-image-20261126): sum up 26 November 2026's world news in one image.

## What it is

A program (`main.ts`, Node 22, stdlib only) that writes a single
1024×1024 newspaper front page — **THE WORLD IN ONE IMAGE** — to
`/output/entry.png`. The page is drawn by `tools/render.py` (Pillow)
and shipped as `entry.png` next to `main.ts`.

## The day's stories (Thursday 26 November 2026)

- **Hero — Washington:** Trump's new tariff salvo sinks stocks.
  The US proposes higher duties on China, the EU and 14 others over
  subsidised factories. The Nasdaq falls 2% to the brink of a bear
  market as the AI sell-off deepens — and Taiwan says it will keep
  its 15% rate.
- **Taiwan:** Taipei says its tariff deal will hold; semiconductors
  make up more than 70% of Taiwan's exports to America.
- **United States:** A Thanksgiving nor'easter brings 60 mph gusts
  to New York; the 100th Macy's parade moves to Saturday — a first.
- **Indonesia:** Bogor mine toll rises to 9; seventeen miners are
  still believed trapped in the 100-metre shaft.
- **Australia:** Flight Centre probes a data breach — an
  unauthorised party may have accessed customer records.
- **Europe:** EU leaders meet on a security plan as Chancellor Merz
  warns of a growing threat from Russia.

Sources: Reuters, Associated Press.

## How to run

```sh
python3 tools/render.py        # draws entry.png (1024x1024)
MAKEFUN_OUTPUT_DIR=/output node main.ts   # copies it to /output/entry.png
```

## Referral

Try make.fun yourself: [make.fun/r/hxd0fhbx](https://make.fun/r/hxd0fhbx)

## License

MIT — see [LICENSE](LICENSE).
