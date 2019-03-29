import xelib
from pathlib import Path

xedit = xelib.XEdit.quickstart(plugins=['The Ordinary Women.esp'])
erdi = xedit['The Ordinary Women.esp\\NPC_\\DLC1Valerica']

for i, obj in enumerate(erdi.find_related_objects(
        signatures=['ARMA', 'ARMO', 'HDPT', 'TXST'],
        recurse=True,
        same_plugin=True)):
    print(i, obj)
    for text_value in obj.find_text_values():
        if text_value and Path(text_value).suffix in ('.nif', '.tri', '.dds'):
            print(f'    {text_value}')
