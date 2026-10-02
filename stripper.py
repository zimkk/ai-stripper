#!/usr/bin/env python3
"""
     ___    ____       _____ ______ ____  ____ ____  ____  ______ ____  
    /   |  /  _/      / ___//_  __// __ \\/  _// __ \\/ __ \\/ ____// __ \\ 
   / /| |  / /        \\__ \\  / /  / /_/ // / / /_/ / /_/ / __/  / /_/ / 
  / ___ |_/ /        ___/ / / /  / _, _// / / ____/ ____/ /___ / _, _/  
 /_/  |_/___/       /____/ /_/  /_/ |_/___//_/   /_/   /_____//_/ |_|   

AI-STRIPPER • Advanced Image Metadata & Synthetic Fingerprint Vaporizer
========================================================================
Interactive Terminal App (TUI) & High-Performance CLI Engine to purge:
- EXIF & Camera Serials
- Exact GPS Geotags (with auto Google Maps link)
- C2PA Content Credentials & JUMBF Provenance Manifests
- AI Generation Prompts & Workflows (Midjourney, SD, ComfyUI, DALL-E)
- ICC Profiles (with zero-loss sRGB color gamut conversion)
- Hardware Orientation Bug Auto-Transposition (exif_transpose)
"""

import os
import sys
import io
import time
import argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple, Dict, Any, Optional

# Ensure proper UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from PIL import Image, ImageOps, ExifTags
try:
    from PIL import ImageCms
    HAS_CMS = True
except ImportError:
    HAS_CMS = False

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
    TaskProgressColumn,
)
from rich.prompt import Prompt, Confirm, IntPrompt

try:
    from prompt_toolkit.application import Application
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.layout.containers import Window, HSplit
    from prompt_toolkit.layout.controls import FormattedTextControl
    from prompt_toolkit.layout.layout import Layout
    from prompt_toolkit.styles import Style
    from prompt_toolkit import prompt as pt_prompt
    from prompt_toolkit.completion import PathCompleter
    HAS_PROMPT_TOOLKIT = True
except ImportError:
    HAS_PROMPT_TOOLKIT = False

VERSION = "2.1.0"
APP_NAME = "AI-STRIPPER"
console = Console()

VALID_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp', '.tiff', '.tif', '.bmp', '.gif'}

DEFAULT_CONFIG = {
    "quality": 100,
    "convert_srgb": True,
    "auto_orient": True,
    "recursive": False,
    "workers": min(8, (os.cpu_count() or 4) * 2),
    "suffix": "",
    "overwrite": False,
    "animations": True,
}

# ---------------------------------------------------------------------------
# ASCII Art & Cyber Animations (Clean, 100% Cross-Platform)
# ---------------------------------------------------------------------------

ASCII_LOGO = [
    r"     ___    ____       _____ ______ ____  ____ ____  ____  ______ ____  ",
    r"    /   |  /  _/      / ___//_  __// __ \/  _// __ \/ __ \/ ____// __ \ ",
    r"   / /| |  / /        \__ \  / /  / /_/ // / / /_/ / /_/ / __/  / /_/ / ",
    r"  / ___ |_/ /        ___/ / / /  / _, _// / / ____/ ____/ /___ / _, _/  ",
    r" /_/  |_/___/       /____/ /_/  /_/ |_/___//_/   /_/   /_____//_/ |_|   "
]

LOCK_ASCII = [
    r"          .------------------.          ",
    r"         /   .------------.   \         ",
    r"        |   /              \   |        ",
    r"        |  |   [ LOCKED ]   |  |        ",
    r"        |  |   ZERO TRACE   |  |        ",
    r"       _|  |________________|  |_       ",
    r"     .' |_|                  |_| '.     ",
    r"     '._____ ____ ____ ____ _____.'     ",
    r"     |     .'____ ____ ____'.     |     ",
    r"     '.__.'.'                '.'.__.'   ",
    r"           '.________________.'         "
]

def render_colored_logo(glow_offset: int = 0) -> Text:
    """Renders the logo with a smooth neon rainbow cyber gradient."""
    palette = [
        "#00f0ff", "#00d4ff", "#00b4d8", "#7000ff", "#a855f7",
        "#d946ef", "#ec4899", "#f43f5e", "#fb7185", "#ff007f"
    ]
    t = Text()
    for i, line in enumerate(ASCII_LOGO):
        color = palette[(i + glow_offset) % len(palette)]
        t.append(line + "\n", style=f"bold {color}")
    return t


def play_boot_animation():
    """Plays an in-place high-tech cyberpunk telemetry startup animation without duplicate scrolling."""
    if not sys.stdin.isatty():
        return

    console.clear()

    # In-place transient glow animation across the logo (no line duplication)
    with Live(render_colored_logo(0), console=console, auto_refresh=False, transient=True) as live:
        for frame in range(1, 5):
            time.sleep(0.06)
            live.update(render_colored_logo(frame))
            live.refresh()

    # Print the settled logo once
    console.print(render_colored_logo(glow_offset=2))

    boot_steps = [
        ("[bold cyan]>> [SYS-INIT][/bold cyan] Booting AI-STRIPPER Cyber-Defense Core v" + VERSION, 0.04),
        ("[bold green][+][/bold green] EXIF Auto-Transpose Matrix ............. [bold green]ONLINE[/bold green]", 0.03),
        ("[bold magenta][+][/bold magenta] C2PA JUMBF Manifest Disassembler ....... [bold magenta]ACTIVE[/bold magenta]", 0.03),
        ("[bold yellow][+][/bold yellow] AI Prompt & Latent Tag Vaporizer ....... [bold yellow]ARMED[/bold yellow]", 0.03),
        ("[bold blue][+][/bold blue] LCMS Wide-Gamut sRGB Color Shield ...... [bold blue]CALIBRATED[/bold blue]", 0.03),
        ("[bold green][+][/bold green] Incognito Sanitization Pipeline ........ [bold green]READY[/bold green]\n", 0.04),
    ]

    for step_text, delay in boot_steps:
        console.print(step_text)
        time.sleep(delay)

    time.sleep(0.2)


def play_exit_animation():
    """Plays a stylish neon cyber-shield lock animation on exit."""
    console.clear()
    lock_text = Text()
    for i, line in enumerate(LOCK_ASCII):
        lock_text.append(line + "\n", style=f"bold {'#00ffaf' if i > 5 else '#00f0ff'}")

    console.print(lock_text)
    console.print("[bold bright_white]  +=========================================================+[/bold bright_white]")
    console.print("[bold bright_white]  | [/bold bright_white][bold green][+] SYSTEM SECURED • ALL METADATA WIPED • ZERO TRACES[/bold green][bold bright_white]   |[/bold bright_white]")
    console.print("[bold bright_white]  +=========================================================+[/bold bright_white]\n")


# ---------------------------------------------------------------------------
# Core Metadata Stripping Engine
# ---------------------------------------------------------------------------

def convert_to_srgb(img: Image.Image) -> Image.Image:
    """
    If the image has an embedded ICC profile (e.g. Display P3, Adobe RGB),
    convert pixel values to standard sRGB so colors do not wash out when the
    profile header is removed.
    """
    if not HAS_CMS or "icc_profile" not in img.info:
        return img

    try:
        icc_data = img.info.get("icc_profile")
        if not icc_data:
            return img

        input_profile = ImageCms.ImageCmsProfile(io.BytesIO(icc_data))
        srgb_profile = ImageCms.createProfile("sRGB")

        transformed = ImageCms.profileToProfile(
            img,
            inputProfile=input_profile,
            outputProfile=srgb_profile,
            outputMode=img.mode
        )
        return transformed
    except Exception:
        return img


def strip_image_metadata(
    input_path: Path,
    output_path: Path,
    quality: int = 100,
    target_format: Optional[str] = None,
    convert_srgb: bool = True,
    auto_orient: bool = True
) -> Dict[str, Any]:
    """
    Reads an image, removes all metadata (EXIF, C2PA, XMP, ICC, AI prompts, text chunks),
    applies physical orientation correction, and saves a clean copy to output_path.
    """
    orig_size = input_path.stat().st_size
    dest_ext = (f".{target_format.lower()}" if target_format else output_path.suffix).lower()
    if dest_ext == '.jpeg':
        dest_ext = '.jpg'

    with Image.open(input_path) as raw_img:
        # 1. Correct physical orientation before stripping EXIF orientation tag
        if auto_orient:
            try:
                img = ImageOps.exif_transpose(raw_img)
            except Exception:
                img = raw_img.copy()
        else:
            img = raw_img.copy()

        # 2. Color space handling: convert to sRGB if ICC profile is present
        if convert_srgb and HAS_CMS:
            img = convert_to_srgb(img)

        # 3. Clean pixel buffer reconstruction to guarantee zero metadata leakage
        save_kwargs: Dict[str, Any] = {}

        if dest_ext in ('.jpg', '.jpeg'):
            if img.mode in ('RGBA', 'LA', 'P'):
                bg = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                bg.paste(img, mask=img.split()[3] if img.mode in ('RGBA', 'LA') else None)
                clean_img = bg
            elif img.mode != 'RGB':
                clean_img = img.convert('RGB')
            else:
                clean_img = Image.new('RGB', img.size)
                clean_img.paste(img)

            save_kwargs = {'quality': quality, 'optimize': True, 'subsampling': 0}

        elif dest_ext == '.png':
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                clean_img = img.convert('RGBA')
            elif img.mode == 'L':
                clean_img = Image.new('L', img.size)
                clean_img.paste(img)
            else:
                clean_img = img.convert('RGB')

            save_kwargs = {'optimize': True}

        elif dest_ext == '.webp':
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                clean_img = img.convert('RGBA')
                lossless = (quality >= 100)
            elif img.mode == 'L':
                clean_img = Image.new('L', img.size)
                clean_img.paste(img)
                lossless = (quality >= 100)
            else:
                clean_img = img.convert('RGB')
                lossless = (quality >= 100)

            save_kwargs = {'quality': quality, 'lossless': lossless}

        elif dest_ext in ('.tiff', '.tif'):
            clean_img = img.convert('RGB')
            save_kwargs = {'compression': 'tiff_deflate'}

        elif dest_ext == '.gif':
            clean_img = img.convert('P')
            save_kwargs = {'optimize': True}

        else:
            clean_img = img.convert('RGB')
            save_kwargs = {}

        output_path.parent.mkdir(parents=True, exist_ok=True)
        clean_img.save(output_path, **save_kwargs)

    clean_size = output_path.stat().st_size
    saved_bytes = orig_size - clean_size

    return {
        "status": "success",
        "input_path": input_path,
        "output_path": output_path,
        "orig_size": orig_size,
        "clean_size": clean_size,
        "saved_bytes": saved_bytes,
        "error": None
    }


# ---------------------------------------------------------------------------
# Metadata Inspection & Audit Engine
# ---------------------------------------------------------------------------

def parse_gps_coordinates(gps_info: Dict[Any, Any]) -> Optional[Tuple[float, float, Optional[float]]]:
    """Extracts decimal latitude, longitude, and altitude from EXIF GPS tags."""
    try:
        def to_degrees(val):
            if isinstance(val, tuple) or isinstance(val, list):
                deg = float(val[0])
                minute = float(val[1])
                sec = float(val[2])
                return deg + (minute / 60.0) + (sec / 3600.0)
            return float(val)

        lat_raw = gps_info.get(2) or gps_info.get('GPSLatitude')
        lat_ref = gps_info.get(1) or gps_info.get('GPSLatitudeRef', 'N')
        lon_raw = gps_info.get(4) or gps_info.get('GPSLongitude')
        lon_ref = gps_info.get(3) or gps_info.get('GPSLongitudeRef', 'E')
        alt_raw = gps_info.get(6) or gps_info.get('GPSAltitude')

        if lat_raw and lon_raw:
            lat = to_degrees(lat_raw)
            if lat_ref == 'S':
                lat = -lat
            lon = to_degrees(lon_raw)
            if lon_ref == 'W':
                lon = -lon
            alt = float(alt_raw) if alt_raw is not None else None
            return (lat, lon, alt)
    except Exception:
        pass
    return None


def inspect_image_metadata(img_path: Path) -> Dict[str, Any]:
    """
    Deeply inspects an image for:
    - EXIF camera, lens, timestamps
    - GPS geolocation (with coordinates and map link)
    - AI generation prompts (Stable Diffusion, Midjourney, ComfyUI, DALL-E)
    - C2PA / Content Credentials signatures
    - ICC color profile
    - XMP / IPTC / text chunks
    - Privacy Risk Assessment
    """
    results: Dict[str, Any] = {
        "file_name": img_path.name,
        "file_size": img_path.stat().st_size,
        "format": "Unknown",
        "dimensions": "Unknown",
        "color_mode": "Unknown",
        "exif": {},
        "gps": None,
        "ai_metadata": {},
        "c2pa_detected": False,
        "icc_profile": None,
        "raw_text_chunks": {},
        "risk_level": "CLEAN",
        "risk_reasons": []
    }

    try:
        with open(img_path, "rb") as f:
            header_sample = f.read(256 * 1024)
            c2pa_keywords = [b'c2pa', b'C2PA', b'jumb', b'contentcredentials', b'caPA']
            if any(k in header_sample for k in c2pa_keywords):
                results["c2pa_detected"] = True
                results["risk_reasons"].append("C2PA / Content Credentials manifest detected")
    except Exception:
        pass

    try:
        with Image.open(img_path) as img:
            results["format"] = img.format or img_path.suffix.upper().strip('.')
            results["dimensions"] = f"{img.width} x {img.height} px"
            results["color_mode"] = img.mode

            if "icc_profile" in img.info:
                profile_name = "Embedded ICC Profile"
                if HAS_CMS:
                    try:
                        p = ImageCms.ImageCmsProfile(io.BytesIO(img.info["icc_profile"]))
                        profile_name = ImageCms.getProfileName(p).strip()
                    except Exception:
                        pass
                results["icc_profile"] = profile_name

            for key, val in img.info.items():
                if key in ('exif', 'icc_profile', 'photoshop'):
                    continue
                val_str = str(val)
                low = val_str.lower()
                if any(ai_term in low for ai_term in ['steps:', 'sampler:', 'cfg scale:', 'prompt', 'negative prompt', 'workflow']):
                    results["ai_metadata"][key] = val_str[:500] + ("..." if len(val_str) > 500 else "")
                    results["risk_reasons"].append(f"AI Generation prompt/workflow detected in '{key}'")
                elif len(val_str) < 300:
                    results["raw_text_chunks"][key] = val_str

            try:
                exif_data = img.getexif()
                if exif_data:
                    for tag_id, tag_val in exif_data.items():
                        tag_name = ExifTags.TAGS.get(tag_id, str(tag_id))
                        if isinstance(tag_val, bytes) and len(tag_val) > 100:
                            continue
                        results["exif"][tag_name] = str(tag_val)

                    camera_fields = ['Make', 'Model', 'LensModel', 'Software', 'DateTime', 'DateTimeOriginal']
                    found_cam = [f"{k}: {results['exif'][k]}" for k in camera_fields if k in results['exif']]
                    if found_cam:
                        results["risk_reasons"].append(f"Camera details found: {', '.join(found_cam[:3])}")

                    gps_ifd = exif_data.get_ifd(0x8825)
                    if gps_ifd:
                        coords = parse_gps_coordinates(gps_ifd)
                        if coords:
                            lat, lon, alt = coords
                            results["gps"] = {
                                "latitude": lat,
                                "longitude": lon,
                                "altitude": alt,
                                "maps_url": f"https://www.google.com/maps/search/?api=1&query={lat:.6f},{lon:.6f}"
                            }
                            results["risk_reasons"].append(f"Precise GPS location detected ({lat:.4f}, {lon:.4f})")
            except Exception:
                pass

    except Exception as e:
        results["risk_reasons"].append(f"Inspection error: {e}")

    reasons = results["risk_reasons"]
    if results["gps"] is not None:
        results["risk_level"] = "CRITICAL"
    elif any("Camera" in r for r in reasons) or any("AI Generation" in r for r in reasons) or results["c2pa_detected"]:
        results["risk_level"] = "HIGH"
    elif reasons:
        results["risk_level"] = "MEDIUM"
    else:
        results["risk_level"] = "CLEAN"

    return results


def display_inspection_report(info: Dict[str, Any]):
    """Renders a comprehensive inspection report using Rich panels and tables."""
    console.print()

    level = info["risk_level"]
    badge_colors = {
        "CLEAN": "bold green on black",
        "LOW": "bold cyan on black",
        "MEDIUM": "bold yellow on black",
        "HIGH": "bold red on black",
        "CRITICAL": "bold white on red"
    }
    badge_color = badge_colors.get(level, "bold white")
    title_text = Text()
    title_text.append(" [?] AI-STRIPPER Privacy & Fingerprint Audit: ", style="bold white")
    title_text.append(f"{info['file_name']}", style="bold cyan")
    title_text.append(f"  [{level}] ", style=badge_color)

    meter_bars = {
        "CLEAN":    "[green][##########][/green] [bold green]0% SAFE[/bold green]",
        "LOW":      "[cyan][###-------][/cyan] [bold cyan]25% LOW[/bold cyan]",
        "MEDIUM":   "[yellow][######----][/yellow] [bold yellow]50% MEDIUM[/bold yellow]",
        "HIGH":     "[red][########--][/red] [bold red]75% HIGH RISK[/bold red]",
        "CRITICAL": "[bold white on red][##########][/bold white on red] [bold red]100% CRITICAL LEAK[/bold red]"
    }

    table = Table(box=None, expand=True, show_header=False)
    table.add_column("Property", style="bold dim", width=24)
    table.add_column("Value", style="cyan")

    table.add_row("Threat Level Meter", meter_bars.get(level, ""))
    table.add_row("File Size", f"{info['file_size'] / 1024:.1f} KB ({info['file_size']:,} bytes)")
    table.add_row("Format & Mode", f"{info['format']} ({info['color_mode']})")
    table.add_row("Dimensions", info["dimensions"])
    table.add_row("Color Profile", info["icc_profile"] or "[dim]None / Untagged[/dim]")
    table.add_row("C2PA Content Credentials", "[bold red][!] Detected (Provenance Tracking)[/bold red]" if info["c2pa_detected"] else "[green]Not detected[/green]")

    console.print(Panel(table, title=title_text, border_style="cyan", expand=False))

    if info["gps"]:
        gps = info["gps"]
        gps_panel = Table(box=None, expand=True, show_header=False)
        gps_panel.add_column("Key", style="bold red", width=24)
        gps_panel.add_column("Value", style="yellow")
        gps_panel.add_row("Latitude", f"{gps['latitude']:.6f} deg")
        gps_panel.add_row("Longitude", f"{gps['longitude']:.6f} deg")
        if gps["altitude"]:
            gps_panel.add_row("Altitude", f"{gps['altitude']} m")
        gps_panel.add_row("Google Maps Link", f"[underline blue]{gps['maps_url']}[/underline blue]")

        console.print(Panel(
            gps_panel,
            title="[bold red][!] SENSITIVE GPS GEOLOCATION FOUND[/bold red]",
            border_style="red"
        ))

    if info["ai_metadata"]:
        ai_table = Table(expand=True, box=None, show_header=True)
        ai_table.add_column("Tag / Parameter", style="bold magenta", width=20)
        ai_table.add_column("Extracted Data", style="bright_white")
        for k, v in info["ai_metadata"].items():
            ai_table.add_row(k, v)
        console.print(Panel(
            ai_table,
            title="[bold magenta][AI] Generation Metadata (Prompts & Settings)[/bold magenta]",
            border_style="magenta"
        ))

    if info["exif"]:
        exif_table = Table(expand=True, box=None, show_header=True)
        exif_table.add_column("EXIF Tag", style="bold cyan", width=24)
        exif_table.add_column("Value", style="white")
        priority_keys = ['Make', 'Model', 'LensModel', 'Software', 'DateTime', 'DateTimeOriginal', 'Artist', 'Copyright']
        shown = 0
        for k in priority_keys:
            if k in info["exif"]:
                exif_table.add_row(k, info["exif"][k])
                shown += 1
        for k, v in info["exif"].items():
            if k not in priority_keys and shown < 12:
                exif_table.add_row(k, str(v)[:80])
                shown += 1

        console.print(Panel(
            exif_table,
            title=f"[bold cyan][CAM] EXIF Camera & Hardware Metadata ({len(info['exif'])} tags total)[/bold cyan]",
            border_style="cyan"
        ))

    if level in ("CRITICAL", "HIGH"):
        console.print(f"[bold yellow][!] Recommendation:[/bold yellow] This image contains sensitive private metadata. [bold green]Strip with AI-STRIPPER before publishing.[/bold green]\n")
    else:
        console.print("[bold green][+] Image is relatively clean or free of critical privacy leaks.[/bold green]\n")


# ---------------------------------------------------------------------------
# Batch Processing & Multi-threading
# ---------------------------------------------------------------------------

def collect_images(target_dir: Path, recursive: bool = False) -> List[Path]:
    """Gathers all supported image paths from directory."""
    images = []
    pattern = "**/*" if recursive else "*"
    for p in target_dir.glob(pattern):
        if p.is_file() and p.suffix.lower() in VALID_EXTENSIONS:
            images.append(p)
    images.sort(key=lambda x: str(x).lower())
    return images


def format_bytes(num_bytes: float) -> str:
    """Formats bytes to human-readable string (KB, MB, GB)."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if abs(num_bytes) < 1024.0:
            return f"{num_bytes:3.1f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.1f} TB"


def process_image_task(args: Tuple[Path, Path, int, Optional[str], bool, bool]) -> Dict[str, Any]:
    """Helper wrapper for multi-threaded executor."""
    input_path, output_path, quality, target_format, convert_srgb, auto_orient = args
    try:
        return strip_image_metadata(
            input_path=input_path,
            output_path=output_path,
            quality=quality,
            target_format=target_format,
            convert_srgb=convert_srgb,
            auto_orient=auto_orient
        )
    except Exception as e:
        return {
            "status": "error",
            "input_path": input_path,
            "output_path": output_path,
            "orig_size": input_path.stat().st_size if input_path.exists() else 0,
            "clean_size": 0,
            "saved_bytes": 0,
            "error": str(e)
        }


def run_batch_processing(
    input_files: List[Path],
    output_dir: Optional[Path],
    base_input_dir: Optional[Path] = None,
    quality: int = 100,
    suffix: str = "",
    target_format: Optional[str] = None,
    in_place: bool = False,
    workers: int = 8,
    convert_srgb: bool = True,
    auto_orient: bool = True
) -> List[Dict[str, Any]]:
    """
    Executes high-speed batch metadata stripping with an animated ASCII shredder
    and live Rich progress bar, displaying a formatted summary table upon completion.
    """
    if not input_files:
        console.print("[yellow]No images found to process.[/yellow]")
        return []

    tasks = []
    for idx, in_file in enumerate(input_files, start=1):
        if in_place:
            out_file = in_file
        else:
            if base_input_dir and in_file.is_relative_to(base_input_dir):
                rel_path = in_file.relative_to(base_input_dir)
                stem = rel_path.stem
                if suffix:
                    stem = f"{stem}{suffix}"
                ext = f".{target_format.lower()}" if target_format else rel_path.suffix
                out_file = output_dir / rel_path.parent / f"{stem}{ext}"
            else:
                stem = in_file.stem
                if suffix:
                    stem = f"{stem}{suffix}"
                ext = f".{target_format.lower()}" if target_format else in_file.suffix
                out_file = output_dir / f"{stem}{ext}"

        tasks.append((in_file, out_file, quality, target_format, convert_srgb, auto_orient))

    results = []
    total_orig_size = 0
    total_clean_size = 0
    start_time = time.time()

    console.print()
    shredder_panel = Panel(
        Text(r">> PURGING METADATA • VAPORIZING C2PA & AI FINGERPRINTS <<", style="bold magenta justify=center"),
        border_style="magenta",
        expand=False
    )
    console.print(shredder_panel)

    with Progress(
        SpinnerColumn(spinner_name="dots12", style="bold cyan"),
        TextColumn("[bold cyan]{task.description}[/bold cyan]"),
        BarColumn(bar_width=None, style="magenta", complete_style="green"),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        console=console
    ) as progress:
        task_id = progress.add_task(f"Sanitizing {len(tasks)} images...", total=len(tasks))

        with ThreadPoolExecutor(max_workers=max(1, workers)) as executor:
            future_to_task = {executor.submit(process_image_task, t): t for t in tasks}

            for future in as_completed(future_to_task):
                res = future.result()
                results.append(res)
                if res["status"] == "success":
                    total_orig_size += res["orig_size"]
                    total_clean_size += res["clean_size"]
                progress.advance(task_id)

    elapsed = time.time() - start_time
    success_count = sum(1 for r in results if r["status"] == "success")
    fail_count = sum(1 for r in results if r["status"] == "error")
    total_saved = total_orig_size - total_clean_size
    reduction_pct = (total_saved / total_orig_size * 100) if total_orig_size > 0 else 0

    console.print()
    summary_table = Table(title="[+] Vaporization Completed", box=None, expand=True)
    summary_table.add_column("Metric", style="bold cyan", width=25)
    summary_table.add_column("Result", style="bold white")

    summary_table.add_row("Total Images", f"{len(input_files)}")
    summary_table.add_row("Successfully Cleaned", f"[green]{success_count}[/green]")
    if fail_count > 0:
        summary_table.add_row("Failed", f"[red]{fail_count}[/red]")
    summary_table.add_row("Original Total Size", format_bytes(total_orig_size))
    summary_table.add_row("Sanitized Total Size", format_bytes(total_clean_size))
    if total_saved > 0:
        summary_table.add_row("Total Space Saved", f"[bold green]{format_bytes(total_saved)} ({reduction_pct:.1f}% reduction)[/bold green]")
    else:
        summary_table.add_row("Size Difference", f"{format_bytes(abs(total_saved))} change")
    summary_table.add_row("Time Elapsed", f"{elapsed:.2f} seconds ({len(tasks) / max(elapsed, 0.001):.1f} imgs/sec)")
    if output_dir and not in_place:
        summary_table.add_row("Saved Destination", f"[underline blue]{output_dir.resolve()}[/underline blue]")

    console.print(Panel(summary_table, border_style="green", expand=False))

    if fail_count > 0:
        fail_table = Table(title="[!] Failures Encountered", box=None)
        fail_table.add_column("File", style="yellow")
        fail_table.add_column("Error", style="red")
        for r in results:
            if r["status"] == "error":
                fail_table.add_row(r["input_path"].name, str(r["error"]))
        console.print(fail_table)

    return results


# ---------------------------------------------------------------------------
# Interactive Terminal App (TUI) with Arrow Key Navigation
# ---------------------------------------------------------------------------

def render_arrow_menu(options: List[Tuple[str, str, str]], active_idx: int, header_subtitle: str = "") -> List[Tuple[str, str]]:
    """Renders formatted text for the arrow-key terminal menu."""
    tokens = []
    tokens.append(('class:header', "  Use [Up / Down / j / k] to navigate  *  [Enter] to select  *  [q] to quit\n\n"))

    for i, (key, title, subtitle) in enumerate(options):
        is_selected = (i == active_idx)
        if is_selected:
            tokens.append(('class:cursor', " >> "))
            tokens.append(('class:selected_num', f"[{key}] "))
            tokens.append(('class:selected_title', f"{title} "))
            if subtitle:
                tokens.append(('class:selected_sub', f" {subtitle}"))
            tokens.append(('', "\n"))
        else:
            tokens.append(('class:dim', "    "))
            tokens.append(('class:num', f"[{key}] "))
            tokens.append(('class:title', f"{title} "))
            if subtitle:
                tokens.append(('class:sub', f" {subtitle}"))
            tokens.append(('', "\n"))

    tokens.append(('class:footer', f"\n  {header_subtitle}\n"))
    return tokens


def run_interactive_menu(options: List[Tuple[str, str, str]], default_idx: int = 0, status_hint: str = "") -> str:
    """
    Launches an arrow-key navigable TUI menu using prompt_toolkit.
    Falls back gracefully to rich Prompt if stdin is non-interactive.
    """
    if not HAS_PROMPT_TOOLKIT or not sys.stdin.isatty():
        for key, title, subtitle in options:
            sub = f" [dim]({subtitle})[/dim]" if subtitle else ""
            console.print(f"  [bold cyan]{key}[/bold cyan]. {title}{sub}")
        valid_keys = [opt[0] for opt in options]
        return Prompt.ask("\nSelect option", choices=valid_keys, default=valid_keys[default_idx])

    selected = [default_idx]
    kb = KeyBindings()

    @kb.add('up')
    @kb.add('k')
    def move_up(event):
        selected[0] = (selected[0] - 1) % len(options)

    @kb.add('down')
    @kb.add('j')
    def move_down(event):
        selected[0] = (selected[0] + 1) % len(options)

    for i, opt in enumerate(options):
        k = opt[0]
        def make_handler(idx=i, key_val=k):
            def handler(event):
                event.app.exit(result=key_val)
            return handler
        kb.add(k)(make_handler())

    @kb.add('enter')
    def select_item(event):
        event.app.exit(result=options[selected[0]][0])

    @kb.add('q')
    @kb.add('c-c')
    def quit_app(event):
        event.app.exit(result="QUIT")

    style = Style.from_dict({
        'header': '#5fd7ff italic',
        'cursor': 'bold #ff007f',
        'selected_num': 'bold #00ffaf',
        'selected_title': 'bold #ffffff bg:#7000ff',
        'selected_sub': '#e0e0e0 bg:#7000ff',
        'dim': '#555555',
        'num': '#00d7ff',
        'title': '#e4e4e4',
        'sub': '#767676',
        'footer': '#808080 italic',
    })

    def get_formatted_text():
        return render_arrow_menu(options, selected[0], status_hint)

    control = FormattedTextControl(get_formatted_text)
    layout = Layout(HSplit([Window(content=control, dont_extend_height=True)]))
    app = Application(layout=layout, key_bindings=kb, style=style, full_screen=False)

    res = app.run()
    return res if res else "QUIT"


def get_input_path(prompt_text: str, default: Optional[str] = None, must_exist: bool = True, is_file: bool = False) -> Path:
    """
    Prompts user for path with tab-completion support via prompt_toolkit,
    falling back to Rich Prompt if unavailable.
    """
    while True:
        try:
            if HAS_PROMPT_TOOLKIT and sys.stdin.isatty():
                completer = PathCompleter(only_directories=not is_file, expanduser=True)
                def_str = f" [{default}]" if default else ""
                raw = pt_prompt(f"{prompt_text}{def_str}: ", completer=completer).strip().strip('"\'')
                if not raw and default:
                    raw = default
            else:
                raw = Prompt.ask(prompt_text, default=default or "").strip().strip('"\'')
        except (KeyboardInterrupt, EOFError):
            console.print("\n[yellow]Operation cancelled.[/yellow]")
            sys.exit(0)

        if not raw:
            console.print("[red]Path cannot be empty. Please try again.[/red]")
            continue

        p = Path(raw).expanduser().resolve()
        if must_exist:
            if is_file and not p.is_file():
                console.print(f"[red]Error: File does not exist: {p}[/red]")
                continue
            elif not is_file and not p.is_dir():
                console.print(f"[red]Error: Directory does not exist: {p}[/red]")
                continue
        return p


def print_banner(uncleaned_count: Optional[int] = None):
    """Renders the stylized application banner."""
    console.clear()
    subtitle = "[bold cyan]AI-STRIPPER Core[/bold cyan] • [dim]C2PA & Synthetic Metadata Eradicator[/dim]"
    if uncleaned_count is not None and uncleaned_count > 0:
        subtitle += f" • [bold yellow][!] {uncleaned_count} unstripped images detected[/bold yellow]"

    console.print(Panel(
        render_colored_logo(glow_offset=2),
        subtitle=subtitle,
        border_style="magenta",
        expand=False
    ))


def interactive_terminal_app():
    """Main interactive TUI loop with arrow navigation, file wizards, and settings."""
    script_dir = Path(__file__).resolve().parent
    default_input = script_dir / "images to be stripped"
    default_output = script_dir / "stripped"

    config = DEFAULT_CONFIG.copy()

    # Play initial cyberpunk boot animation once on launch
    if config.get("animations", True):
        play_boot_animation()

    while True:
        unstripped = 0
        if default_input.is_dir():
            unstripped = len(collect_images(default_input))

        print_banner(uncleaned_count=unstripped)

        menu_options = [
            ("1", "Quick Strip Default Folders", f"images to be stripped/ -> stripped/ [{unstripped} items ready]"),
            ("2", "Batch Strip Directory Wizard", "Pick custom folder, recursion, quality, output"),
            ("3", "Strip Single Image", "Target a specific image file with custom destination"),
            ("4", "Inspect & Audit Metadata", "Deep privacy scan: GPS map link, AI prompts, C2PA"),
            ("5", "Settings & Preferences", f"sRGB: {'ON' if config['convert_srgb'] else 'OFF'} • Q: {config['quality']} • Threads: {config['workers']}"),
            ("6", "Engine Info & Benchmarks", "View Pillow features, CPU cores, supported formats"),
            ("7", "Help & Privacy Threat Guide", "Detailed manual on what gets purged and why"),
            ("8", "Exit Application", "Quit the terminal application")
        ]

        choice = run_interactive_menu(menu_options, default_idx=0, status_hint="Press 1-8 or navigate with Arrow Keys and press Enter")

        if choice in ("8", "QUIT"):
            play_exit_animation()
            break

        console.clear()

        if choice == "1":
            console.rule("[bold cyan]Quick Strip Default Folders[/bold cyan]")
            if not default_input.is_dir():
                console.print(f"[yellow]Default folder '{default_input.name}' not found. Creating it...[/yellow]")
                default_input.mkdir(parents=True, exist_ok=True)

            images = collect_images(default_input, recursive=False)
            if not images:
                console.print(f"\n[yellow]No images found in [bold]{default_input}[/bold]. Drop images there to test![/yellow]")
            else:
                console.print(f"\n[cyan]Found [bold]{len(images)}[/bold] images in [bold]{default_input.name}[/bold][/cyan]")
                if Confirm.ask("Start stripping metadata now?", default=True):
                    default_output.mkdir(parents=True, exist_ok=True)
                    run_batch_processing(
                        input_files=images,
                        output_dir=default_output,
                        base_input_dir=default_input,
                        quality=config["quality"],
                        workers=config["workers"],
                        convert_srgb=config["convert_srgb"],
                        auto_orient=config["auto_orient"]
                    )

        elif choice == "2":
            console.rule("[bold cyan]Batch Strip Directory Wizard[/bold cyan]")
            in_dir = get_input_path("Enter directory containing images", default=str(default_input), must_exist=True, is_file=False)
            recursive = Confirm.ask("Scan subdirectories recursively?", default=config["recursive"])

            images = collect_images(in_dir, recursive=recursive)
            if not images:
                console.print(f"\n[yellow]No supported images found in '{in_dir}'.[/yellow]")
            else:
                console.print(f"\n[green]Found [bold]{len(images)}[/bold] supported image(s).[/green]")

                in_place = Confirm.ask("Overwrite original files in-place? (Dangerous: will modify original images)", default=False)
                if in_place:
                    out_dir = None
                    if not Confirm.ask("Are you sure you want to permanently overwrite originals?", default=False):
                        continue
                else:
                    default_out = in_dir.parent / f"{in_dir.name}_stripped"
                    out_dir = get_input_path("Enter output directory", default=str(default_out), must_exist=False, is_file=False)

                suffix = Prompt.ask("Append suffix to filenames? (Leave blank to keep same names)", default="")
                quality = IntPrompt.ask("Output quality (1-100) for lossy formats", default=config["quality"])

                run_batch_processing(
                    input_files=images,
                    output_dir=out_dir,
                    base_input_dir=in_dir,
                    quality=quality,
                    suffix=suffix,
                    in_place=in_place,
                    workers=config["workers"],
                    convert_srgb=config["convert_srgb"],
                    auto_orient=config["auto_orient"]
                )

        elif choice == "3":
            console.rule("[bold cyan]Strip Single Image[/bold cyan]")
            img_file = get_input_path("Enter image path to strip", must_exist=True, is_file=True)
            default_out = img_file.parent / f"{img_file.stem}_stripped{img_file.suffix}"
            out_file = get_input_path("Enter output destination file", default=str(default_out), must_exist=False, is_file=True)

            quality = IntPrompt.ask("Quality (1-100)", default=config["quality"])
            console.print(f"\n[cyan]Processing [bold]{img_file.name}[/bold]...[/cyan]")
            res = strip_image_metadata(img_file, out_file, quality=quality, convert_srgb=config["convert_srgb"], auto_orient=config["auto_orient"])
            if res["status"] == "success":
                console.print(f"\n[bold green][+] Cleaned successfully![/bold green] Saved {res['saved_bytes'] / 1024:.1f} KB -> [underline]{out_file}[/underline]")
            else:
                console.print(f"\n[bold red][!] Failed: {res['error']}[/bold red]")

        elif choice == "4":
            console.rule("[bold cyan]Inspect Image Metadata & Privacy Audit[/bold cyan]")
            sample_candidates = collect_images(default_input)
            default_candidate = str(sample_candidates[0]) if sample_candidates else None
            img_file = get_input_path("Enter image path to inspect", default=default_candidate, must_exist=True, is_file=True)

            info = inspect_image_metadata(img_file)
            display_inspection_report(info)

            if Confirm.ask("Would you like to strip this image now?", default=False):
                default_out = img_file.parent / f"{img_file.stem}_stripped{img_file.suffix}"
                out_file = get_input_path("Enter output destination file", default=str(default_out), must_exist=False, is_file=True)
                res = strip_image_metadata(img_file, out_file, quality=config["quality"], convert_srgb=config["convert_srgb"], auto_orient=config["auto_orient"])
                if res["status"] == "success":
                    console.print(f"\n[bold green][+] Cleaned successfully![/bold green] -> [underline]{out_file}[/underline]")

        elif choice == "5":
            console.rule("[bold cyan]Configure Preferences[/bold cyan]")
            config["convert_srgb"] = Confirm.ask("Convert ICC profiles to standard sRGB (prevents color desaturation)", default=config["convert_srgb"])
            config["auto_orient"] = Confirm.ask("Auto-orient images using EXIF transposition (prevents sideways images)", default=config["auto_orient"])
            config["quality"] = IntPrompt.ask("Default lossy quality (1-100)", default=config["quality"])
            config["workers"] = IntPrompt.ask("Batch worker threads (concurrency)", default=config["workers"])
            config["animations"] = Confirm.ask("Enable cyber animations", default=config.get("animations", True))
            console.print("\n[bold green][+] Settings updated for this session![/bold green]")

        elif choice == "6":
            console.rule("[bold cyan]Engine Status & System Info[/bold cyan]")
            sys_table = Table(box=None, expand=True)
            sys_table.add_column("Component", style="bold cyan", width=25)
            sys_table.add_column("Details", style="white")

            sys_table.add_row("AI-STRIPPER Engine", f"v{VERSION}")
            sys_table.add_row("Python Version", sys.version.split()[0])
            sys_table.add_row("Pillow (PIL) Version", Image.__version__)
            sys_table.add_row("Color Management (CMS)", "[green]Available (LittleCMS)[/green]" if HAS_CMS else "[yellow]Unavailable[/yellow]")
            sys_table.add_row("Interactive TUI Backend", "[green]prompt_toolkit (VT100/Win32)[/green]" if HAS_PROMPT_TOOLKIT else "[yellow]Basic Prompt[/yellow]")
            sys_table.add_row("Logical CPU Cores", str(os.cpu_count() or "Unknown"))
            sys_table.add_row("Supported Extensions", ", ".join(sorted(VALID_EXTENSIONS)))

            console.print(Panel(sys_table, border_style="cyan", title="System Capabilities"))

        elif choice == "7":
            console.rule("[bold cyan]Privacy Threat Guide & Architecture[/bold cyan]")
            guide_text = """
[bold bright_white]Why Traditional Stripping Fails (and why AI-STRIPPER is different):[/bold bright_white]

1. [bold cyan]C2PA / Content Credentials Tracking:[/bold cyan]
   Modern cameras, editing software, and AI generators embed digital provenance
   manifests (JUMBF boxes). Standard EXIF tools often fail to remove these.
   AI-STRIPPER decodes the pure pixel array and writes a pristine image container.

2. [bold magenta]AI Generation Workflow Leaks:[/bold magenta]
   Stable Diffusion, ComfyUI, and Midjourney embed complete prompts, negative prompts,
   model hashes, and seeds in PNG text chunks. AI-STRIPPER eliminates all ancillary chunks.

3. [bold yellow]Color Fidelity Loss (The ICC Trap):[/bold yellow]
   Stripping an ICC profile without color conversion leaves images washed out on sRGB
   displays. AI-STRIPPER converts wide-gamut profiles (e.g. Display P3, Adobe RGB) to sRGB
   before removing the profile, ensuring identical color appearance.

4. [bold green]Sideways Photos (Orientation Loss):[/bold green]
   Phones store photos in hardware sensor orientation and add an EXIF rotation tag.
   Deleting EXIF naively leaves photos rotated 90 or 180 degrees. AI-STRIPPER applies
   physical transpose before stripping EXIF.
            """
            console.print(Panel(guide_text, border_style="magenta"))

        console.print()
        Prompt.ask("[dim]Press Enter to return to main menu[/dim]", default="")


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description=f"{APP_NAME} • Image Metadata & Synthetic Fingerprint Vaporizer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ai-stripper                                      # Launch Interactive Terminal App (TUI)
  ai-stripper -i ./input -o ./output               # Batch process directory
  ai-stripper -i photo.jpg -o clean.jpg            # Process single image
  ai-stripper --inspect photo.jpg                  # Deep audit image metadata
  ai-stripper -i ./input -r --in-place             # Recursively strip in-place
        """
    )
    parser.add_argument("-i", "--input", help="Path to input image or directory")
    parser.add_argument("-o", "--output", help="Path to output image or directory")
    parser.add_argument("-q", "--quality", type=int, default=100, help="Output quality (1-100) for lossy formats (default: 100)")
    parser.add_argument("-r", "--recursive", action="store_true", help="Recursively process subdirectories")
    parser.add_argument("-s", "--suffix", default="", help="Append suffix to filenames (e.g. '_stripped')")
    parser.add_argument("--format", choices=["original", "jpg", "png", "webp"], default="original", help="Convert images to specific format")
    parser.add_argument("--in-place", action="store_true", help="Overwrite original files in-place")
    parser.add_argument("--inspect", nargs="?", const="DEFAULT", help="Inspect and audit metadata of an image without modifying")
    parser.add_argument("-w", "--workers", type=int, default=min(8, (os.cpu_count() or 4) * 2), help="Worker threads for batch processing")
    parser.add_argument("--no-srgb", action="store_true", help="Disable automatic ICC to sRGB conversion")
    parser.add_argument("--no-orient", action="store_true", help="Disable automatic EXIF orientation transposition")
    parser.add_argument("--no-anim", action="store_true", help="Disable cyberpunk boot/exit animations")
    parser.add_argument("-I", "--interactive", action="store_true", help="Launch interactive wizard even if arguments are passed")
    parser.add_argument("-v", "--version", action="version", version=f"{APP_NAME} v{VERSION}")

    args = parser.parse_args()

    # If no flags passed or explicit -I requested, launch interactive mode
    if len(sys.argv) == 1 or args.interactive:
        if args.no_anim:
            DEFAULT_CONFIG["animations"] = False
        interactive_terminal_app()
        return

    # Inspect mode
    if args.inspect is not None:
        target_path = None
        if args.inspect != "DEFAULT":
            target_path = Path(args.inspect)
        elif args.input:
            target_path = Path(args.input)

        if not target_path or not target_path.exists():
            console.print(f"[red]Error: Target file for inspection does not exist: {target_path}[/red]")
            sys.exit(1)

        info = inspect_image_metadata(target_path)
        display_inspection_report(info)
        return

    # CLI processing mode
    if not args.input:
        console.print("[red]Error: Missing input path. Specify -i/--input or run without arguments for interactive mode.[/red]")
        sys.exit(1)

    input_path = Path(args.input).expanduser().resolve()
    if not input_path.exists():
        console.print(f"[red]Error: Input path '{input_path}' does not exist.[/red]")
        sys.exit(1)

    convert_format = None if args.format == "original" else args.format
    convert_srgb = not args.no_srgb
    auto_orient = not args.no_orient

    # Single file mode
    if input_path.is_file():
        if args.in_place:
            output_path = input_path
        elif args.output:
            out_p = Path(args.output).expanduser().resolve()
            output_path = out_p if out_p.suffix else out_p / input_path.name
        else:
            ext = f".{convert_format}" if convert_format else input_path.suffix
            stem = f"{input_path.stem}{args.suffix}" if args.suffix else f"{input_path.stem}_stripped"
            output_path = input_path.parent / f"{stem}{ext}"

        console.print(f"[cyan]>> AI-STRIPPER processing: [bold]{input_path.name}[/bold][/cyan]")
        res = strip_image_metadata(
            input_path=input_path,
            output_path=output_path,
            quality=args.quality,
            target_format=convert_format,
            convert_srgb=convert_srgb,
            auto_orient=auto_orient
        )
        if res["status"] == "success":
            console.print(f"[bold green][+] Sanitized![/bold green] Saved {res['saved_bytes'] / 1024:.1f} KB -> [underline]{output_path}[/underline]")
        else:
            console.print(f"[bold red][!] Failed: {res['error']}[/bold red]")
            sys.exit(1)
        return

    # Directory batch mode
    images = collect_images(input_path, recursive=args.recursive)
    if not images:
        console.print(f"[yellow]No supported images found in '{input_path}'.[/yellow]")
        sys.exit(0)

    if args.in_place:
        output_dir = None
    elif args.output:
        output_dir = Path(args.output).expanduser().resolve()
    else:
        output_dir = input_path.parent / f"{input_path.name}_stripped"

    run_batch_processing(
        input_files=images,
        output_dir=output_dir,
        base_input_dir=input_path,
        quality=args.quality,
        suffix=args.suffix,
        target_format=convert_format,
        in_place=args.in_place,
        workers=args.workers,
        convert_srgb=convert_srgb,
        auto_orient=auto_orient
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Process interrupted by user. Exiting.[/yellow]")
        sys.exit(0)
