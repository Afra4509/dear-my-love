"""
╔══════════════════════════════════════════════════════════╗
║          untuk_nasha.py  —  sebuah catatan kecil         ║
╚══════════════════════════════════════════════════════════╝

Jalankan di terminal atau Python online:
  python nasha.py

Memerlukan:  pip install rich
(tersedia di Replit, Programiz, OnlinePython, dll.)
"""

import time
import sys

# ── Pastikan rich tersedia ──────────────────────────────────
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.rule import Rule
    from rich.text import Text
    from rich.align import Align
    from rich.columns import Columns
    from rich.padding import Padding
    from rich import print as rprint
    from rich.style import Style
    from rich.live import Live
    from rich.spinner import Spinner
    from rich.table import Table
except ImportError:
    print("\nMenginstal rich...\n")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "rich", "-q"])
    from rich.console import Console
    from rich.panel import Panel
    from rich.rule import Rule
    from rich.text import Text
    from rich.align import Align
    from rich.padding import Padding
    from rich import print as rprint
    from rich.style import Style
    from rich.live import Live
    from rich.spinner import Spinner
    from rich.table import Table


# ═══════════════════════════════════════════════════════════
#  Konfigurasi
# ═══════════════════════════════════════════════════════════

ROSE        = "#e8a0a8"
ROSE_LIGHT  = "#f5d0d6"
ROSE_DARK   = "#c2596a"
GOLD        = "#cba76a"
GOLD_LIGHT  = "#e8d5a8"
TEXT        = "#d4b8be"
TEXT_DIM    = "#7a5d65"
INK         = "grey11"

console = Console(highlight=False)

DELAY_FAST   = 0.018
DELAY_NORMAL = 0.028
DELAY_SLOW   = 0.050


# ═══════════════════════════════════════════════════════════
#  Helpers
# ═══════════════════════════════════════════════════════════

def sleep(s: float) -> None:
    time.sleep(s)


def pause(s: float = 0.6) -> None:
    sleep(s)


def typewrite(text: str, style: str = TEXT, delay: float = DELAY_NORMAL) -> None:
    """Cetak teks karakter per karakter."""
    for char in text:
        console.print(char, end="", style=style, highlight=False)
        sleep(delay)
    console.print()


def typewrite_center(text: str, style: str = TEXT, delay: float = DELAY_NORMAL, width: int = 70) -> None:
    """Cetak teks karakter per karakter, rata tengah."""
    padding = max(0, (width - len(text)) // 2) * " "
    console.print(padding, end="", highlight=False)
    typewrite(text, style, delay)


def rule(title: str = "", style: str = ROSE_DARK) -> None:
    if title:
        console.print(Rule(f"[{ROSE_DARK}]{title}[/]", style=style))
    else:
        console.print(Rule(style=style + " dim"))
    pause(0.3)


def blank(n: int = 1) -> None:
    for _ in range(n):
        console.print()


def fade_in(lines: list[tuple[str, str]], delay_between: float = 0.08) -> None:
    """Tampilkan baris-baris dengan jeda antar baris."""
    for text, style in lines:
        console.print(Align.center(f"[{style}]{text}[/]"))
        sleep(delay_between)


# ═══════════════════════════════════════════════════════════
#  Layar pembuka  (intro splash)
# ═══════════════════════════════════════════════════════════

def intro_splash() -> None:
    console.clear()
    sleep(0.4)

    # Spinner loading
    with Live(
        Align.center(Spinner("dots2", text=f"[{TEXT_DIM}] memuat kenangan ...[/]", style=ROSE_DARK)),
        refresh_per_second=20,
        console=console,
    ) as live:
        sleep(2.2)

    console.clear()
    sleep(0.3)

    # Big ASCII title
    art = [
        r"  _   _           _           ",
        r" | \ | |         | |          ",
        r" |  \| | __ _ ___| |__   __ _ ",
        r" | . ` |/ _` / __| '_ \ / _` |",
        r" | |\  | (_| \__ \ | | | (_| |",
        r" |_| \_|\__,_|___/_| |_|\__,_|",
    ]
    blank(2)
    for i, line in enumerate(art):
        alpha = [ROSE_DARK, ROSE, ROSE_LIGHT, GOLD_LIGHT, GOLD, ROSE_LIGHT][i]
        console.print(Align.center(f"[bold {alpha}]{line}[/]"))
        sleep(0.08)

    blank()
    console.print(Align.center(f"[italic {TEXT_DIM}]Putri Zaqirah[/]"))
    blank(2)
    pause(0.8)


# ═══════════════════════════════════════════════════════════
#  Metadata header
# ═══════════════════════════════════════════════════════════

def print_metadata() -> None:
    table = Table.grid(padding=(0, 3))
    table.add_column(style=TEXT_DIM, justify="right")
    table.add_column(style=TEXT)

    table.add_row("[dim]file[/dim]",    "[italic]untuk_nasha.py[/italic]")
    table.add_row("[dim]kepada[/dim]",  f"[bold italic {ROSE_LIGHT}]Nasha Putri Zaqirah[/]")
    table.add_row("[dim]dari[/dim]",    "[italic]seseorang yang pernah diam-diam menyukai kamu[/italic]")
    table.add_row("[dim]catatan[/dim]", "[italic dim]ditulis di antara baris kode[/italic dim]")

    console.print(
        Panel(
            Align.center(table),
            border_style=ROSE_DARK,
            padding=(1, 4),
            title=f"[{ROSE}]✦  sebuah catatan kecil  ✦[/]",
            subtitle=f"[{TEXT_DIM}]— buka dengan hati yang tenang —[/]",
        )
    )
    blank()
    pause(0.5)


# ═══════════════════════════════════════════════════════════
#  Surat
# ═══════════════════════════════════════════════════════════

def print_letter() -> None:

    rule(f" ✦  Surat  ✦ ")
    blank()

    # Salutation
    console.print(
        Align.center(
            f"[italic {ROSE_LIGHT}]Untuk [bold {GOLD_LIGHT}]Nasha Putri Zaqirah[/bold {GOLD_LIGHT}],[/]"
        )
    )
    blank()
    pause(0.5)

    # ── Paragraf ─────────────────────────────────────────
    paragraphs = [

        ( # 1
            f"Mungkin ini adalah cara yang agak aneh untuk menulis sesuatu tentang "
            f"seseorang. Bukan di buku harian, bukan di surat kertas yang dilipat rapi, "
            f"dan bukan juga pesan singkat yang dikirim lewat chat. Aku menulis ini di "
            f"sebuah [italic]file[/italic], di dalam notebook yang biasanya dipakai untuk "
            f"kode, logika, dan perhitungan.",
            TEXT,
        ),
        ( # 2
            f"Namun di antara semua baris kode itu, ada satu bagian yang tidak berisi "
            f"angka, tidak berisi rumus, tidak berisi algoritma.",
            TEXT,
        ),
    ]

    for text, style in paragraphs:
        _paragraph(text, style)

    # name reveal
    _center_reveal("Bagian itu berisi namamu.", TEXT)
    blank()
    _name_reveal("Nasha Putri Zaqirah.")
    blank()
    pause(0.5)

    _rule_ornament()

    _paragraph(
        "Aku tidak tahu apakah suatu hari nanti kamu akan membaca ini atau tidak. "
        "Bisa jadi tidak pernah. Bisa jadi file ini hanya akan tersimpan di suatu folder, "
        "di dalam komputer, bertahun-tahun lamanya. Tapi aku tetap menuliskannya, karena "
        "ada hal-hal yang terkadang lebih baik disimpan dalam tulisan daripada hanya "
        "dipikirkan sendirian.",
        TEXT,
    )

    _paragraph(
        "Aku mengenal banyak orang dalam hidupku, tapi ada beberapa orang yang entah "
        "kenapa terasa berbeda. Bukan karena mereka melakukan sesuatu yang besar atau "
        "dramatis, tapi karena kehadiran mereka saja sudah cukup membuat hari terasa "
        "sedikit lebih menarik.",
        TEXT,
    )

    _quote("Dan jujur saja, kamu adalah salah satu orang itu.")
    pause(0.4)

    _rule_ornament()

    _paragraph(
        "Aku tidak tahu apakah kamu pernah menyadarinya atau tidak. Mungkin tidak. "
        "Bahkan kemungkinan besar memang tidak. Tapi setiap kali aku melihatmu, ada "
        "sesuatu yang membuatku berhenti sebentar dari apa yang sedang kupikirkan.",
        TEXT,
    )

    _center_reveal("Bukan karena sesuatu yang berlebihan.", TEXT)
    _center_reveal("Hanya karena kamu.", f"italic {ROSE_LIGHT}")
    blank()
    pause(0.4)

    _rule_ornament()

    _paragraph(
        "Kadang aku berpikir, aneh juga bagaimana seseorang bisa tiba-tiba menjadi "
        "penting dalam pikiran kita, padahal mungkin kita tidak terlalu sering berbicara. "
        "Dunia ini penuh dengan orang, penuh dengan wajah yang kita lihat setiap hari, "
        "tapi hanya sedikit yang benar-benar kita ingat.",
        TEXT,
    )

    _center_reveal("Dan entah kenapa, kamu termasuk yang selalu teringat.", f"italic {ROSE}")
    blank()
    pause(0.4)

    _rule_ornament()

    _paragraph(
        "Aku tidak tahu harus menyebut ini sebagai apa. Mungkin sekadar kagum. "
        "Mungkin rasa suka yang sederhana. Atau mungkin hanya perasaan yang muncul "
        "tanpa alasan yang jelas.",
        TEXT,
    )

    _paragraph("Yang aku tahu, namamu pernah terlintas di pikiranku lebih dari sekali.", TEXT)

    _center_reveal("Bahkan mungkin lebih sering daripada yang seharusnya.", f"italic {TEXT}")
    blank()
    pause(0.4)

    _rule_ornament()

    _paragraph(
        "Aku juga sadar bahwa hidup setiap orang berjalan dengan cara yang berbeda. "
        "Kita semua punya cerita masing-masing, punya rencana masing-masing, dan punya "
        "jalan yang belum tentu sama. Bisa saja suatu hari nanti kita benar-benar berjalan "
        "ke arah yang berbeda tanpa pernah menyadari kapan tepatnya kita berpisah arah.",
        TEXT,
    )

    _center_reveal("Itu hal yang sangat mungkin terjadi.", TEXT)
    blank()
    pause(0.4)

    _rule_ornament()

    _paragraph(
        "Tapi sebelum waktu berjalan terlalu jauh, sebelum kenangan berubah menjadi "
        "sesuatu yang samar, aku ingin meninggalkan sesuatu yang sederhana: sebuah "
        "tulisan yang mengatakan bahwa pernah ada seseorang yang menganggapmu istimewa "
        "dengan caranya sendiri.",
        TEXT,
    )

    _center_reveal("Tanpa perlu kamu lakukan apa-apa.", TEXT)
    _center_reveal("Tanpa perlu kamu sadari.", TEXT)
    blank()
    pause(0.4)

    _rule_ornament()

    _paragraph(
        "Aku tidak berharap sesuatu yang besar dari tulisan ini. Tidak ada tuntutan, "
        "tidak ada harapan yang berat. Ini hanya sebuah cara untuk menyimpan satu perasaan "
        "kecil agar tidak hilang begitu saja.",
        TEXT,
    )

    _paragraph(
        "Karena kadang, yang paling berharga dari sebuah perasaan bukanlah apakah "
        "perasaan itu dibalas atau tidak.",
        TEXT,
    )

    _quote("Melainkan fakta bahwa perasaan itu pernah ada.")

    _paragraph("Dan aku tidak ingin pura-pura bahwa itu tidak pernah terjadi.", TEXT)
    pause(0.4)

    _rule_ornament()

    _paragraph(
        "Jika suatu hari nanti aku membuka kembali file ini, mungkin aku akan tersenyum "
        "sendiri dan mengingat masa di mana semuanya terasa sederhana. Masa di mana "
        "seseorang bisa menjadi alasan kecil untuk merasa senang dalam satu hari.",
        TEXT,
    )

    _paragraph(
        "Dan jika kebetulan suatu hari kamu benar-benar membaca ini, aku hanya ingin "
        "kamu tahu satu hal.",
        TEXT,
    )

    _quote(
        "Di antara miliaran orang di dunia ini, pernah ada seseorang yang menuliskan "
        "namamu dengan sangat hati-hati di sebuah notebook, hanya karena dia tidak ingin "
        "melupakannya."
    )

    _name_reveal("Nasha Putri Zaqirah.")
    blank()

    _paragraph(
        "Nama yang sederhana, tapi pernah menjadi bagian dari sebuah cerita kecil "
        "dalam hidup seseorang.",
        TEXT,
    )

    _center_reveal("Mungkin cerita itu tidak besar.", TEXT)
    _center_reveal("Mungkin juga tidak penting bagi dunia.", TEXT)
    blank()

    _paragraph(
        "Tapi bagi orang yang menuliskannya, cerita itu cukup berarti untuk diabadikan.",
        TEXT,
    )
    pause(0.4)

    _rule_ornament()

    _paragraph(
        "Dan mungkin, hanya mungkin, suatu hari nanti aku akan membuka file ini lagi "
        "dan tersenyum karena pernah mengenal seseorang sepertimu.",
        TEXT,
    )

    blank()
    _center_reveal("Terima kasih sudah menjadi bagian kecil dari cerita itu.", f"italic {ROSE_LIGHT}")
    blank(2)

    # Closing signature
    console.print(
        Align.right(
            f"[italic {TEXT_DIM}]— seseorang yang pernah diam-diam menyukai kamu[/]",
            width=console.width - 4,
        )
    )
    blank(2)


# ═══════════════════════════════════════════════════════════
#  Puisi penutup
# ═══════════════════════════════════════════════════════════

def print_poem() -> None:
    rule(f" ✦  Catatan Terakhir  ✦ ")
    blank()

    lines = [
        ("ada nama yang tidak pernah benar-benar pergi",  TEXT),
        ("meski bibir tidak pernah mengucapkannya keras-keras", TEXT_DIM),
        ("", ""),
        ("tertulis di sini, di antara fungsi dan variabel,", TEXT),
        ("seperti konstanta yang tidak berubah —", TEXT_DIM),
        ("", ""),
        ("Nasha Putri Zaqirah.",  f"bold italic {ROSE_LIGHT}"),
    ]

    for line, style in lines:
        if line == "":
            blank()
            sleep(0.12)
        else:
            if style == f"bold italic {ROSE_LIGHT}":
                blank()
                _name_reveal(line, large=False)
                blank()
            else:
                console.print(Align.center(f"[italic {style}]{line}[/]"))
                sleep(0.18)

    blank(2)


# ═══════════════════════════════════════════════════════════
#  Layar penutup
# ═══════════════════════════════════════════════════════════

def outro() -> None:
    rule()
    blank()

    # Final panel
    final_text = Text(justify="center")
    final_text.append("Nasha Putri Zaqirah\n", style=f"bold italic {ROSE_LIGHT}")
    final_text.append("\n", style="")
    final_text.append("diabadikan dalam sebuah notebook\n", style=f"italic {TEXT_DIM}")
    final_text.append("dengan sepenuh hati  ♡", style=f"italic {TEXT_DIM}")

    console.print(
        Panel(
            Align.center(final_text),
            border_style=ROSE_DARK,
            padding=(2, 6),
            title=f"[{GOLD}]✦  ♡  ✦[/]",
            subtitle=f"[{TEXT_DIM}]— akhir dari catatan ini —[/]",
        )
    )
    blank(2)


# ═══════════════════════════════════════════════════════════
#  Komponen internal (private)
# ═══════════════════════════════════════════════════════════

def _paragraph(text: str, style: str, width: int = 74) -> None:
    """Cetak paragraf dengan wrapping dan indentasi."""
    import textwrap
    wrapped = textwrap.fill(text, width=width)
    for i, line in enumerate(wrapped.splitlines()):
        prefix = "  " if i == 0 else ""
        console.print(f"[{style}]{prefix}{line}[/]")
        sleep(0.012)
    blank()
    sleep(0.08)


def _center_reveal(text: str, style: str, delay: float = 0.03) -> None:
    """Cetak teks karakter per karakter dari tengah."""
    padding = max(0, (console.width - len(text)) // 2) * " "
    console.print(padding, end="", highlight=False)
    typewrite(text, style=style, delay=delay)
    sleep(0.06)


def _name_reveal(text: str = "Nasha Putri Zaqirah.", large: bool = True) -> None:
    """Cetak nama dengan efek typewriter + glow style."""
    style = f"bold italic {ROSE_LIGHT}" if large else f"italic {ROSE_LIGHT}"
    padding = max(0, (console.width - len(text)) // 2) * " "
    console.print(padding, end="", highlight=False)
    typewrite(text, style=style, delay=DELAY_SLOW)
    sleep(0.15)


def _quote(text: str, width: int = 64) -> None:
    """Cetak blok kutipan di dalam panel."""
    import textwrap
    wrapped = textwrap.fill(text, width=width)
    console.print(
        Panel(
            f"[italic {ROSE_LIGHT}]{wrapped}[/]",
            border_style=ROSE_DARK,
            padding=(0, 3),
            expand=False,
        )
    )
    blank()
    pause(0.25)


def _rule_ornament() -> None:
    console.print(Align.center(f"[{TEXT_DIM}]· · · · ·[/]"))
    blank()
    pause(0.2)


# ═══════════════════════════════════════════════════════════
#  Entry point
# ═══════════════════════════════════════════════════════════

def main() -> None:
    try:
        intro_splash()
        print_metadata()
        print_letter()
        print_poem()
        outro()
    except KeyboardInterrupt:
        blank(2)
        console.print(
            Align.center(f"[italic {TEXT_DIM}]— dibiarkan berlalu dengan tenang —[/]")
        )
        blank()


if __name__ == "__main__":
    main()
