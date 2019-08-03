# -*- mode: python -*-

# Set up some convenience variables to shorten up the path names
images_dir = "images\\"

# Files that need to be bundled that are in images_dir
imagesList   = ["icon.png", "pic.jpg", "backtiming_calculator.png", "coordinates_extractor.png", "empty.png", "village_planner.png", "village_finder.png", "logo_text.png", "farm_thief.png"]

# Create a list of all the necessary resources in the format that pyInstaller wants it in
d = []

# Add images
for image in imagesList:
    d.append((images_dir + image, images_dir + image, "DATA"))

# Add icon
d.append(("exe_icon.ico", "exe_icon.ico", "DATA"))

block_cipher = None

from pathlib import Path

a = Analysis(['main.py'],
             pathex=[Path().absolute()],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas + d,
          name="ZeZe's TWTools 0.7",
          debug=False,
          strip=False,
          console=False,
          upx=False,
          icon="exe_icon.ico")