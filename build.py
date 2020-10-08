from cx_Freeze import setup, Executable

options = {
    "build_exe": {
        "optimize": 2,
        "packages": ["pyglet"],
        "excludes": ["tkinter"],
        "include_files": ["assets"],
    },
    "bdist_msi": {
        "add_to_path": False,
        "all_users": True,
    },
    "bdist_mac": {
        "bundle_name": "FatGuys",
    },
    "bdist_dmg": {
        "volume_label": "FatGuys",
        "applications_shortcut": True,
    },
}

setup(name="fatguys",
      version="1.0",
      description="Lazy Devs' game jam entry",
      options=options,
      executables=[Executable("fatguys.py",
                              targetName="FatGuys",
                              icon="assets/icon.ico",
                              copyright="Visual & kb1000 2020")])
