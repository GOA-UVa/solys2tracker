# -*- mode: python ; coding: utf-8 -*-

import sys

block_cipher = None

a_pathex = []
a_binaries = []
a_datas = []

if sys.platform == 'linux':
    a_pathex = ['./.venv/lib/python3.8/site-packages/', './.venv/lib64/python3.8/site-packages/']
    a_binaries = [
        ('.venv/lib/python3.8/site-packages/spiceypy/utils/libcspice.so', './spiceypy/utils')
    ]
    a_datas = [
        ('solys2tracker/style.qss', '.')#,
        #('./solys2tracker/assets/icon.png', './solys2tracker/assets')
    ]

a = Analysis(['solys2tracker/runner.py'],
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

#a.datas += [('./assets/icon.png', './assets/icon.png', 'DATA')]

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
            icon=None,#'solys2tracker/assets/icon.ico',
            disable_windowed_traceback=False,
            target_arch=None,
            codesign_identity=None,
            entitlements_file=None )
