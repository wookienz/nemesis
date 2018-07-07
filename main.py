from pubg_python import PUBG, Shard
import config
import database
import json
import logging


logging.basicConfig(filename='nemesis.log', level=logging.DEBUG)
api = PUBG(config.api_key, Shard.PC_AS)
d = database.database()


def killtally(players):
    """

    :param players:
    :return:
    """
    l = []
    for a in players[0].matches:
        l.append(a.id)
    for match in l:
        get_match = api.matches().get(match)
        match_asset = get_match.assets[0]
        match_tel = api.telemetry(match_asset.url)
        player_kill_events = match_tel.events_from_type('LogPlayerKill')
        print('======================')
        print('Match ID:' + match)
        for b in player_kill_events:
            if not b.killer.name == '':  # ie blue zone killed them
                d.insert_row(b.killer.name)
        d.results()
        print('======================')


def get_games_from_player_name(name):
    """
    lookup all games played by the name player. return the player object.
    :param name:
    :return:
    """
    players = api.players().filter(player_names=['NZWookie'])
    logging.log(logging.INFO, 'Looking up player %s, for games they have played: %s', name, players)
    return players


def store_match_id(players):
    """
    from an object containing the macthes played by fileterd player, store all macth ids played
    :param players:
    :return:
    """
    for match in players[0].matches:
        d.store_match_id(match)


def lookup_match_id(id):
    """

    :param id:
    :return:
    """
    try:
        match = api.matches().get(id)
        return match
    except Exception as e:
        return False


def store_names_from_match(matchobj):
    """
    given a match object parse the match id and people who playes in that match. Store both values.
    :param matchobj:
    :return:
    """
    for id in match.rosters:
        d.store_match_id(id.id)
        d.store_name_match(id.id, id.participants[0].name, id.participants[0].player_id)
        d.mark_match_checked(id.id)


def load_json_from_file(path):
    """
    load match ids from a json file
    :param path:
    :return:
    """
    with open('samples.txt', 'r') as fh:
        j = json.load(fh)
        return j

def get_telemetry_data(matchid):
    """

    :param matchid:
    :return:
    """
    get_match = api.matches().get(matchid)
    logging.log(logging.INFO, 'getting tel data for match %s', matchid)
    match_asset = get_match.assets[0]
    match_tel = api.telemetry(match_asset.url)
    return match_tel

def store_tel_data(data, id):
    """
    Given a telemetry object store relevant data
    :param data:
    :return:
    """
    l = data.events_from_type('LogPlayerKill')
    for events in l:
        logging.log(logging.INFO, 'storing player kill data')
        d.store_tel_data(events, id)



test = api.samples().get()

for id in test.matches:
        tel = get_telemetry_data(id.id)
        store_tel_data(tel, id.id)


"""
m = load_json_from_file('')
for a in m['data']['relationships']['matches']['data']:
    d.store_match_id(a['id'])


games_played = get_games_from_player_name("NZWookie")
store_match_id(games_played)


ids = d.return_match_ids()
for a in ids:
    match = lookup_match_id(a[0])
    if match:
        store_names_from_match(match)


names = d.return_player_names()
for a in names:
    games_played = get_games_from_player_name(a[0])
    store_match_id(games_played)
print(d.return_player_names())
"""