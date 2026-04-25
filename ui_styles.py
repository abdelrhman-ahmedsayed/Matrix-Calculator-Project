"""
QSS Stylesheets for the Matrix Calculator
Premium dark theme with cyan/teal accents and modern aesthetics.
"""

# ─── Color Palette ──────────────────────────────────────────────
BG_DARK = "#0d1117"
BG_PANEL = "#161b22"
BG_ELEVATED = "#1c2333"
BG_INPUT = "#0d1117"
BORDER = "#30363d"
BORDER_FOCUS = "#00d4ff"
ACCENT = "#00d4ff"
ACCENT_HOVER = "#33ddff"
ACCENT_SECONDARY = "#7c3aed"
ACCENT_SEC_HOVER = "#9055ff"
TEXT_PRIMARY = "#e6edf3"
TEXT_SECONDARY = "#8b949e"
TEXT_DIM = "#484f58"
SUCCESS = "#3fb950"
ERROR = "#f85149"
WARNING = "#d29922"

MAIN_STYLESHEET = f"""

/* ─── Global ─────────────────────────────────────────────── */
QMainWindow {{
    background-color: {BG_DARK};
}}

QWidget {{
    color: {TEXT_PRIMARY};
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    font-size: 13px;
}}

/* ─── Custom Title Bar ───────────────────────────────────── */
#titleBar {{
    background-color: {BG_PANEL};
    border-bottom: 1px solid {BORDER};
    min-height: 38px;
    max-height: 38px;
}}

#titleLabel {{
    color: {TEXT_PRIMARY};
    font-size: 13px;
    font-weight: 600;
    padding-left: 12px;
}}

#titleIcon {{
    padding-left: 10px;
}}

/* Window control buttons */
#btnMinimize, #btnMaximize, #btnClose {{
    background: transparent;
    border: none;
    border-radius: 0px;
    min-width: 46px;
    max-width: 46px;
    min-height: 38px;
    max-height: 38px;
    font-size: 14px;
    color: {TEXT_SECONDARY};
}}

#btnMinimize:hover, #btnMaximize:hover {{
    background-color: rgba(255, 255, 255, 0.08);
    color: {TEXT_PRIMARY};
}}

#btnClose:hover {{
    background-color: #c42b1c;
    color: white;
}}

/* ─── Panels ─────────────────────────────────────────────── */
#matrixPanel {{
    background-color: {BG_PANEL};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 16px;
}}

#resultPanel {{
    background-color: {BG_PANEL};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 16px;
}}

#operationPanel {{
    background-color: {BG_PANEL};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 12px;
}}

#historyPanel {{
    background-color: {BG_PANEL};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 12px;
}}

/* ─── Panel Headers ──────────────────────────────────────── */
#panelHeader {{
    color: {TEXT_PRIMARY};
    font-size: 15px;
    font-weight: 700;
    padding-bottom: 4px;
}}

#panelSubHeader {{
    color: {TEXT_SECONDARY};
    font-size: 11px;
    font-weight: 400;
}}

/* ─── Matrix Table ───────────────────────────────────────── */
QTableWidget {{
    background-color: {BG_DARK};
    border: 1px solid {BORDER};
    border-radius: 8px;
    gridline-color: {BORDER};
    selection-background-color: rgba(0, 212, 255, 0.15);
    font-family: 'Cascadia Mono', 'Consolas', 'Courier New', monospace;
    font-size: 14px;
}}

QTableWidget::item {{
    padding: 4px 8px;
    border: none;
    color: {TEXT_PRIMARY};
}}

QTableWidget::item:selected {{
    background-color: rgba(0, 212, 255, 0.12);
    color: {ACCENT};
}}

QTableWidget::item:focus {{
    background-color: rgba(0, 212, 255, 0.08);
    outline: none;
}}

QHeaderView {{
    background-color: {BG_ELEVATED};
    font-family: 'Segoe UI', sans-serif;
    font-size: 11px;
    font-weight: 600;
}}

QHeaderView::section {{
    background-color: {BG_ELEVATED};
    color: {TEXT_SECONDARY};
    border: none;
    border-bottom: 1px solid {BORDER};
    border-right: 1px solid {BORDER};
    padding: 6px 8px;
}}

QTableCornerButton::section {{
    background-color: {BG_ELEVATED};
    border: none;
    border-bottom: 1px solid {BORDER};
    border-right: 1px solid {BORDER};
}}

/* ─── Spin Boxes ─────────────────────────────────────────── */
QSpinBox {{
    background-color: {BG_INPUT};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 4px 8px;
    color: {TEXT_PRIMARY};
    font-size: 13px;
    min-width: 50px;
    min-height: 28px;
}}

QSpinBox:focus {{
    border-color: {ACCENT};
}}

QSpinBox::up-button, QSpinBox::down-button {{
    background-color: {BG_ELEVATED};
    border: none;
    width: 20px;
}}

QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
    background-color: rgba(0, 212, 255, 0.15);
}}

QSpinBox::up-arrow {{
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-bottom: 5px solid {TEXT_SECONDARY};
    width: 0;
    height: 0;
}}

QSpinBox::down-arrow {{
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid {TEXT_SECONDARY};
    width: 0;
    height: 0;
}}

/* ─── Operation Buttons ──────────────────────────────────── */
QPushButton {{
    background-color: {BG_ELEVATED};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 8px 16px;
    color: {TEXT_PRIMARY};
    font-size: 13px;
    font-weight: 600;
    min-height: 36px;
}}

QPushButton:hover {{
    background-color: rgba(0, 212, 255, 0.12);
    border-color: {ACCENT};
    color: {ACCENT};
}}

QPushButton:pressed {{
    background-color: rgba(0, 212, 255, 0.20);
}}

/* Accent button style */
#accentButton {{
    background-color: rgba(0, 212, 255, 0.15);
    border: 1px solid {ACCENT};
    color: {ACCENT};
}}

#accentButton:hover {{
    background-color: rgba(0, 212, 255, 0.25);
}}

/* Secondary button style */
#secondaryButton {{
    background-color: rgba(124, 58, 237, 0.15);
    border: 1px solid {ACCENT_SECONDARY};
    color: {ACCENT_SECONDARY};
}}

#secondaryButton:hover {{
    background-color: rgba(124, 58, 237, 0.25);
    border-color: {ACCENT_SEC_HOVER};
    color: {ACCENT_SEC_HOVER};
}}

/* Clear / danger button */
#dangerButton {{
    background-color: rgba(248, 81, 73, 0.10);
    border: 1px solid rgba(248, 81, 73, 0.4);
    color: {ERROR};
}}

#dangerButton:hover {{
    background-color: rgba(248, 81, 73, 0.20);
    border-color: {ERROR};
}}

/* ─── Labels ─────────────────────────────────────────────── */
#dimLabel {{
    color: {TEXT_SECONDARY};
    font-size: 12px;
}}

#resultScalar {{
    color: {ACCENT};
    font-family: 'Cascadia Mono', 'Consolas', monospace;
    font-size: 22px;
    font-weight: 700;
}}

#errorLabel {{
    color: {ERROR};
    font-size: 12px;
    font-weight: 600;
    padding: 8px;
}}

#successLabel {{
    color: {SUCCESS};
    font-size: 12px;
    font-weight: 600;
    padding: 8px;
}}

/* ─── Scroll Bars ────────────────────────────────────────── */
QScrollBar:vertical {{
    background-color: {BG_DARK};
    width: 10px;
    border: none;
    border-radius: 5px;
}}

QScrollBar::handle:vertical {{
    background-color: {BORDER};
    border-radius: 5px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {TEXT_DIM};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
    border: none;
}}

QScrollBar:horizontal {{
    background-color: {BG_DARK};
    height: 10px;
    border: none;
    border-radius: 5px;
}}

QScrollBar::handle:horizontal {{
    background-color: {BORDER};
    border-radius: 5px;
    min-width: 30px;
}}

QScrollBar::handle:horizontal:hover {{
    background-color: {TEXT_DIM};
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0;
    border: none;
}}

/* ─── Status Bar ─────────────────────────────────────────── */
QStatusBar {{
    background-color: {BG_PANEL};
    border-top: 1px solid {BORDER};
    color: {TEXT_SECONDARY};
    font-size: 11px;
    padding: 2px 8px;
}}

/* ─── Tooltips ───────────────────────────────────────────── */
QToolTip {{
    background-color: {BG_ELEVATED};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 12px;
}}

/* ─── Separator Lines ────────────────────────────────────── */
#separator {{
    background-color: {BORDER};
    min-height: 1px;
    max-height: 1px;
}}

/* ─── History List ───────────────────────────────────────── */
QListWidget {{
    background-color: {BG_DARK};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 4px;
    font-family: 'Cascadia Mono', 'Consolas', monospace;
    font-size: 11px;
    color: {TEXT_SECONDARY};
}}

QListWidget::item {{
    padding: 6px 8px;
    border-radius: 4px;
    margin: 1px 0;
}}

QListWidget::item:hover {{
    background-color: rgba(0, 212, 255, 0.08);
}}

QListWidget::item:selected {{
    background-color: rgba(0, 212, 255, 0.12);
    color: {ACCENT};
}}

/* ─── Dialog Inputs ──────────────────────────────────────── */
QLineEdit {{
    background-color: {BG_INPUT};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 6px 10px;
    color: {TEXT_PRIMARY};
    font-size: 13px;
    min-height: 28px;
}}

QLineEdit:focus {{
    border-color: {ACCENT};
}}

QInputDialog {{
    background-color: {BG_PANEL};
}}

/* ─── Group labels ───────────────────────────────────────── */
#groupLabel {{
    color: {TEXT_DIM};
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    padding: 4px 0px;
}}
"""
