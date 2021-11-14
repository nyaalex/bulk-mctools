def read_desc(description):
    if type(description) == str:
        return description
    elif 'extra' in description:
        return ''.join([i['text'] for i in description['extra']])
    elif 'text' in description:
        return description['text']
    else:
        return description['translate']


def print_response(res, flags=(True, True, True)):
    try:
        host = res['host']
        ping = str(res['ping'])
        version = res['version']['name']
        description = read_desc(res['description'])
        player_count = str(res['players']['online'])

        if player_count != '0' and 'sample' in res['players']:
            player_list = ';'.join([i['name'] for i in res['players']['sample']])
        else:
            player_list = 'null'

        info = [host, ping, version, description, player_count, player_list]

        return ','.join(info)
    except Exception as e:
        return e, res['host']
