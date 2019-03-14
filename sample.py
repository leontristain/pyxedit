from xelib.xedit import XEdit
from pathlib import Path
from somelib import get_mod_dir
import os

'''
Yaml Configuration:
 - plugin: Bijin_AIO 2018.esp
   xedit:
     - script: npc_selector
       chosen:
         - Irileth
         - Hulda
         - Carlotta Valentia
     - script: delete_path
       paths:
         - Dialog Topic
'''

chosen = ['Irileth', 'Hulda', 'Carlotta Valentia']
relink_vanilla = True

files_to_delete = set()

with XEdit(plugins=['Bijin_AIO 2018.esp']).context() as xedit:
    bijin_aio = xedit.plugin('Bijin_AIO 2018.esp')
    npcs = bijin_aio['Non-Player Character (Actor)']
    records_to_keep = set()
    records_to_delete = set()
    with xedit.manage_handles:
        for npc in npcs:
            tracked = records_to_keep if npc.name in chosen else records_to_delete
            head_parts = npc['Head Parts']
            for head_part in head_parts:
                if head_part:
                    tracked.add(head_part.full_path)
                    texture_set = head_part.texture_set
                    if texture_set:
                        tracked.add(texture_set)

            worn_armor = npc['Worn Armor']
            if worn_armor:
                tracked = records_to_delete if relink_vanilla else tracked
                tracked.append(worn_armor)
                for armature in worn_armor.armature:
                    tracked.append(armature)
                    male_skin_texture = armature.male_skin_texture
                    if male_skin_texture:
                        tracked.append(male_skin_texture)
                    female_skin_texture = armature.female_skin_texture
                    if female_skin_texture:
                        tracked.append(female_skin_texture)

            if npc.name not in chosen:
                npc.delete()
            elif relink_vanilla and worn_armor:
                npc['Worn Armor'] = None

    for record_path in records_to_delete:
        if record_path not in records_to_keep:
            record = bijin_aio.get(record_path)
            files_to_delete.update(record.filenames)
            record.delete()

    bijin_aio.save()

mod_dir = get_mod_dir('Bijin AIO')
for file in files_to_delete:
    file_ = Path(mod_dir, files_to_delete)
    if file_.is_file():
        os.remove(file_)
