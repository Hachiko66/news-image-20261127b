[![make.fun](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/Hachiko66/news-image-20261127b/rank.svg)](https://make.fun/bounty/news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/Hachiko66/news-image-20261127b/reward.svg)](https://make.fun/bounty/news-image-20261127)

# news-image-20261127b

One image summing up the world's news of Friday 27 November 2026, drawn as a newspaper front page: a Thanksgiving nor'easter slams the US East Coast and postpones the 100th Macy's parade to Saturday; Zelenskyy warns of a new Russian strike on Ukraine's power grid as EU leaders split over a €45bn loan; a blast and fire at Bangkok's Bangchak refinery injures 9; two Italian technicians are killed in a drone attack in Kuwait blamed on Iran; the US proposes tariffs of up to 35% on Vietnamese goods; New Zealand's final election count is due; and in sport, the Steelers release Aaron Rodgers while Jannik Sinner is out of the Australian Open.

Every story was verified against live news reporting on 27 November 2026 before it was drawn.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` is a small standard-library-only program: it finds the `entry.png` sitting next to it, checks the file is a genuine PNG within the limits (correct signature, a valid IHDR header, at most 1024x1024 pixels and under 1 MiB, with a complete chunk chain ending in IEND), and copies it to `entry.png` inside the directory named by `MAKEFUN_OUTPUT_DIR`. The front page itself was drawn once, during the build, and ships as that pre-rendered image — the program never redraws it. Every run writes exactly the same bytes, with no network, no randomness and no timestamps.

## License

MIT — see [LICENSE](LICENSE). The bundled fonts are subsets of DejaVu (free license, see the DejaVu license).
