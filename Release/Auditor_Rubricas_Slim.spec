# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_all

# Configuración de rutas absolutas
project_root = os.path.abspath(r'C:\Users\LENOVO\Desktop\REPOSITORIOS\PEDAGOG-IA_Cel-las_de_Automatizacion')
cell_path = os.path.join(project_root, 'celula-auditor-rubricas')

# Recolección SELECTIVA de dependencias
datas = []
binaries = []
hiddenimports = [
    'adapters',
    'adapters.pdf_adapter',
    'core',
    'core.exporter',
    'openpyxl'
]

# Recolectar solo lo necesario (Rich, Openpyxl, PyMuPDF)
for lib in ['rich', 'openpyxl', 'fitz']:
    tmp_ret = collect_all(lib)
    datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

# Lista de exclusiones masiva (SIN PANDAS NI NUMPY)
excluded_modules = [
    'tkinter', 'matplotlib', 'numpy', 'pandas', 'scipy', 
    'unittest', 'pydoc', 'email', 'http', 'xml', 'html',
    'distutils', 'setuptools', 'lib2to3', 'IPython', 'PIL'
]

block_cipher = None

a = Analysis(
    [os.path.join(cell_path, 'main.py')],
    pathex=[project_root, cell_path],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excluded_modules,
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
    name='Auditor_Rubricas_Slim',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
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
