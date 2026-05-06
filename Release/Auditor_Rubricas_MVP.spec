# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = []
binaries = []
hiddenimports = []

# Colección de dependencias complejas
tmp_ret = collect_all('api_intelligence_wrapper')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

tmp_ret = collect_all('fitz')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

tmp_ret = collect_all('pymupdf')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

a = Analysis(
    ['..\\celula-auditor-rubricas\\main.py'],
    pathex=['C:\\Users\\LENOVO\\Desktop\\REPOSITORIOS\\PEDAGOG-IA_Cel-las_de_Automatizacion\\celula-auditor-rubricas'],
    binaries=binaries,
    datas=[
        ('..\\celula-auditor-rubricas\\prompts\\*.md', 'prompts'),
    ] + datas,
    hiddenimports=['adapters', 'adapters.pdf_adapter', 'core', 'core.exporter', 'openpyxl', 'fitz'] + hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Auditor_Rubricas_MVP',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
