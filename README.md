<div align="center">

```
     ___    ____       _____ ______ ____  ____ ____  ____  ______ ____  
    /   |  /  _/      / ___//_  __// __ \/  _// __ \/ __ \/ ____// __ \ 
   / /| |  / /        \__ \  / /  / /_/ // / / /_/ / /_/ / __/  / /_/ / 
  / ___ |_/ /        ___/ / / /  / _, _// / / ____/ ____/ /___ / _, _/  
 /_/  |_/___/       /____/ /_/  /_/ |_/___//_/   /_/   /_____//_/ |_|   
```

# ⚡ AI-STRIPPER

### *Advanced Image Metadata & Synthetic Fingerprint Vaporizer*
**The Sexiest, Most Powerful Interactive Terminal App (TUI) & Engine for 100% Incognito Photos**

<p align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.8+"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-2ea44f?style=for-the-badge" alt="License: MIT"></a>
  <a href="https://github.com/Textualize/rich"><img src="https://img.shields.io/badge/UI-Interactive%20TUI-7928CA?style=for-the-badge&logo=gnometerminal&logoColor=white" alt="Interactive TUI"></a>
  <a href="#"><img src="https://img.shields.io/badge/Privacy-100%25%20Offline-0052CC?style=for-the-badge&logo=auth0&logoColor=white" alt="100% Offline"></a>
  <a href="#"><img src="https://img.shields.io/badge/Security-C2PA%20Purged-ff007f?style=for-the-badge" alt="C2PA Purged"></a>
  <a href="#"><img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=for-the-badge" alt="Cross-Platform"></a>
  <a href="#"><img src="https://img.shields.io/badge/PRs-Welcome-brightgreen?style=for-the-badge" alt="PRs Welcome"></a>
</p>

<p align="center">
  <b>Vaporize C2PA Manifests • Erase GPS Geotags • Strip AI Prompts • Purge Hardware EXIF</b><br>
  <i>Zero visual quality loss. Zero color distortion. Zero sideways photos.</i>
</p>

---

</div>

## 📑 Table of Contents

- [⚡ Why AI-STRIPPER? The Threat Matrix](#-why-ai-stripper-the-threat-matrix)
- [🖥️ Interactive Terminal Application (TUI)](#️-interactive-terminal-application-tui)
- [🔍 Deep Privacy Audit & Threat Meter](#-deep-privacy-audit--threat-meter)
- [🚀 Quick Start & Installation](#-quick-start--installation)
- [⌨️ Keyboard-First Terminal Controls](#️-keyboard-first-terminal-controls)
- [🤖 CLI Automation & Headless Power Mode](#-cli-automation--headless-power-mode)
- [🛠️ Full CLI Flag Cheat Sheet](#️-full-cli-flag-cheat-sheet)
- [🐍 Python Developer Library API](#-python-developer-library-api)
- [🔄 CI/CD & Pre-Commit Hook Integration](#-cicd--pre-commit-hook-integration)
- [🧠 Technical Architecture: Under the Hood](#-technical-architecture-under-the-hood)
- [📊 Supported Formats](#-supported-formats)
- [🤝 Contributing & Community](#-contributing--community)
- [📄 License](#-license)

---

## ⚡ Why AI-STRIPPER? The Threat Matrix

Most image cleaners only delete basic EXIF tags and fail against modern surveillance and generative tracking. Worse, naive scripts degrade photos by washing out colors or rotating portraits sideways.

| Feature / Threat Defense | Naive Scripts (`PIL.save`) | `exiftool -all=` | Web Cleaners | ⚡ **AI-STRIPPER** |
| :--- | :---: | :---: | :---: | :---: |
| **GPS Geotags & Device Serial #s** | ⚠️ Partial | ✅ Yes | ✅ Yes | **✅ 100% Purged** |
| **C2PA / Content Credentials** | ❌ Missed | ⚠️ Inconsistent | ❌ Missed | **✅ Completely Vaporized** |
| **AI Generation Prompts (SD / MJ / ComfyUI)** | ❌ Missed | ⚠️ Partial | ❌ Missed | **✅ Fully Erased** |
| **Color Preservation (ICC to sRGB)** | ❌ **Washed Out** | ❌ **Color Shift** | ❌ **Washed Out** | **✅ Zero Color Shift** |
| **Auto-Transposition (Orientation)** | ❌ **Sideways Photos** | ⚠️ Complex | ❌ Broken | **✅ Perfectly Oriented** |
| **Interactive Terminal App (TUI)** | ❌ None | ❌ None | ❌ None | **✅ Arrow-Navigable TUI** |
| **Multi-Threaded Parallel Engine** | ❌ Single-core | ❌ Slow | ❌ Cloud Upload | **✅ Blazing Multi-Core** |
| **Data Privacy & Security** | ✅ Local | ✅ Local | ❌ Third-party server | **✅ 100% Offline & Air-Gapped** |

### ⚠️ The Pitfalls Solved by AI-STRIPPER:
1. **The ICC Color Trap**: Photos taken on modern iPhones and cameras use the **Display P3** or **Adobe RGB** wide-color gamut. When traditional tools delete the ICC profile header, displays default to sRGB, causing the photo to look **dull, muddy, and desaturated**. AI-STRIPPER mathematically converts pixels to sRGB *before* stripping, ensuring identical, vibrant colors.
2. **The Sideways Photo Bug**: Mobile sensors capture raw pixels upside-down or sideways and rely on an EXIF orientation flag. Deleting EXIF naively turns vertical portraits sideways. AI-STRIPPER applies hardware transposition *first*, permanently freezing the correct orientation.
3. **C2PA & Synthetic Tracking**: Modern software (Photoshop, DALL-E, Leica, Midjourney) embeds JUMBF metadata manifests that track provenance and edit history. AI-STRIPPER writes a pristine pixel raster container, leaving zero digital provenance traces.

---

## 🖥️ Interactive Terminal Application (TUI)

Launch the full interactive terminal application with one simple command:

```bash
python stripper.py
# or if installed globally:
ai-stripper
```

### 🎮 The TUI Experience:
- **Arrow-Key Navigation**: Navigate smoothly using <kbd>↑</kbd> / <kbd>↓</kbd> or <kbd>k</kbd> / <kbd>j</kbd>.
- **Instant Shortcuts**: Press <kbd>1</kbd>–<kbd>8</kbd> to jump straight to any option.
- **Tab Autocomplete**: Real-time path autocompletion powered by `prompt_toolkit`.
- **Live Unstripped Counter**: Displays how many uncleaned images are queued in your default folder.

```text
     ___    ____       _____ ______ ____  ____ ____  ____  ______ ____  
    /   |  /  _/      / ___//_  __// __ \/  _// __ \/ __ \/ ____// __ \ 
   / /| |  / /        \__ \  / /  / /_/ // / / /_/ / /_/ / __/  / /_/ / 
  / ___ |_/ /        ___/ / / /  / _, _// / / ____/ ____/ /___ / _, _/  
 /_/  |_/___/       /____/ /_/  /_/ |_/___//_/   /_/   /_____//_/ |_|   
    IMAGE METADATA STRIPPER & PRIVACY SHIELD  v2.1.0

  Use [↑ / ↓ / j / k] to navigate  •  [Enter] to select  •  [q] to quit

 ❯ [1] ⚡ Quick Strip Default Folders  images to be stripped/ ➔ stripped/ [16 items]
   [2] 📁 Batch Strip Directory Wizard  Pick custom folder, recursion, quality, output
   [3] 🖼️  Strip Single Image  Target a specific image file with custom destination
   [4] 🔍 Inspect & Audit Metadata  Deep privacy scan: GPS map link, AI prompts, C2PA
   [5] ⚙️  Settings & Preferences  sRGB: ON • Q: 100 • Threads: 8
   [6] 📊 Engine Info & Benchmarks  View Pillow features, CPU cores, supported formats
   [7] 📖 Help & Privacy Threat Guide  Detailed manual on what gets purged and why
   [8] 🚪 Exit Application  Quit the terminal application
```

---

## 🔍 Deep Privacy Audit & Threat Meter

Curious what your photos are broadcasting to the world? Audit any file with the built-in inspector:

```bash
ai-stripper --inspect "sample_photo.jpg"
```

### 📋 Live Audit Output Sample:
```text
┌─  🔍 AI-STRIPPER Privacy & Fingerprint Audit: photo.jpg  [CRITICAL]  ──────┐
│  Threat Level Meter              ■■■■■■■■■■ 100% CRITICAL LEAK             │
│  File Size                       4.2 MB (4,404,019 bytes)                  │
│  Format & Mode                   JPEG (RGB)                                │
│  Dimensions                      4032 x 3024 px                            │
│  Color Profile                   Display P3 (Wide Gamut)                   │
│  C2PA Content Credentials        ⚠️ Detected (Provenance Tracking)         │
└────────────────────────────────────────────────────────────────────────────┘

┌─ 🚨 SENSITIVE GPS GEOLOCATION FOUND ───────────────────────────────────────┐
│  Latitude                        37.774929°                                │
│  Longitude                       -122.419416°                              │
│  Altitude                        14.2 m                                    │
│  Google Maps Link                https://www.google.com/maps/search/...    │
└────────────────────────────────────────────────────────────────────────────┘

┌─ 🤖 AI Generation Metadata (Prompts & Settings) ───────────────────────────┐
│  parameters                      masterpiece, ultra-detailed cyberpunk city│
│                                  Steps: 30, Sampler: DPM++ 2M Karras, CFG: 7│
└────────────────────────────────────────────────────────────────────────────┘

┌─ 📷 EXIF Camera & Hardware Metadata (34 tags total) ───────────────────────┐
│  Make                            Apple                                     │
│  Model                           iPhone 15 Pro Max                         │
│  LensModel                       iPhone 15 Pro Max back triple camera      │
│  DateTimeOriginal                2026:09:24 18:42:10                       │
└────────────────────────────────────────────────────────────────────────────┘

⚠️  Recommendation: This image contains sensitive private metadata. Strip with AI-STRIPPER before publishing.
```

---

## 🚀 Quick Start & Installation

### Option 1: Standard Clone & Run

```bash
# 1. Clone repository
git clone https://github.com/zimkk/openai-stripper.git
cd openai-stripper

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch Interactive Terminal App!
python stripper.py
```

### Option 2: Install as a Global CLI Tool

Using `pip install -e .`, install AI-STRIPPER globally:

```bash
pip install -e .
```

Now launch it from **any folder** in your terminal:
```bash
ai-stripper
```

---

## ⌨️ Keyboard-First Terminal Controls

| Keybinding | Action |
| :---: | :--- |
| <kbd>↑</kbd> or <kbd>k</kbd> | Move menu cursor **Up** |
| <kbd>↓</kbd> or <kbd>j</kbd> | Move menu cursor **Down** |
| <kbd>Enter</kbd> | Select active item / confirm action |
| <kbd>1</kbd> – <kbd>8</kbd> | Instant shortcut to menu item |
| <kbd>Tab</kbd> | Autocomplete file & directory paths |
| <kbd>q</kbd> or <kbd>Ctrl+C</kbd> | Return to previous menu / Quit application |

---

## 🤖 CLI Automation & Headless Power Mode

AI-STRIPPER features a dual-engine architecture: run with no arguments for the **Interactive TUI**, or provide command-line flags for **Automated Pipelines & Scripts**.

### ⚡ 1. Batch Process a Directory
```bash
ai-stripper -i ./raw_photos -o ./clean_photos
```

### 🔄 2. Recursive Scan with Suffix & Quality Tuning
```bash
ai-stripper -i ./photos -o ./clean -r -q 95 --suffix "_clean"
```

### ⚠️ 3. In-Place Overwrite (Sanitize In-Place)
```bash
ai-stripper -i ./public_assets --in-place
```

### 🎯 4. Convert Image Formats While Stripping
```bash
ai-stripper -i ./avatars -o ./webp_avatars --format webp
```

### 🔍 5. Audit an Image Without Modifying
```bash
ai-stripper --inspect sensitive_photo.png
```

### ⚡ 6. Tune Worker Threads for Huge Libraries
```bash
ai-stripper -i ./large_dataset -o ./dataset_clean -w 16
```

---

## 🛠️ Full CLI Flag Cheat Sheet

| Flag | Short | Type | Default | Description |
| :--- | :---: | :---: | :---: | :--- |
| `--input` | `-i` | `PATH` | `None` | Path to source image file or directory |
| `--output` | `-o` | `PATH` | `None` | Path to destination file or directory |
| `--quality` | `-q` | `INT` | `100` | Output compression quality (1-100) for JPEG / WebP |
| `--recursive` | `-r` | `FLAG` | `False` | Recursively scan nested subdirectories |
| `--suffix` | `-s` | `STR` | `""` | Append custom suffix to output filenames (e.g. `_clean`) |
| `--format` | - | `CHOICE` | `original` | Format conversion: `original`, `jpg`, `png`, `webp` |
| `--in-place` | - | `FLAG` | `False` | Overwrite source files in-place |
| `--inspect` | - | `PATH` | `None` | Audit and display metadata without modifying files |
| `--workers` | `-w` | `INT` | `Auto` | Number of concurrent worker threads |
| `--no-srgb` | - | `FLAG` | `False` | Skip automatic ICC profile to sRGB conversion |
| `--no-orient` | - | `FLAG` | `False` | Skip hardware EXIF orientation auto-transposition |
| `--no-anim` | - | `FLAG` | `False` | Disable cyberpunk startup and exit animations |
| `--interactive`| `-I` | `FLAG` | `False` | Force interactive TUI mode even if flags are present |
| `--version` | `-v` | `FLAG` | - | Print version and exit |
| `--help` | `-h` | `FLAG` | - | Show command-line help screen |

---

## 🐍 Python Developer Library API

Import AI-STRIPPER directly into your Python automation scripts, web services, or Flask/FastAPI backends!

```python
from pathlib import Path
from stripper import strip_image_metadata, inspect_image_metadata

# 1. Audit an image programmatically
audit = inspect_image_metadata(Path("user_upload.jpg"))
print(f"Risk Level: {audit['risk_level']}")
if audit["gps"]:
    print(f"GPS Found: {audit['gps']['latitude']}, {audit['gps']['longitude']}")

# 2. Strip metadata cleanly
result = strip_image_metadata(
    input_path=Path("user_upload.jpg"),
    output_path=Path("user_upload_clean.jpg"),
    quality=95,
    convert_srgb=True,
    auto_orient=True
)

print(f"Cleaned! Space saved: {result['saved_bytes'] / 1024:.1f} KB")
```

---

## 🔄 CI/CD & Pre-Commit Hook Integration

Automatically strip sensitive metadata before committing images to your Git repositories!

### 1. `.pre-commit-config.yaml`
```yaml
repos:
  - repo: local
    hooks:
      - id: ai-stripper
        name: Sanitize Image Metadata
        entry: ai-stripper --in-place -i
        language: system
        types: [image]
```

### 2. GitHub Actions (`.github/workflows/strip-metadata.yml`)
```yaml
name: Sanitize Images on Pull Request

on:
  pull_request:
    paths:
      - '**.png'
      - '**.jpg'
      - '**.jpeg'
      - '**.webp'

jobs:
  strip-metadata:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install Dependencies
        run: pip install -r requirements.txt
      - name: Strip Images
        run: python stripper.py -i ./docs/images -r --in-place
```

---

## 🧠 Technical Architecture: Under the Hood

```
   ┌─────────────────────────────────────────────────────────────┐
   │                   Raw Input Image File                      │
   │  [EXIF] [GPS] [C2PA JUMBF] [AI Prompts] [Wide ICC Profile]  │
   └──────────────────────────────┬──────────────────────────────┘
                                  │
                                  ▼
                   Step 1: EXIF Auto-Transpose
         (Transforms physical pixels to eliminate sideways bug)
                                  │
                                  ▼
             Step 2: Color Gamut Management (LCMS)
     (Converts Display-P3 / Adobe-RGB pixels to standard sRGB)
                                  │
                                  ▼
            Step 3: Pristine Pure Buffer Reconstruction
       (Allocates brand-new Image.new() buffer; zero info copy)
                                  │
                                  ▼
                   Step 4: Safe Re-Encoding
        (Encodes with pure scanlines; zero ancillary chunks)
                                  │
                                  ▼
   ┌─────────────────────────────────────────────────────────────┐
   │                  Sanitized Output Image                     │
   │      100% Visual Fidelity • 0% Metadata Trace Left          │
   └─────────────────────────────────────────────────────────────┘
```

---

## 📊 Supported Formats

| Format | Extensions | Metadata Removed | Transparency |
| :---: | :---: | :--- | :---: |
| **PNG** | `.png` | Text chunks (`tEXt`, `zTXt`, `iTXt`), ICC, C2PA, XMP | Preserved (RGBA) |
| **JPEG** | `.jpg`, `.jpeg` | EXIF, GPS, IPTC, XMP, JUMBF/C2PA APP11 markers | Alpha blended onto White |
| **WebP** | `.webp` | EXIF, XMP, ICC, animation comment headers | Preserved |
| **TIFF** | `.tiff`, `.tif` | GeoTIFF tags, Camera & Lens tags, Software IDs | Preserved |
| **BMP** | `.bmp` | Device headers and color masks | Preserved |
| **GIF** | `.gif` | Application extensions, user comments | Preserved |

---

## 🤝 Contributing & Community

Contributions, issues, and feature requests are welcome!

1. **Fork the Repository**
2. **Create your Feature Branch** (`git checkout -b feature/CoolNewFeature`)
3. **Commit your Changes** (`git commit -m 'feat: Add AVIF support'`)
4. **Push to the Branch** (`git push origin feature/CoolNewFeature`)
5. **Open a Pull Request**

---

## 📄 License

This project is licensed under the **MIT License** — see the [`LICENSE`](LICENSE) file for details.

<div align="center">
  <b>Built with ⚡ for privacy advocates, photographers, and open-source creators worldwide.</b>
</div>
