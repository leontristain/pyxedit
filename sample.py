import argparse
from pathlib import Path
import os

from xelib import XEdit


def process_plugin(game_path,
                   plugin_name,
                   npcs_to_keep=None,
                   relink_vanilla=False):
    npcs_to_keep = npcs_to_keep or set()

    files_to_keep = set()
    files_to_delete = set()

    with XEdit(plugins=[plugin_name]).context() as xedit:
        # we will want to iterate over NPCs, so retrieve the npcs list on the
        # plugin
        plugin = xedit.plugin(plugin_name)
        npcs = plugin['Non-Player Character (Actor)']

        # the first pass will be an information gathering pass, during which we
        # will put any records associated with NPCs we want to keep into records
        # to keep, and any records associated with NPCs we want to delete into
        # records to delete
        records_to_keep = set()
        records_to_delete = set()

        # time to get to work, we loop over npcs
        for npc in npcs:
            # choose one of the two sets to add records to, depending on whether
            # the npc is to be kept or deleted
            tracked_records = (records_to_keep if npc.name in npcs_to_keep
                               else records_to_delete)
            tracked_files = (files_to_keep if npc.name in npcs_to_keep
                             else files_to_delete)

            # we can manage handles per npc
            with xedit.manage_handles:
                # loop through npc's head parts and track stuff
                head_parts = list(npc.head_parts)
                for head_part in head_parts:
                    tracked_records.add(head_part.long_path)
                    tracked_files.update(head_part.file_paths)
                    texture_set = head_part.texture_set
                    if texture_set:
                        tracked_records.add(texture_set.long_path)
                        tracked_files.update(texture_set.file_paths)
                    head_parts.extend(head_part.extra_parts)

                # track the worn armor
                worn_armor = npc.worn_armor
                if worn_armor:
                    # set the tracked sets to the ones for deletion if we are
                    # also attempting to relinking bodies to vanilla
                    tracked_records = (records_to_delete if relink_vanilla
                                       else tracked_records)
                    tracked_files = (files_to_delete if relink_vanilla
                                     else tracked_files)

                    tracked_records.append(worn_armor.long_path)
                    for armature in worn_armor.armature:
                        tracked_records.add(armature.long_path)
                        tracked_files.update(armature.file_paths)
                        for texture_set in armature.texture_sets:
                            tracked_records.add(texture_set.long_path)
                            tracked_files.update(texture_set.file_paths)

                # we can now delete the npc if we don't want to keep it
                if npc.name not in npcs_to_keep:
                    npc.delete()

                # if we don't delete the npc, we should at least nullify the
                # worn armor if we are relinking vanilla body
                elif relink_vanilla and worn_armor:
                    npc.worn_armor = None

        # at this point, we should have gathered a list of record long_paths, if
        # any exists in only the to_delete set, we can delete them; make sure to
        # only delete records underneath our plugin
        for long_path in records_to_delete:
            if long_path not in records_to_keep:
                record = xedit[long_path]
                if record.plugin == plugin_name:
                    record.delete()

        # records have been properly deleted, save the plugin
        plugin.save()

    # return the files we can delete
    return files_to_delete.difference(files_to_keep)


def prune_mod_folder(files_to_delete, mod_folder):
    for file_path in files_to_delete:
        file_ = Path(mod_folder, file_path)
        if file_.is_file():
            os.remove(file_)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--game-path', required=True)
    parser.add_argument('--mod-folder', required=True)
    parser.add_argument('--plugin-name', required=True)
    parser.add_argument('--npcs-to-keep', default='')
    parser.add_argument('--relink-vanilla', action='store_true')
    args = parser.parse_args()

    npcs_to_keep = set()
    for item in args.npcs_to_keep.split(','):
        stripped = item.strip()
        if stripped:
            npcs_to_keep.add(stripped)

    files_to_delete = process_plugin(args.game_path,
                                     args.plugin_name,
                                     npcs_to_keep=npcs_to_keep,
                                     relink_vanilla=args.relink_vanilla)
    if files_to_delete:
        prune_mod_folder(files_to_delete, args.mod_folder)
