# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Air-Piano
This file controls how the executable is built
"""

import sys
from pathlib import Path

# Get the directory where this spec file is located
spec_root = Path(__file__).parent

a = Analysis(
    ['air_piano_main.py'],
    pathex=[str(spec_root)],
    binaries=[],
    datas=[
        ('requirements.txt', '.'),
    ],
    hiddenimports=[
        'cv2',
        'mediapipe',
        'pygame',
        'pygame.midi',
        'pygame.mixer',
        'numpy',
        'threading',
        'time',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# Collect all MediaPipe files
from PyInstaller.utils.hooks import collect_all
mp_datas, mp_binaries, mp_hiddenimports = collect_all('mediapipe')
a.datas += mp_datas
a.binaries += mp_binaries
a.hiddenimports += mp_hiddenimports

# Collect all OpenCV files
cv2_datas, cv2_binaries, cv2_hiddenimports = collect_all('cv2')
a.datas += cv2_datas
a.binaries += cv2_binaries
a.hiddenimports += cv2_hiddenimports

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Air-Piano',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True if you want to see console output for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='piano.ico' if Path('piano.ico').exists() else None,
)
