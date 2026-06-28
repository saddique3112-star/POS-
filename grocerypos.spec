# grocerypos.spec
# ─────────────────────────────────────────────────────────────────────────────
# PyInstaller spec for GroceryPOS Pro
# Build:  pyinstaller grocerypos.spec
# Output: dist/GroceryPOS_Pro/GroceryPOS_Pro.exe
# ─────────────────────────────────────────────────────────────────────────────

import sys
from pathlib import Path

block_cipher = None

ROOT = Path(SPECPATH)   # directory containing this .spec file

a = Analysis(
    [str(ROOT / 'main.py')],
    pathex     = [str(ROOT)],
    binaries   = [],
    datas      = [
        # include assets folder
        (str(ROOT / 'assets'), 'assets'),
    ],
    hiddenimports = [
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'tkinter.simpledialog',
        'sqlite3',
        'hashlib',
        'json',
        'csv',
        'logging',
        'pathlib',
        'shutil',
        'datetime',
        # optional deps (fail gracefully if absent)
        'openpyxl',
        'reportlab',
        'reportlab.lib',
        'reportlab.lib.pagesizes',
        'reportlab.lib.styles',
        'reportlab.lib.units',
        'reportlab.lib.colors',
        'reportlab.platypus',
        'barcode',
        'barcode.writer',
        'PIL',
        'PIL.Image',
    ],
    hookspath   = [],
    hooksconfig = {},
    runtime_hooks= [],
    excludes    = ['matplotlib', 'numpy', 'scipy', 'pandas'],
    win_no_prefer_redirects = False,
    win_private_assemblies  = False,
    cipher      = block_cipher,
    noarchive   = False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries = True,
    name             = 'GroceryPOS_Pro',
    debug            = False,
    bootloader_ignore_signals = False,
    strip            = False,
    upx              = True,
    console          = False,          # no console window
    disable_windowed_traceback = False,
    argv_emulation   = False,
    target_arch      = None,
    codesign_identity= None,
    entitlements_file= None,
    # icon           = str(ROOT / 'assets' / 'icon.ico'),  # uncomment if icon exists
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip    = False,
    upx      = True,
    upx_exclude = [],
    name     = 'GroceryPOS_Pro',
)
