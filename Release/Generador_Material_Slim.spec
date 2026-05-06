# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_all

# Configuración de rutas absolutas
project_root = os.path.abspath(r'C:\Users\LENOVO\Desktop\REPOSITORIOS\PEDAGOG-IA_Cel-las_de_Automatizacion')
cell_path = os.path.join(project_root, 'celula-generador-material')

# Recolección SELECTIVA de dependencias
datas = []
binaries = []
hiddenimports = [
    'core',
    'core.engine',
    'api_intelligence_wrapper',
    'api_intelligence_wrapper.facade'
]

# Recolectar solo lo necesario (Rich y Pydantic)
# ELIMINAMOS PANDAS Y NUMPY de aquí
for lib in ['rich', 'pydantic']:
    tmp_ret = collect_all(lib)
    datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

# Lista de exclusiones para reducir peso drásticamente
excluded_modules = [
    'tkinter', 'matplotlib', 'numpy', 'pandas', 'scipy', 
    'unittest', 'pydoc',
    'distutils', 'setuptools', 'lib2to3'
]

block_cipher = None

a = Analysis(
    [os.path.join(cell_path, 'main.py')],
    pathex=[cell_path, os.path.join(project_root, 'api_intelligence_wrapper')],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excluded_modules, # Aplicamos exclusiones
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
    name='Generador_Material_Slim', # Cambiamos nombre para diferenciar
    debug=False,
    bootloader_ignore_signals=False,
    strip=True, # Strip symbols
    upx=True,   # UPX compression
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
