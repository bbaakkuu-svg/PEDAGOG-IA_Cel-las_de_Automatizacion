# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_all

# Configuración de rutas absolutas para robustez
project_root = os.path.abspath(r'C:\Users\LENOVO\Desktop\REPOSITORIOS\PEDAGOG-IA_Cel-las_de_Automatizacion')
cell_path = os.path.join(project_root, 'celula-generador-material')

# Recolección automática de dependencias complejas si existieran
datas = []
binaries = []
hiddenimports = [
    'core',
    'core.engine',
    'api_intelligence_wrapper',
    'api_intelligence_wrapper.facade'
]

# Recolectar metadatos de pydantic y rich
tmp_ret = collect_all('rich')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('pydantic')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

block_cipher = None

a = Analysis(
    [os.path.join(cell_path, 'main.py')],
    pathex=[
        project_root,
        cell_path
    ],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Generador_Material_MVP',
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
    icon=None,
)
