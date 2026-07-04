<h4 align="right">
  <a href="README_zh.md">简体中文</a> | English
</h4>

> **Fork** of [XiaoYouChR/Ghost-Downloader-3](https://github.com/XiaoYouChR/Ghost-Downloader-3) — adds **vsd (Rust)** as alternative HLS/DASH engine, signed Firefox extension, and updated install guide.

> [!NOTE]
> Due to academic commitments, upstream development has slowed down. This fork adds practical improvements for daily use.

<!-- PROJECT LOGO -->
<div align="center">

![Banner](.github/assets/banner.webp)

<a href="https://trendshift.io/repositories/13847" target="_blank"><img src="https://trendshift.io/api/badge/repositories/13847" alt="chethan62/Ghost-Downloader-3 | Trendshift" style="width: 250px; height: 55px;"/></a>

### AI-powered next-generation cross-platform multithreaded downloader

[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Release][release-shield]][release-url]
[![Downloads][downloads-shield]][release-url]

##### [Releases](https://github.com/chethan62/Ghost-Downloader-3/releases) · [Report Bug](https://github.com/chethan62/Ghost-Downloader-3/issues/new?template=bug_report.yml) · [Request Feature](https://github.com/chethan62/Ghost-Downloader-3/issues/new?template=feature_request.yml)

</div>

<!-- ABOUT THE PROJECT -->
## About The Project

* A downloader built out of passion — Python + Qt (PySide6) + Fluent UI
* Originally created to help a Bilibili creator integrate resources
* **Fork improvements**:
  - **vsd (Rust)** — 27 MB single binary, 5 ms startup, replaces N_m3u8DL-RE for HLS/DASH
  - **Signed Firefox extension** — installs directly, no dev mode needed
  - **Download Engine selector** — choose N_m3u8DL-RE (full features) or vsd (speed)

| Platform | Required Version | Architectures | Compatible |
|:--------:|:----------------:|:-------------:|:----------:|
| 🐧 Linux  | `glibc 2.35+`   | `x86_64`/`arm64` | ✅ |
| 🪟 Windows | `7 SP1+`      | `x86_64`/`arm64` | ✅ |
| 🍎 macOS  | `13.0+`        | `x86_64`/`arm64` | ✅ |
| 🤖 Android | `9.0+`        | `arm64-v8a`     | ✅ |

> [!WARNING]
> Qt `6.6+` no longer supports CPUs without the `AVX` instruction set.

## Features

* **IDM-style chunked downloads** ⚡ — multi-threaded HTTP, resume support
* **Multi-protocol** 🌐 — HTTP, Magnet/BitTorrent, FTP, M3U8 (HLS), MPEG-DASH
* **Live HLS recording** 📺 — real-time decryption 🔓, Android supported
* **Browser extension** 🦊 — sniffs media (HLS, DASH, MP4, audio, images) off pages
* **Pause / edit / resume** ✏️ — change URL, headers, proxy mid-download
* **Android app** 📱 — background downloads, notifications
* **AI smart acceleration** 🚀 — dynamic chunk rebalancing

## Installation

### Desktop App (Linux / Windows / macOS)

```bash
# Option 1: pipx (recommended — isolated, auto-updates)
# Uses Python 3.11 (libtorrent doesn't have 3.14 wheels yet)
pipx install git+https://github.com/chethan62/Ghost-Downloader-3.git --python python3.11

# Option 2: from source
git clone https://github.com/chethan62/Ghost-Downloader-3.git
cd Ghost-Downloader-3
pipx install . --python python3.11

# Run
Ghost-Downloader-3
```

**Dependencies** (installed automatically):
- Python 3.11+ (use `--python python3.11` — libtorrent has no 3.14 wheels yet)
- PySide6 (Qt 6)
- libtorrent, ffmpeg, m3u8, mpegdash, yt-dlp

**Desktop shortcut**: Auto-created on first launch. Appears as "Ghost Downloader 3" in KDE/GNOME launcher.

**Arch Linux** (AUR):
```bash
yay -S ghost-downloader-git  # community package tracks upstream
```

### Browser Extension

| Browser | Install Method |
|---------|----------------|
| **Firefox** (easiest) | 1. Download `ghost-downloader-firefox-2.0.2-signed.xpi` from [Releases](https://github.com/chethan62/Ghost-Downloader-3/releases/tag/v2.0.2-fork)<br>2. Open in Firefox → **Add** |
| **Chrome / Edge / Brave / Vivaldi** | 1. Download `ghost-downloader-chrome-2.0.2.zip` from [Releases](https://github.com/chethan62/Ghost-Downloader-3/releases/tag/v2.0.2-fork)<br>2. Unzip → `chrome://extensions` → **Developer mode** → **Load unpacked** → select folder |

### Connect Extension to Desktop App

1. Open **Ghost Downloader** desktop app
2. Settings → **Browser Extension** → **Start Browser Extension Server** (port 15151 by default)
3. Click extension toolbar icon → **Pair** → **Auto Pair**
4. Confirm pairing in desktop app popup

## Usage

1. **Visit a video page** (YouTube, Bilibili, Dailymotion, generic HLS/DASH)
2. **Click extension icon** → **Resources** tab shows sniffed streams:
   - HLS (`.m3u8`) — with variant quality ladder
   - DASH (`.mpd`) — audio/video tracks separated
   - Direct MP4/WebM, audio, images
4. **Select** → **Send to Desktop** → downloads in Ghost Downloader
5. **Monitor** progress in desktop app (IDM-style chunks, resume, speed limit)

### Download Engine: N_m3u8DL-RE vs vsd

Settings → **M3U8** → **Download Engine**:

| Engine | Size | Startup | Features |
|--------|------|---------|----------|
| **N_m3u8DL-RE** (default) | 50 MB + .NET | ~300 ms | Ad filtering, rate limit, live recording, MSS, binary merge |
| **vsd (Rust)** | 27 MB | **~5 ms** | HLS/DASH, DRM keys, resume, subtitles, concurrent segments |

For most sites: **vsd is faster to start**. Use N_m3u8DL-RE if you need ad filtering or MSS.

## Roadmap (Fork)

- ✅ vsd (Rust) as alternative HLS engine
- ✅ Signed Firefox extension
- ⏳ Native Rust download engine (lower memory)
- ⏳ Public plugin API
- ⏳ eD2k protocol

## Contributing

1. Fork the Project
2. Create Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the **GPL v3.0** License. See `LICENSE` for details.

Copyright © 2024-2026 XiaoYouChR (upstream), chethan62 (fork).

## Contact

- **Fork issues**: [chethan62/Ghost-Downloader-3/issues](https://github.com/chethan62/Ghost-Downloader-3/issues)
- **Upstream**: XiaoYouChR@qq.com | [QQ Group](https://qm.qq.com/q/gPk6FR1Hby)

## Acknowledgments

* [cat-catch](https://github.com/xifangczy/cat-catch) — browser sniffing (vendored in extension)
* [vsd](https://github.com/clitic/vsd) — Rust HLS/DASH engine (forked to [chethan62/vsd](https://github.com/chethan62/vsd) with `--percent-only`)
* [N_m3u8DL-RE](https://github.com/nilaoda/N_m3u8DL-RE) — C# HLS/DASH engine
* [FFmpeg](https://ffmpeg.org/) • [yt-dlp](https://github.com/yt-dlp/yt-dlp) • [libtorrent](https://github.com/arvidn/libtorrent)
* [PySide6](https://github.com/PySide/pyside-setup) • [Fluent UI](https://github.com/zhiyiYo/PyQt-Fluent-Widgets)

---

[forks-shield]: https://img.shields.io/github/forks/chethan62/Ghost-Downloader-3.svg?style=for-the-badge
[forks-url]: https://github.com/chethan62/Ghost-Downloader-3/network/members
[stars-shield]: https://img.shields.io/github/stars/chethan62/Ghost-Downloader-3.svg?style=for-the-badge
[stars-url]: https://github.com/chethan62/Ghost-Downloader-3/stargazers
[issues-shield]: https://img.shields.io/github/issues/chethan62/Ghost-Downloader-3.svg?style=for-the-badge
[issues-url]: https://github.com/chethan62/Ghost-Downloader-3/issues
[release-shield]: https://img.shields.io/github/v/release/chethan62/Ghost-Downloader-3?style=for-the-badge
[release-url]: https://github.com/chethan62/Ghost-Downloader-3/releases/latest
[downloads-shield]: https://img.shields.io/github/downloads/chethan62/Ghost-Downloader-3/total?style=for-the-badge