<div align="center">

```
     ___    ____       _____ ______ ____  ____ ____  ____  ______ ____  
    /   |  /  _/      / ___//_  __// __ \/  _// __ \/ __ \/ ____// __ \ 
   / /| |  / /        \__ \  / /  / /_/ // / / /_/ / /_/ / __/  / /_/ / 
  / ___ |_/ /        ___/ / / /  / _, _// / / ____/ ____/ /___ / _, _/  
 /_/  |_/___/       /____/ /_/  /_/ |_/___//_/   /_/   /_____//_/ |_|   
```

# ⚡ AI-STRIPPER

### *The Free, Open-Source OpenAI & Google Gemini Metadata Vaporizer*

<p align="center">
  <a href="https://github.com/zimkk"><img src="https://img.shields.io/badge/Author-zimkk-black?style=for-the-badge&logo=github&logoColor=white" alt="Author zimkk"></a>
  <a href="https://github.com/zimkk/openai-stripper"><img src="https://img.shields.io/badge/OpenAI%20(ChatGPT)-Purged-10a37f?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI Purged"></a>
  <a href="https://github.com/zimkk/openai-stripper"><img src="https://img.shields.io/badge/Google%20Gemini-Purged-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Gemini Purged"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-2ea44f?style=for-the-badge" alt="MIT License"></a>
  <a href="#"><img src="https://img.shields.io/badge/Privacy-100%25%20Offline-7928CA?style=for-the-badge&logo=auth0&logoColor=white" alt="100% Offline"></a>
</p>

<p align="center">
  <b>Vaporize C2PA manifests, digital tracking watermarks, AI generation prompts, and camera EXIF.</b><br>
  <i>100% free forever. No subscriptions. No cloud uploads. Zero quality loss.</i>
</p>

---

</div>

## 🎯 Why AI-STRIPPER?

Whenever you create an image with **OpenAI (ChatGPT / DALL-E 3)** or **Google Gemini (Imagen)**, invisible **C2PA Content Credentials** and metadata manifests are silently injected into the file.

Scammy web tools charge **$10/month** or force you to upload your private art to random servers. **AI-STRIPPER** solves this:

- 🛡️ **100% Local & Free:** Runs directly on your CPU. Your images never leave your computer.
- 🧼 **Zero-Leakage Rastering:** Discards all C2PA JUMBF boxes, AI prompt workflows, and EXIF geotags.
- 🎨 **True Color Fidelity:** Converts wide-gamut Display P3/Adobe RGB to standard sRGB so colors never wash out.
- 🔄 **Hardware Auto-Transposition:** Mobile portraits never rotate sideways after stripping.

---

## 🚀 Quick Start

### 1. 1-Click Launch (Easiest)
- **Windows:** Double-click [`run.bat`](run.bat)
- **macOS / Linux:** Run `./run.sh`

*Dependencies are verified and installed automatically.*

---

### 2. Install via Pip / Global CLI
```bash
pip install ai-stripper
ai-stripper
```

---

### 3. Developer Run
```bash
git clone https://github.com/zimkk/openai-stripper.git
cd openai-stripper
pip install -r requirements.txt
python stripper.py
```

---

## 🖥️ Interactive Terminal App (TUI)

Launch with `ai-stripper` or `python stripper.py` for a keyboard-first terminal experience:

```text
     ___    ____       _____ ______ ____  ____ ____  ____  ______ ____  
    /   |  /  _/      / ___//_  __// __ \/  _// __ \/ __ \/ ____// __ \ 
   / /| |  / /        \__ \  / /  / /_/ // / / /_/ / /_/ / __/  / /_/ / 
  / ___ |_/ /        ___/ / / /  / _, _// / / ____/ ____/ /___ / _, _/  
 /_/  |_/___/       /____/ /_/  /_/ |_/___//_/   /_/   /_____//_/ |_|   
    OPENAI & GEMINI METADATA VAPORIZER  v2.1.0

  Use [Up / Down / j / k] to navigate  *  [Enter] to select  *  [q] to quit

 >> [1] Quick Strip Default Folders  images to be stripped/ -> stripped/
    [2] Batch Strip Directory Wizard  Custom folder, recursion, quality
    [3] Strip Single Image  Target an individual image file
    [4] Inspect & Audit Metadata  Deep scan: C2PA, GPS coordinates, Prompts
    [5] Settings & Preferences  sRGB: ON • Q: 100 • Threads: 8
    [6] Exit Application  Quit
```

- **Controls:** <kbd>↑</kbd> <kbd>↓</kbd> or <kbd>k</kbd> <kbd>j</kbd> to move • <kbd>Enter</kbd> to select • <kbd>1</kbd>–<kbd>6</kbd> shortcuts • <kbd>Tab</kbd> autocomplete paths.

---

## ⚡ Power-User CLI Flags

Automate AI-STRIPPER in scripts, pre-commit hooks, or batch pipelines:

```bash
# Batch process a directory
ai-stripper -i ./chatgpt_images -o ./clean_images

# Audit image metadata & C2PA credentials without modifying
ai-stripper --inspect artwork.png

# Strip in-place recursively across subfolders
ai-stripper -i ./library -r --in-place

# Convert format on-the-fly with 95% quality
ai-stripper -i ./exports -o ./webp_clean --format webp -q 95
```

---

## 🔍 Metadata Inspection & Threat Meter

Run `--inspect` on any image to audit its hidden tracking data before publishing:

```text
┌─ [?] AI-STRIPPER Privacy Audit: chatgpt_artwork.png [HIGH RISK] ──────────┐
│  Threat Level Meter               [########--] 75% HIGH RISK              │
│  Dimensions                       1024 x 1024 px                          │
│  C2PA Content Credentials         [!] Detected (OpenAI Provenance Tracking)│
└───────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Supported Formats

| Format | Extension | Cleansed Metadata | Transparency |
| :---: | :---: | :--- | :---: |
| **PNG** | `.png` | C2PA JUMBF boxes, text chunks (`tEXt`/`zTXt`), ICC profiles | Preserved (RGBA) |
| **JPEG** | `.jpg`, `.jpeg` | EXIF, GPS coordinates, C2PA APP11 markers, IPTC, XMP | Clean White Blend |
| **WebP** | `.webp` | EXIF, XMP, ICC headers, animation comment chunks | Preserved |
| **TIFF / BMP** | `.tiff`, `.bmp` | Device headers, GeoTIFF tags, color masks | Preserved |

---

## 👨‍💻 Author & Contributions

Built with ⚡ by **[zimkk](https://github.com/zimkk)** and open-source privacy advocates.

Contributions, feature suggestions, and pull requests are warmly welcomed!

```bash
# Fork & clone
git checkout -b feature/CoolFeature
git commit -m "feat: Add new capability"
git push origin feature/CoolFeature
```

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for details.
