"""
╔══════════════════════════════════════════════════════════════════╗
║   nasssh.py  ·  dear-my-love  ·  encrypted memory transmission  ║
╚══════════════════════════════════════════════════════════════════╝
"""

import time
import sys
import io
import subprocess

# ── Force UTF-8 output on Windows ──────────────────────────────────
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ── Auto-install dependencies ───────────────────────────────────────
for _pkg in ["rich"]:
    try:
        __import__(_pkg)
    except ImportError:
        print(f"[sys] installing {_pkg}...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", _pkg, "-q"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )

# ── Rich imports ────────────────────────────────────────────────────
from rich.console  import Console
from rich.panel    import Panel
from rich.rule     import Rule
from rich.text     import Text
from rich.align    import Align
from rich.table    import Table
from rich.live     import Live
from rich.spinner  import Spinner
from rich.progress import (
    Progress, SpinnerColumn, BarColumn,
    TextColumn, TimeElapsedColumn, TaskProgressColumn,
)
from rich.tree     import Tree
from rich.columns  import Columns

# ── Standard library ────────────────────────────────────────────────
import os
import random
import hashlib
import platform
import textwrap
import uuid
from datetime import datetime

# ════════════════════════════════════════════════════════════════════
#  CONSTANTS & RUNTIME METADATA
# ════════════════════════════════════════════════════════════════════

ROSE        = "#e8a0a8"
ROSE_LIGHT  = "#f5d0d6"
ROSE_DARK   = "#c2596a"
GOLD        = "#cba76a"
GOLD_LIGHT  = "#e8d5a8"
TEXT        = "#d4b8be"
TEXT_DIM    = "#7a5d65"
CYAN        = "#7ecfcf"
CYAN_DIM    = "#3a7a7a"
GREEN       = "#7ecf9e"
GREEN_DIM   = "#3a7a5a"
AMBER       = "#cfb97e"
GREY        = "#4a3f48"

SESSION_ID  = str(uuid.uuid4()).upper()
TIMESTAMP   = datetime.now()
CHECKSUM    = hashlib.sha256(b"Nasha Putri Zaqirah").hexdigest()[:16].upper()
BUILD_HASH  = hashlib.md5(b"dear-my-love").hexdigest()[:8].upper()

console     = Console(highlight=False, legacy_windows=False)

DELAY_KEY   = 0.022
DELAY_SLOW  = 0.048
NOISE_CHARS = "█▓▒░│┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌"

# ════════════════════════════════════════════════════════════════════
#  HELPERS
# ════════════════════════════════════════════════════════════════════

def _sleep(s: float) -> None:
    time.sleep(s)

def _blank(n: int = 1) -> None:
    for _ in range(n):
        console.print()

def _ts() -> str:
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]

def _log(msg: str, level: str = "INFO") -> None:
    icons      = {"INFO": "●", "OK": "✔", "WARN": "▲", "ERR": "✖", "SYS": "◈", "DATA": "◆"}
    lvl_colors = {"INFO": CYAN, "OK": GREEN, "WARN": AMBER, "ERR": ROSE_DARK, "SYS": GREY, "DATA": GOLD}
    icon = icons.get(level, "·")
    lc   = lvl_colors.get(level, CYAN)
    console.print(
        f"[{GREY}]{_ts()}[/]  [{lc}]{icon}[/]  [{lc}]{level:<4}[/]  [{TEXT}]{msg}[/]"
    )
    _sleep(0.04)

def _typewrite(text: str, style: str = TEXT, delay: float = DELAY_KEY) -> None:
    for ch in text:
        console.print(ch, end="", style=style, highlight=False)
        _sleep(delay)
    console.print()

def _center_type(text: str, style: str = TEXT, delay: float = 0.025) -> None:
    pad = max(0, (console.width - len(text)) // 2) * " "
    console.print(pad, end="", highlight=False)
    _typewrite(text, style, delay)

def _glitch_reveal(final: str, style: str = ROSE_LIGHT, steps: int = 14) -> None:
    """Decode-style reveal: random noise → real text."""
    pad = max(0, (console.width - len(final)) // 2) * " "
    for step in range(steps + 1):
        ratio    = step / steps
        revealed = "".join(
            ch
            if (i / max(len(final), 1)) < ratio or random.random() < ratio * 0.7
            else random.choice(NOISE_CHARS)
            for i, ch in enumerate(final)
        )
        console.print(f"\r{pad}[{style}]{revealed}[/]", end="", highlight=False)
        _sleep(0.045)
    console.print()

def _para(text: str, style: str = TEXT, width: int = 72) -> None:
    for i, line in enumerate(textwrap.fill(text, width).splitlines()):
        prefix = "   " if i == 0 else ""
        console.print(f"[{style}]{prefix}{line}[/]")
        _sleep(0.010)
    _blank()

def _quote(text: str, width: int = 62) -> None:
    wrapped = textwrap.fill(text, width)
    console.print(
        Panel(
            f"[italic {ROSE_LIGHT}]{wrapped}[/]",
            border_style=ROSE_DARK, padding=(0, 3), expand=False,
        )
    )
    _blank()
    _sleep(0.2)

def _divider() -> None:
    console.print(Align.center(f"[{GREY}]─ ─ ─ ─ ─[/]"))
    _blank()
    _sleep(0.15)

def _section_rule(title: str) -> None:
    console.print(Rule(f"[{GREY}]{title}[/]", style=GREY + " dim"))
    _blank()
    _sleep(0.2)

# ════════════════════════════════════════════════════════════════════
#  STAGE 1  —  BOOT SEQUENCE
# ════════════════════════════════════════════════════════════════════

def boot_sequence() -> None:
    console.clear()

    banner_lines = [
        "██████╗ ███████╗ █████╗ ██████╗     ███╗   ███╗██╗   ██╗",
        "██╔══██╗██╔════╝██╔══██╗██╔══██╗    ████╗ ████║╚██╗ ██╔╝",
        "██║  ██║█████╗  ███████║██████╔╝    ██╔████╔██║ ╚████╔╝ ",
        "██║  ██║██╔══╝  ██╔══██║██╔══██╗    ██║╚██╔╝██║  ╚██╔╝  ",
        "██████╔╝███████╗██║  ██║██║  ██║    ██║ ╚═╝ ██║   ██║   ",
        "╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝     ╚═╝   ╚═╝   ",
        "                L  O  V  E                               ",
    ]
    gradient = [ROSE_DARK, ROSE_DARK, ROSE, ROSE, ROSE_LIGHT, GOLD, GOLD_LIGHT]

    _blank(2)
    for i, line in enumerate(banner_lines):
        console.print(Align.center(f"[bold {gradient[i]}]{line}[/]"))
        _sleep(0.06)

    _blank()
    console.print(Align.center(
        f"[{TEXT_DIM}]v2.0.26  ·  build {BUILD_HASH}  ·  encrypted memory module[/]"
    ))
    _blank(2)
    _sleep(0.5)

    boot_tasks = [
        ("SYS",  "Initializing runtime environment",                                 0.10),
        ("INFO", f"Python {sys.version.split()[0]}  ·  {platform.system()} {platform.machine()}", 0.08),
        ("INFO", f"Session ID   :  {SESSION_ID}",                                    0.08),
        ("INFO", f"Timestamp    :  {TIMESTAMP.isoformat()}",                         0.08),
        ("SYS",  "Loading memory module  [dear-my-love]",                            0.12),
        ("SYS",  "Mounting emotional filesystem ...",                                 0.10),
        ("INFO", f"Checksum     :  SHA-256/{CHECKSUM}",                              0.08),
        ("INFO", "Encryption   :  AES-256-GCM (simulated)",                          0.08),
        ("WARN", "WARNING: contents may affect heart rate",                           0.08),
        ("OK",   "All systems nominal. Proceeding ...",                               0.15),
    ]
    for level, msg, delay in boot_tasks:
        _log(msg, level)
        _sleep(delay)

    _blank()

    stages = [
        ("Decrypting payload",        0.008),
        ("Reconstructing memories",   0.011),
        ("Verifying integrity",       0.007),
        ("Rendering emotion engine",  0.009),
        ("Calibrating output",        0.006),
    ]

    with Progress(
        SpinnerColumn(spinner_name="dots2", style=ROSE),
        TextColumn(f"[{TEXT}]{{task.description}}", markup=True),
        BarColumn(
            bar_width=36, style=GREY,
            complete_style=ROSE_DARK, finished_style=ROSE_LIGHT,
        ),
        TaskProgressColumn(style=GOLD),
        TimeElapsedColumn(),
        console=console, transient=False,
    ) as prog:
        tasks = [prog.add_task(desc, total=100) for desc, _ in stages]
        while not all(prog.tasks[i].finished for i in range(len(stages))):
            for i in range(len(stages)):
                prog.advance(tasks[i], random.uniform(1, 6))
            _sleep(stages[0][1])

    _blank()
    console.print(Align.center(
        f"[bold {GREEN}]✔  SYSTEM READY  ─  memory transmission authorized[/]"
    ))
    _blank(2)
    _sleep(1.0)
    console.clear()


# ════════════════════════════════════════════════════════════════════
#  STAGE 2  —  SYSTEM DASHBOARD
# ════════════════════════════════════════════════════════════════════

def system_dashboard() -> None:

    sys_table = Table(show_header=False, box=None, padding=(0, 2), expand=False)
    sys_table.add_column(style=TEXT_DIM, justify="right", width=18)
    sys_table.add_column(style=f"italic {TEXT}")
    sys_table.add_row("runtime",    f"Python {sys.version.split()[0]}")
    sys_table.add_row("platform",   f"{platform.system()} {platform.release()} ({platform.machine()})")
    sys_table.add_row("timestamp",  TIMESTAMP.strftime("%A, %d %B %Y  ·  %H:%M:%S"))
    sys_table.add_row("session",    f"[dim]{SESSION_ID}[/dim]")
    sys_table.add_row("checksum",   f"[{CYAN_DIM}]SHA256/{CHECKSUM}[/]")
    sys_table.add_row("module",     "[bold]dear-my-love[/bold]  /  nasssh.py")
    sys_table.add_row("status",     f"[bold {GREEN}]AUTHORIZED[/bold {GREEN}]")

    tree = Tree(f"[bold {ROSE}]dear-my-love/[/]", guide_style=GREY)
    tree.add(f"[{TEXT}]index.html[/]           [{TEXT_DIM}]# website[/]")
    tree.add(f"[{ROSE_LIGHT}]nasssh.py[/]            [{TEXT_DIM}]# you are here[/]")
    tree.add(f"[{GOLD}]untu seseorang.ipynb[/]  [{TEXT_DIM}]# notebook[/]")
    tree.add(f"[{CYAN_DIM}]README.md[/]             [{TEXT_DIM}]# documentation[/]")

    recip = Table.grid(padding=(0, 2))
    recip.add_column(style=TEXT_DIM, justify="right", width=10)
    recip.add_column()
    recip.add_row("to",   f"[bold italic {ROSE_LIGHT}]Nasha Putri Zaqirah[/]")
    recip.add_row("from", f"[italic {TEXT_DIM}]seseorang yang pernah diam-diam menyukai kamu[/]")
    recip.add_row("type", f"[{CYAN_DIM}]ENCRYPTED_LETTER[/]  ·  [{GOLD}]PRIORITY: SINCERE[/]")

    console.print(
        Columns(
            [
                Panel(sys_table, border_style=GREY,      title=f"[{GREY}]SYS_INFO",      padding=(1, 2)),
                Panel(tree,      border_style=ROSE_DARK,  title=f"[{ROSE_DARK}]FS_TREE",  padding=(1, 2)),
            ],
            equal=True, expand=True,
        )
    )
    _blank()
    console.print(
        Panel(
            Align.center(recip),
            border_style=ROSE,
            title=f"[{ROSE}]✦  TRANSMISSION METADATA  ✦",
            subtitle=f"[{TEXT_DIM}]payload integrity: {CHECKSUM}",
            padding=(1, 4),
        )
    )
    _blank()
    _sleep(0.5)


# ════════════════════════════════════════════════════════════════════
#  STAGE 3  —  DECODE ANIMATION
# ════════════════════════════════════════════════════════════════════

def decode_animation() -> None:
    _section_rule("DECRYPTION ENGINE  ·  AES-256-GCM")

    raw     = "Nasha Putri Zaqirah".encode()
    hex_str = " ".join(f"{b:02X}" for b in raw)
    bin_str = " ".join(f"{b:08b}" for b in raw[:6]) + "  ···"

    console.print(f"[{GREY}]  raw hex  :  [{CYAN_DIM}]{hex_str}[/]")
    _sleep(0.3)
    console.print(f"[{GREY}]  binary   :  [{GREEN_DIM}]{bin_str}[/]")
    _sleep(0.3)
    console.print(f"[{GREY}]  decoded  :  ", end="")
    _typewrite("Nasha Putri Zaqirah", style=f"bold {ROSE_LIGHT}", delay=0.055)
    _sleep(0.4)

    _blank()
    _log("Payload decrypted successfully",         "OK")
    _log("Hash verified: no tampering detected",   "OK")
    _log("Proceeding to render message...",         "INFO")
    _blank()

    _glitch_reveal(
        "N a s h a   P u t r i   Z a q i r a h",
        style=f"bold {ROSE_LIGHT}", steps=18,
    )
    _blank(2)
    _sleep(0.8)


# ════════════════════════════════════════════════════════════════════
#  STAGE 4  —  THE LETTER
# ════════════════════════════════════════════════════════════════════

def render_letter() -> None:
    console.clear()
    _section_rule("MESSAGE PAYLOAD  ·  BEGIN TRANSMISSION")

    console.print(Align.center(
        f"[italic {ROSE_LIGHT}]Untuk  "
        f"[bold {GOLD_LIGHT}]Nasha Putri Zaqirah[/bold {GOLD_LIGHT}],[/]"
    ))
    _blank()
    _sleep(0.5)

    # ── Letter blocks (type, content) ─────────────────────────────
    # types: "para" | "center" | "center_i" | "quote" | "glitch"
    blocks = [
        ("01", [
            ("para",     "Mungkin ini adalah cara yang agak aneh untuk menulis sesuatu tentang "
                         "seseorang. Bukan di buku harian, bukan di surat kertas yang dilipat rapi, "
                         "dan bukan juga pesan singkat yang dikirim lewat chat. Aku menulis ini di "
                         "sebuah file, di dalam notebook yang biasanya dipakai untuk kode, logika, "
                         "dan perhitungan."),
            ("para",     "Namun di antara semua baris kode itu, ada satu bagian yang tidak berisi "
                         "angka, tidak berisi rumus, tidak berisi algoritma."),
            ("center",   "Bagian itu berisi namamu."),
            ("glitch",   "Nasha Putri Zaqirah."),
        ]),
        ("02", [
            ("para",     "Aku tidak tahu apakah suatu hari nanti kamu akan membaca ini atau tidak. "
                         "Bisa jadi tidak pernah. Bisa jadi file ini hanya akan tersimpan di suatu "
                         "folder, di dalam komputer, bertahun-tahun lamanya. Tapi aku tetap "
                         "menuliskannya, karena ada hal-hal yang terkadang lebih baik disimpan dalam "
                         "tulisan daripada hanya dipikirkan sendirian."),
            ("para",     "Aku mengenal banyak orang dalam hidupku, tapi ada beberapa orang yang "
                         "entah kenapa terasa berbeda. Bukan karena mereka melakukan sesuatu yang "
                         "besar atau dramatis, tapi karena kehadiran mereka saja sudah cukup membuat "
                         "hari terasa sedikit lebih menarik."),
            ("quote",    "Dan jujur saja, kamu adalah salah satu orang itu."),
        ]),
        ("03", [
            ("para",     "Aku tidak tahu apakah kamu pernah menyadarinya atau tidak. Mungkin tidak. "
                         "Bahkan kemungkinan besar memang tidak. Tapi setiap kali aku melihatmu, ada "
                         "sesuatu yang membuatku berhenti sebentar dari apa yang sedang kupikirkan."),
            ("center",   "Bukan karena sesuatu yang berlebihan."),
            ("center_i", "Hanya karena kamu."),
        ]),
        ("04", [
            ("para",     "Kadang aku berpikir, aneh juga bagaimana seseorang bisa tiba-tiba menjadi "
                         "penting dalam pikiran kita, padahal mungkin kita tidak terlalu sering "
                         "berbicara. Dunia ini penuh dengan orang, penuh dengan wajah yang kita lihat "
                         "setiap hari, tapi hanya sedikit yang benar-benar kita ingat."),
            ("center_i", "Dan entah kenapa, kamu termasuk yang selalu teringat."),
        ]),
        ("05", [
            ("para",     "Aku tidak tahu harus menyebut ini sebagai apa. Mungkin sekadar kagum. "
                         "Mungkin rasa suka yang sederhana. Atau mungkin hanya perasaan yang muncul "
                         "tanpa alasan yang jelas."),
            ("para",     "Yang aku tahu, namamu pernah terlintas di pikiranku lebih dari sekali."),
            ("center",   "Bahkan mungkin lebih sering daripada yang seharusnya."),
        ]),
        ("06", [
            ("para",     "Aku juga sadar bahwa hidup setiap orang berjalan dengan cara yang berbeda. "
                         "Kita semua punya cerita masing-masing, punya rencana masing-masing, dan "
                         "punya jalan yang belum tentu sama. Bisa saja suatu hari nanti kita benar-"
                         "benar berjalan ke arah yang berbeda tanpa pernah menyadari kapan tepatnya "
                         "kita berpisah arah."),
            ("center",   "Itu hal yang sangat mungkin terjadi."),
        ]),
        ("07", [
            ("para",     "Tapi sebelum waktu berjalan terlalu jauh, sebelum kenangan berubah menjadi "
                         "sesuatu yang samar, aku ingin meninggalkan sesuatu yang sederhana: sebuah "
                         "tulisan yang mengatakan bahwa pernah ada seseorang yang menganggapmu "
                         "istimewa dengan caranya sendiri."),
            ("center",   "Tanpa perlu kamu lakukan apa-apa."),
            ("center",   "Tanpa perlu kamu sadari."),
        ]),
        ("08", [
            ("para",     "Aku tidak berharap sesuatu yang besar dari tulisan ini. Tidak ada tuntutan, "
                         "tidak ada harapan yang berat. Ini hanya sebuah cara untuk menyimpan satu "
                         "perasaan kecil agar tidak hilang begitu saja."),
            ("para",     "Karena kadang, yang paling berharga dari sebuah perasaan bukanlah apakah "
                         "perasaan itu dibalas atau tidak."),
            ("quote",    "Melainkan fakta bahwa perasaan itu pernah ada."),
            ("para",     "Dan aku tidak ingin pura-pura bahwa itu tidak pernah terjadi."),
        ]),
        ("09", [
            ("para",     "Jika suatu hari nanti aku membuka kembali file ini, mungkin aku akan "
                         "tersenyum sendiri dan mengingat masa di mana semuanya terasa sederhana. "
                         "Masa di mana seseorang bisa menjadi alasan kecil untuk merasa senang "
                         "dalam satu hari."),
            ("para",     "Dan jika kebetulan suatu hari kamu benar-benar membaca ini, aku hanya "
                         "ingin kamu tahu satu hal."),
            ("quote",    "Di antara miliaran orang di dunia ini, pernah ada seseorang yang "
                         "menuliskan namamu dengan sangat hati-hati di sebuah notebook, hanya "
                         "karena dia tidak ingin melupakannya."),
        ]),
        ("10", [
            ("glitch",   "Nasha Putri Zaqirah."),
            ("para",     "Nama yang sederhana, tapi pernah menjadi bagian dari sebuah cerita kecil "
                         "dalam hidup seseorang."),
            ("center",   "Mungkin cerita itu tidak besar."),
            ("center",   "Mungkin juga tidak penting bagi dunia."),
            ("para",     "Tapi bagi orang yang menuliskannya, cerita itu cukup berarti untuk "
                         "diabadikan."),
            ("para",     "Dan mungkin, hanya mungkin, suatu hari nanti aku akan membuka file ini "
                         "lagi dan tersenyum karena pernah mengenal seseorang sepertimu."),
            ("center_i", "Terima kasih sudah menjadi bagian kecil dari cerita itu."),
        ]),
    ]

    total = len(blocks)
    for blk_num, items in blocks:
        _log(f"transmitting block {blk_num} / {total:02d} ...", "DATA")
        _blank()
        for kind, content in items:
            if kind == "para":
                _para(content)
            elif kind == "center":
                _center_type(content, TEXT)
                _blank()
            elif kind == "center_i":
                _center_type(content, f"italic {ROSE_LIGHT}")
                _blank()
            elif kind == "quote":
                _quote(content)
            elif kind == "glitch":
                _glitch_reveal(content, style=f"bold italic {ROSE_LIGHT}", steps=16)
                _blank()
        _divider()

    console.print(
        Align.right(
            f"[italic {TEXT_DIM}]— seseorang yang pernah diam-diam menyukai kamu[/]",
            width=console.width - 4,
        )
    )
    _blank()
    _log("END OF TRANSMISSION  ·  all blocks received", "OK")
    _blank(2)


# ════════════════════════════════════════════════════════════════════
#  STAGE 5  —  POEM
# ════════════════════════════════════════════════════════════════════

def render_poem() -> None:
    _section_rule("EMBEDDED SUBROUTINE  ·  catatan terakhir")

    poem_lines = [
        f"[italic {TEXT_DIM}]ada nama yang tidak pernah benar-benar pergi",
        f"[italic {TEXT}]meski bibir tidak pernah mengucapkannya keras-keras",
        "",
        f"[italic {TEXT_DIM}]tertulis di sini, di antara fungsi dan variabel,",
        f"[italic {TEXT}]seperti konstanta yang tidak berubah —",
        "",
    ]
    for rendered in poem_lines:
        if rendered == "":
            _blank()
        else:
            console.print(Align.center(f"[{rendered}]"))
            _sleep(0.18)

    _blank()
    _glitch_reveal("Nasha Putri Zaqirah.", style=f"bold italic {ROSE_LIGHT}", steps=20)
    _blank(2)


# ════════════════════════════════════════════════════════════════════
#  STAGE 6  —  TRANSMISSION REPORT
# ════════════════════════════════════════════════════════════════════

def transmission_report() -> None:
    elapsed = (datetime.now() - TIMESTAMP).total_seconds()

    report = Table(show_header=False, box=None, padding=(0, 2), expand=False)
    report.add_column(style=TEXT_DIM, justify="right", width=20)
    report.add_column(style=TEXT)
    report.add_row("session",          f"[dim]{SESSION_ID}[/dim]")
    report.add_row("runtime",          f"[{CYAN}]{elapsed:.3f}s[/]")
    report.add_row("blocks",           f"[{GREEN}]10 / 10  ──  100%  ✔[/]")
    report.add_row("payload checksum", f"[{CYAN_DIM}]{CHECKSUM}[/]")
    report.add_row("integrity",        f"[bold {GREEN}]VERIFIED[/]")
    report.add_row("recipient",        f"[bold italic {ROSE_LIGHT}]Nasha Putri Zaqirah[/]")
    report.add_row("status",           f"[bold {GREEN}]DELIVERED  ✔[/]")

    console.print(
        Panel(
            Align.center(report),
            border_style=ROSE,
            padding=(1, 4),
            title=f"[{ROSE}]✦  TRANSMISSION REPORT  ✦",
            subtitle=f"[{TEXT_DIM}]dear-my-love  ·  build {BUILD_HASH}[/]",
        )
    )
    _blank()


# ════════════════════════════════════════════════════════════════════
#  STAGE 7  —  OUTRO
# ════════════════════════════════════════════════════════════════════

def outro() -> None:
    name_text = Text(justify="center")
    name_text.append("\n")
    name_text.append("Nasha Putri Zaqirah\n", style=f"bold italic {ROSE_LIGHT}")
    name_text.append("\n")
    name_text.append("diabadikan dalam sebuah repository\n", style=f"italic {TEXT_DIM}")
    name_text.append("dengan sepenuh hati  ♡",               style=f"italic {TEXT_DIM}")
    name_text.append("\n")

    console.print(
        Panel(
            Align.center(name_text),
            border_style=ROSE_DARK,
            padding=(2, 8),
            title=f"[{GOLD}]✦  ♡  ✦[/]",
            subtitle=f"[{TEXT_DIM}]— akhir dari catatan ini —[/]",
        )
    )
    _blank()
    console.print(
        Align.center(
            f"[{GREY}]{_ts()}  [{GREEN}]✔[/]  [{TEXT_DIM}]session terminated gracefully[/][/]"
        )
    )
    _blank(2)


# ════════════════════════════════════════════════════════════════════
#  STAGE 8  —  INFINITE LOOP ANIMATION
# ════════════════════════════════════════════════════════════════════

# Heart frames — two sizes that alternate for "pulse" effect
_HEART_BIG = [
    "   ██████  ██████   ",
    " ██████████████████ ",
    " ████████████████████",
    "  ████████████████  ",
    "   ██████████████   ",
    "     ██████████     ",
    "       ██████       ",
    "         ██         ",
]
_HEART_SMALL = [
    "  ████  ████  ",
    " ████████████ ",
    " ████████████ ",
    "  ██████████  ",
    "   ████████   ",
    "    ██████    ",
    "      ██      ",
]

# Orbit chars for the spinning ring around the name
_ORBIT  = list("·  ✦  ·  ♡  ·  ✦  ·  ♡  ")
_WAVES  = ["▁▂▃▄▅▆▇█▇▆▅▄▃▂▁", "▂▃▄▅▆▇█▇▆▅▄▃▂▁▂",
           "▃▄▅▆▇█▇▆▅▄▃▂▁▂▃", "▄▅▆▇█▇▆▅▄▃▂▁▂▃▄"]


def _build_frame(tick: int, W: int) -> Text:
    """Build one animation frame as a Rich Text object."""
    t   = Text(justify="center")
    fps = 18  # logical ticks per second

    # ── 1. Pulsing heart ──────────────────────────────────────────
    # Switch between big/small every 18 ticks (≈1 s)
    big    = (tick // fps) % 2 == 0
    heart  = _HEART_BIG if big else _HEART_SMALL
    # Cycle colour through a rose-gold palette
    hue    = [ROSE_DARK, ROSE, ROSE_LIGHT, GOLD_LIGHT, GOLD, ROSE_LIGHT, ROSE][tick % 7]

    t.append("\n")
    for line in heart:
        pad = max(0, (W - len(line)) // 2) * " "
        t.append(pad + line + "\n", style=f"bold {hue}")

    # ── 2. Pulsing glow label ─────────────────────────────────────
    t.append("\n")
    glows  = [ROSE_DARK, ROSE, ROSE_LIGHT, GOLD_LIGHT, ROSE_LIGHT, ROSE, ROSE_DARK]
    g_col  = glows[tick % len(glows)]
    name   = "Nasha Putri Zaqirah"
    pad    = max(0, (W - len(name)) // 2) * " "
    t.append(pad + name + "\n", style=f"bold italic {g_col}")

    # ── 3. Orbiting ring ─────────────────────────────────────────
    ring_w  = min(W - 4, 48)
    shifted = (_ORBIT * 4)[tick % len(_ORBIT): tick % len(_ORBIT) + ring_w]
    ring_s  = "".join(shifted)[:ring_w]
    r_pad   = max(0, (W - ring_w) // 2) * " "
    r_col   = [ROSE_DARK, ROSE, ROSE_LIGHT, GOLD, ROSE_LIGHT, ROSE, ROSE_DARK][tick % 7]
    t.append("\n" + r_pad + ring_s + "\n", style=f"dim {r_col}")

    # ── 4. Wave bar ───────────────────────────────────────────────
    wave_s = (_WAVES[tick % len(_WAVES)] * ((W // 15) + 2))[:W - 2]
    w_pad  = max(0, (W - len(wave_s)) // 2) * " "
    w_col  = [CYAN_DIM, CYAN_DIM, ROSE_DARK, ROSE_DARK][tick % 4]
    t.append("\n" + w_pad + wave_s + "\n", style=f"dim {w_col}")

    # ── 5. Status footer ─────────────────────────────────────────
    elapsed = tick / fps
    mins    = int(elapsed) // 60
    secs    = int(elapsed) % 60
    msecs   = int((elapsed - int(elapsed)) * 1000)
    status_plain = f"{_ts()}  looping  ·  {mins:02d}:{secs:02d}.{msecs:03d}  ·  ctrl+c to exit"
    s_pad = max(0, (W - len(status_plain)) // 2) * " "
    t.append("\n" + s_pad + status_plain + "\n", style=f"dim {GREY}")

    return t


def final_loop() -> None:
    """Infinite pulsing animation — runs until Ctrl+C."""
    console.print(
        Align.center(f"[{TEXT_DIM}][ animation loop started — ctrl+c to exit ][/]")
    )
    _blank()
    _sleep(0.6)

    W    = max(console.width, 40)
    tick = 0

    with Live(
        console=console,
        refresh_per_second=18,
        screen=False,
        vertical_overflow="visible",
    ) as live:
        while True:
            frame = _build_frame(tick, W)
            live.update(frame)
            tick += 1
            _sleep(1 / 18)


# ════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ════════════════════════════════════════════════════════════════════

def main() -> None:
    try:
        boot_sequence()
        system_dashboard()
        decode_animation()
        render_letter()
        render_poem()
        transmission_report()
        outro()
        final_loop()
    except KeyboardInterrupt:
        _blank(2)
        _log("session interrupted by user", "WARN")
        console.print(
            Align.center(f"[italic {TEXT_DIM}]— dibiarkan berlalu dengan tenang —[/]")
        )
        _blank()


if __name__ == "__main__":
    main()
