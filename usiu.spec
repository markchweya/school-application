# usiu.spec
# Build with:  pyinstaller usiu.spec

import os
from PyInstaller.utils.hooks import collect_submodules
from kivy_deps import sdl2, glew

# Attempt to import angle (Windows only)
try:
    from kivy_deps import angle
    angle_bins = angle.dep_bins
except Exception:
    angle_bins = []

# Collect all kivymd submodules to prevent import errors
hiddenimports = collect_submodules('kivymd')

# Handle icon paths safely
icon_path = 'assets/usiu.ico'
icns_path = 'assets/usiu.icns'

icon_arg = icon_path if os.path.isfile(icon_path) else None
icns_arg = icns_path if os.path.isfile(icns_path) else None

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),  # Include your assets folder
    ],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

# Include Kivy native binaries (SDL2, GLEW, ANGLE)
for dep in (sdl2.dep_bins + glew.dep_bins + angle_bins):
    a.binaries.append((os.path.basename(dep), dep, 'BINARY'))

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# ===== Build EXE (Windows) =====
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='USIU Africa',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,              # No console window
    icon=icon_arg,              # Optional Windows icon
)

# ===== Collect all files into dist folder =====
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='USIU Africa',
)

# ===== macOS app bundle =====
app = BUNDLE(
    coll,
    name='USIU Africa.app',
    icon=icns_arg,              # Optional macOS icon
    bundle_identifier='ke.usiu.africa.login',
)
