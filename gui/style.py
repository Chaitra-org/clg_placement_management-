"""
GUI Styles and Theme Configuration
Provides color palettes, fonts, and ttk style configurations for the application.
"""

from tkinter import ttk

BG_DARK = "#0F172A"
HEADER_BG = "#1E3A8A"
HEADER_FG = "#FFFFFF"
PAGE_BG = "#F8FAFC"
CARD_BG = "#FFFFFF"
BORDER_COLOR = "#E2E8F0"

TEXT_PRIMARY = "#0F172A"
TEXT_MUTED = "#64748B"
TEXT_LIGHT = "#94A3B8"

ACCENT_BLUE = "#2563EB"
ACCENT_GREEN = "#059669"
ACCENT_AMBER = "#D97706"
ACCENT_RED = "#DC2626"
ACCENT_PURPLE = "#7C3AED"

FONT_FAMILY = "Segoe UI"
FONT_TITLE = (FONT_FAMILY, 16, "bold")
FONT_SUBTITLE = (FONT_FAMILY, 10)
FONT_HEADING = (FONT_FAMILY, 12, "bold")
FONT_SUBHEADING = (FONT_FAMILY, 10, "bold")
FONT_BODY = (FONT_FAMILY, 9)
FONT_BODY_BOLD = (FONT_FAMILY, 9, "bold")
FONT_MONO = ("Consolas", 9)


def apply_theme(root):
    """Apply modern ttk styles across widgets."""
    style = ttk.Style(root)
    
    available_themes = style.theme_names()
    if "clam" in available_themes:
        style.theme_use("clam")

    style.configure(
        "TNotebook",
        background=PAGE_BG,
        borderwidth=0
    )
    style.configure(
        "TNotebook.Tab",
        font=(FONT_FAMILY, 10, "bold"),
        padding=[16, 8],
        background="#E2E8F0",
        foreground=TEXT_MUTED,
        borderwidth=0
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", HEADER_BG), ("active", "#CBD5E1")],
        foreground=[("selected", "#FFFFFF"), ("active", TEXT_PRIMARY)]
    )

    style.configure(
        "Treeview",
        font=FONT_BODY,
        rowheight=26,
        background="#FFFFFF",
        fieldbackground="#FFFFFF",
        foreground=TEXT_PRIMARY,
        borderwidth=1,
        relief="solid"
    )
    style.configure(
        "Treeview.Heading",
        font=(FONT_FAMILY, 9, "bold"),
        background="#F1F5F9",
        foreground=TEXT_PRIMARY,
        relief="flat",
        padding=[6, 6]
    )
    style.map(
        "Treeview.Heading",
        background=[("active", "#E2E8F0")]
    )
    style.map(
        "Treeview",
        background=[("selected", "#DBEAFE")],
        foreground=[("selected", "#1E3A8A")]
    )

    style.configure(
        "Primary.TButton",
        font=FONT_BODY_BOLD,
        background=ACCENT_BLUE,
        foreground="#FFFFFF",
        padding=[10, 6],
        borderwidth=0
    )
    style.map(
        "Primary.TButton",
        background=[("active", "#1D4ED8"), ("disabled", "#93C5FD")]
    )

    style.configure(
        "Success.TButton",
        font=FONT_BODY_BOLD,
        background=ACCENT_GREEN,
        foreground="#FFFFFF",
        padding=[10, 6],
        borderwidth=0
    )
    style.map(
        "Success.TButton",
        background=[("active", "#047857"), ("disabled", "#A7F3D0")]
    )

    style.configure(
        "Danger.TButton",
        font=FONT_BODY_BOLD,
        background=ACCENT_RED,
        foreground="#FFFFFF",
        padding=[10, 6],
        borderwidth=0
    )
    style.map(
        "Danger.TButton",
        background=[("active", "#B91C1C"), ("disabled", "#FCA5A5")]
    )

    style.configure("Card.TFrame", background=CARD_BG, relief="flat")
    style.configure("Page.TFrame", background=PAGE_BG)
    style.configure("Header.TFrame", background=HEADER_BG)

    return style
