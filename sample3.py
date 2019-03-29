import xelib

xedit = xelib.XEdit.quickstart()
erdi = xedit['Skyrim.esm\\NPC_\\Erdi']

for v in erdi.find_text_values():
    print(v)
