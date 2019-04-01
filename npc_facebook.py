from xedit import XEdit
import traceback

target_mod = 'The Ordinary Women.esp'
facebook_mod = 'NpcFacebook.esp'


def main():
    with XEdit(plugins=[target_mod, facebook_mod]).session() as xedit:
        npcs = xedit[f'{target_mod}\\NPC_']
        formlist = xedit['NpcFacebook.esp\\FLST\\NpcFacebookNpcs\\LNAM']

        # clear the formlist array
        while formlist:
            formlist.remove(formlist[0])
        print(f'cleared the formlist in {facebook_mod}')

        # iterate over npcs touched by mod and add to formlist
        for npc in npcs.children:
            master_record = npc.master
            print(f'adding record {master_record} of '
                  f'{master_record.plugin.name} to formlist in {facebook_mod}')
            formlist.add(master_record)

        # save the facebook esp
        print(f'saving {facebook_mod}')
        xedit[facebook_mod].save()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(traceback.print_exc())
        print(str(e))
    finally:
        prompt = input('type something to exit')
