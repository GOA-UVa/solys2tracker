# -*- mode: python ; coding: utf-8 -*-

import sys

block_cipher = None

a_pathex = []
a_binaries = []
a_datas = []
runner_file = 'solys2tracker/runner.py'
pyver = 'python3.10'

if sys.platform == 'linux':
    a_pathex = [f'./.venv/lib/{pyver}/site-packages/', f'./.venv/lib64/{pyver}/site-packages/']
    a_binaries = [
        (f'.venv/lib/{pyver}/site-packages/spiceypy/utils/libcspice.so', './spiceypy/utils')
    ]
    a_datas = [
        ('solys2tracker/style.qss', '.')
    ]
elif sys.platform == 'win32' or sys.platform == 'win64':
    a_pathex = ['.\\.venv\\Lib\\site-packages\\']
    a_binaries = [
        ('.venv\\Lib\\site-packages\\spiceypy\\utils\\libcspice.dll', '.\\spiceypy\\utils')
    ]
    a_datas = [
        ('solys2tracker\\style.qss', '.')
    ]
    runner_file = 'solys2tracker\\runner.py'

a = Analysis([runner_file],
            pathex=a_pathex,
            binaries=a_binaries,
            datas=a_datas,
            hiddenimports=[],
            hookspath=[],
            hooksconfig={},
            runtime_hooks=[],
            excludes=[],
            win_no_prefer_redirects=False,
            win_private_assemblies=False,
            cipher=block_cipher,
            noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

if sys.platform == 'win32' or sys.platform == 'win64':
    a.datas += [('.\\solys2tracker\\assets\\icon.png', '.\\solys2tracker\\assets\\icon.png', 'DATA')]
    icon_path = 'solys2tracker\\assets\\icon.ico'
else:
    a.datas += [('./solys2tracker/assets/icon.png', './solys2tracker/assets/icon.png', 'DATA')]
    icon_path = 'solys2tracker/assets/icon.ico'

if sys.platform == 'win32' or sys.platform == 'win64' or sys.platform == 'linux':
    exe = EXE(pyz,
            a.scripts,
            a.binaries,
            a.zipfiles,
            a.datas,  
            [],
            name='Solys2Tracker',
            debug=False,
            bootloader_ignore_signals=False,
            strip=False,
            upx=True,
            upx_exclude=[],
            runtime_tmpdir=None,
            console=False,
            icon=icon_path,
            disable_windowed_traceback=False,
            target_arch=None,
            codesign_identity=None,
            entitlements_file=None )
