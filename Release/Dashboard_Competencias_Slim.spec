# -*- mode: python ; coding: utf-8 -*-
import os

# Configuración de rutas absolutas
project_root = os.path.abspath(r'C:\Users\LENOVO\Desktop\REPOSITORIOS\PEDAGOG-IA_Cel-las_de_Automatizacion')
cell_path = os.path.join(project_root, 'celula-dashboard-competencias')

# Empaquetado explícito de assets
datas = [
    (os.path.join(cell_path, 'web'), 'web'),
    (os.path.join(cell_path, 'data'), 'data')
]

# Lista de exclusiones masiva para "Slim Build"
excluded_modules = [
    'tkinter', 'matplotlib', 'numpy', 'pandas', 'scipy', 
    'unittest', 'pydoc', 'email', 'xml', 'html',
    'distutils', 'setuptools', 'lib2to3', 'IPython', 'PIL'
]

block_cipher = None

a = Analysis(
    [os.path.join(cell_path, 'main.py')],
    pathex=[project_root, cell_path],
    binaries=[],
    datas=datas,
    hiddenimports=[],
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
    name='Dashboard_Competencias_Slim',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True, # Mantenemos consola para ver que el servidor arrancó
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
