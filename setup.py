"""
Setup script for building Hora Widget macOS application
"""
from setuptools import setup

APP = ['hora_gui.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'hora_icon.icns',
    'plist': {
        'CFBundleName': 'Hora Widget',
        'CFBundleDisplayName': 'Hora Widget',
        'CFBundleIdentifier': 'com.horawidget.app',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': True,
        'LSUIElement': True,  # This makes it a menu bar only app (no dock icon by default)
    },
    'packages': ['rumps', 'requests'],
}

setup(
    name='Hora Widget',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
