# -*- mode: python ; coding: utf-8 -*-
# for windows app
block_cipher = None


a = Analysis([
            'app.py'
            ],
             pathex=['C:\\Users\\wuy37\\Desktop\\Rango'],
             binaries=[],
             datas=[
             ('static\\css\\*.css', 'static\\css'),
             ('static\\css\\alt\\*', 'static\\css\\alt'),
             ('static\\images\\*', 'static\\images'),
             ('static\\js\\*', 'static\\js'),
             ('static\\js\\pages\\*', 'static\\js\\pages'),
             ('static\\webfonts\\*', 'static\\webfonts'),
             ('static\\plugins\\datatables\\*', 'static\\plugins\\datatables'),
             ('static\\plugins\\datatables-bs4\\*', 'static\\plugins\\datatables-bs4'),
             ('static\\plugins\\datatables-buttons\\*', 'static\\plugins\\datatables-buttons'),
             ('static\\plugins\\datatables-responsive\\*', 'static\\plugins\\datatables-responsive'),
             ('static\\plugins\\daterangepicker\\*', 'static\\plugins\\daterangepicker'),
             ('templates\\*.html', 'templates'),
             ('data.db', '.'),
             ('appicon.png', '.'),
             ('Rango.ico', '.'),
             ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Rango',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Rango',
               icon='C:\\Users\\wuy37\\Desktop\\Rango\\Rango.ico')
