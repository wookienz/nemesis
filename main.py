from pubg_python import PUBG, Shard
import config
import database

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
    match = api.matches().get(id)
    return match

def store_names_from_match(matchobj):
    """
    given a match object parse the match id and people who playes in that match. Store both values.
    :param matchobj:
    :return:
    """
    for id in match.rosters:
        d.store_name_match(id.id, id.participants[0].name)

test = api.samples().get()

games_played = get_games_from_player_name("NZWookie")
store_match_id(games_played)
ids = d.return_match_ids()
for a in ids:
    match = lookup_match_id(a[0])
    store_names_from_match(match)
names = d.return_player_names()
for a in names:
    games_played = get_games_from_player_name(a[0])
    store_match_id(games_played)
print(d.return_player_names())
#killtally(players)
