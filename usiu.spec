# usiu.spec
# Build with: pyinstaller usiu.spec

from PyInstaller.utils.hooks import collect_submodules
from kivy_deps import sdl2, glew
try:
    # angle is Windows-only
    from kivy_deps import angle
    angle_bins = angle.dep_bins
except Exception:
    angle_bins = []

hidden = []
# KivyMD can lazy load many submodules; include them all to avoid missing imports
hidden += collect_submodules('kivymd')
# (Optional) if you import other dynamic modules, add them here:
# hidden += collect_submodules('your_pkg')

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),  # bundle your assets folder
    ],
    hiddenimports=hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False
)

# Add Kivy native deps (DLLs / dylibs)
for p in (sdl2.dep_bins + glew.dep_bins + angle_bins):
    a.binaries.append((p.split('/')[-1], p, 'BINARY'))

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

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
    console=False,            # no console window
    icon='assets/usiu.ico'    # on macOS this is ignored; see BUNDLE below
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='USIU Africa'
)

app = BUNDLE(
    coll,
    name='USIU Africa.app',
    icon='assets/usiu.icns',  # macOS app icon
    bundle_identifier='ke.usiu.africa.login',
)
