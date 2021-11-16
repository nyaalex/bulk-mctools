import re


def read_desc(description):
    output = ''
    if type(description) == str:
        return re.sub('§.', '', description)

    if 'extra' in description:
        for i in description['extra']:
            output += read_desc(i)

    if 'text' in description:
        output += description['text']

    if 'translate' in description:
        output += description['translate']

    return re.sub('§.', '', output)


def print_response(res):
    try:
        host = res['host']
        ping = str(res['ping'])
        version = res['version']['name']
        description = read_desc(res['description'])

        if 'players' in res:
            player_count = str(res['players']['online'])
        else:
            player_count = '0'

        if player_count != '0' and 'sample' in res['players']:
            player_list = ';'.join([i['name'] for i in res['players']['sample']])
        else:
            player_list = 'null'

        if 'forgeData' in res:
            mods = str(len(res['forgeData']['mods']))
        elif 'modinfo' in res:
            mods = str(len(res['modinfo']['modList']))
        else:
            mods = '0'

        info = [host, ping, version, mods, repr(description), player_count, player_list]

        return ','.join(info) + '\n'
    except Exception as e:
        raise Exception(str(e) + ',' + res['host'])
