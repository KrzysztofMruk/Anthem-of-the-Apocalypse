# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\Krzysztof\\Documents\\GitHub\\AOA\\ui\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\Krzysztof\\Documents\\GitHub\\AOA\\core', 'core/'), ('C:\\Users\\Krzysztof\\Documents\\GitHub\\AOA\\img', 'img/'), ('C:\\Users\\Krzysztof\\Documents\\GitHub\\AOA\\music', 'music/'), ('C:\\Users\\Krzysztof\\Documents\\GitHub\\AOA\\sounds', 'sounds/'), ('C:\\Users\\Krzysztof\\Documents\\GitHub\\AOA\\video', 'video/'), ('C:\\Users\\Krzysztof\\Documents\\GitHub\\AOA\\core\\json', 'json/'), ('C:\\Users\\Krzysztof\\Documents\\GitHub\\AOA\\core\\json\\messages_and_keys.json', '.'), ('C:\\Users\\Krzysztof\\Documents\\GitHub\\AOA\\core\\json\\music_and_sound_volume.json', '.'), ('C:\\Users\\Krzysztof\\Documents\\GitHub\\AOA\\core\\json\\screen_parameters.json', '.'), ('C:\\Users\\Krzysztof\\Documents\\GitHub\\AOA\\core\\json\\time.json', '.'), ('C:\\Users\\Krzysztof\\Documents\\GitHub\\AOA\\core\\json\\win_conditions.json', '.'), ('C:\\Users\\Krzysztof\\Documents\\GitHub\\AOA\\ui', 'ui/')],
    hiddenimports=['zoneinfo', 'sqlite3', 'gtts', 'moviepy', 'moviepy.editor', 'pygame_gui'],
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
    name='Anthem of the Apocalypse',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\Krzysztof\\Documents\\GitHub\\AOA\\icon2.ico'],
)
