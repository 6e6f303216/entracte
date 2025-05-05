import os
from glob import glob
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

project_root = os.getcwd()

def collect_data_dir(src_dir, dest_dir, exclude_files=None):
    exclude_files = exclude_files or []
    data = []
    for root, _, files in os.walk(src_dir):
        for file in files:
            full_path = os.path.join(root, file)
            if os.path.relpath(full_path, src_dir) in exclude_files:
                continue
            relative_path = os.path.relpath(full_path, src_dir)
            dest_path = os.path.join(dest_dir, relative_path)
            data.append((full_path, dest_path))
    return data

assets_data = collect_data_dir(
    'assets',
    'assets',
    exclude_files=[
        'fonts/JetBrainsMonoNerdFont-Medium.ttf'
    ]
)

other_data = [
    ('lockscreen.ps1', '.'),
    ('lockscreen.sh', '.'),
]

datas = assets_data + other_data

a = Analysis(
    ['main.py'],
    pathex=[project_root],
    datas=datas,
    hiddenimports=collect_submodules('PyQt6'),
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
    name='entracte',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon='assets/app.ico',
)
