import sqlite3
import logging

class database:
    """

    """
    def __init__(self):
        """

        """
        self.conn = sqlite3.connect("database.db")
        self.c = self.conn.cursor()


    def insert_row(self, name):
        """

        :return:
        """
        self.c.execute('SELECT * FROM kill_tally WHERE name = ?', (name,))
        data = self.c.fetchone()
        if data is None:
            self.c.execute("INSERT INTO kill_tally (name, kills) VALUES(?,?)", (name, 1))
            self.conn.commit()
            return True
        else:
            self.c.execute("UPDATE kill_tally SET kills = kills + 1 WHERE name =?", (name,))
            self.conn.commit()
            return True

    def results(self):
        """

        :return:
        """
        self.c.execute("SELECT * FROM kill_tally ORDER BY kills DESC")
        print(list(self.c))

    def store_match_id(self, id):
        """
        Give an string of id for  amtch, sotere id value
        :param id: string
        :return:
        """
        id = str(id)
        self.c.execute('SELECT * FROM match_id WHERE id = ?', (id,))
        result = self.c.fetchone()
        if result is None:
            self.c.execute('INSERT INTO match_id (id) VALUES (?)', (id,))
        self.conn.commit()

    def return_match_ids(self):
        """

        :return:
        """
        self.c.execute('SELECT * FROM  match_id')
        return self.c.fetchall()

    def store_name_match(self, match_id, name, account):
        """
        take a name and match id and store in table
        :param name: name of player
        :param match_id: match id as a string
        :param account: account id of player
        :return:
        """
        self.c.execute('SELECT * FROM player WHERE (name = ?) AND (matchid = ?)', (name, match_id))
        results = self.c.fetchone()
        if results is None:
            self.c.execute('INSERT INTO player (name, matchid, account) VALUES (?,?,?)', (name, match_id, account))
            self.conn.commit()
            logging.log(logging.INFO, 'Sotring a name and macth id in player table: %s and %s', name, match_id)

    def mark_match_checked(self, matchid):
        """
        IOnce all the playes have been entered from a match id, then mark match checked.
        :param matchid:
        :return:
        """
        self.c.execute('SELECT * FROM match_id WHERE (id = ?) AND (checked = ?)', (matchid, True))
        r = self.c.fetchone()
        if not r:
            self.c.execute('UPDATE match_id SET checked =? WHERE id = ?', (True, matchid))
            self.conn.commit()
            logging.log(logging.INFO, 'Updating macth checked field for match id: %s', matchid)

    def return_player_names(self):
        """
        return a list of all players in the table
        :return:
        """
        self.c.execute('select name FROM player')
        return self.c.fetchall()

    def return_unchecked_matches(self):
        """
        Find any matches that have been in stored into the database but have yet to be searched for all the players
        in that match
        :return:
        """
        self.c.execute('SELECT id FROM match_id WHERE checked=False')
        l = self.c.fetchall()
        logging.log(logging.INFO, 'THe following matched have yet to be checked for players: %s', l)
        return list(l)

    def store_name(self, name):
        """
        Store a name of a player
        :param name:
        :return:
        """
        self.c.execute('INSERT INTO player (name) VALUES (?)', (name))
        self.conn.commit()
        logging.info(logging.INFO, 'inserting name: %s', name)

    def store_tel_data(self, result, id):
        """

        :param data:
        :return:
        """
        if not (result.damage_type_category == 'Damage_BlueZone' or result.damage_type_category == 'Damage_Groggy'):
            self.c.execute('SELECT * FROM kill_data WHERE (match_id = ?) AND (killer = ?) AND (victim = ?)', (id, result.killer.name, result.victim.name))
            r = self.c.fetchone()
            if r is None:
                self.c.execute('INSERT INTO kill_data (match_id, killer, victim) VALUES (?,?,?)', (id, result.killer.name, result.victim.name))
                self.conn.commit()
                logging.info(logging.INFO, 'inserting kill data data: %s, %s, %s', id, result.killer.name, result.victim.name)

    def db_init(self):
        """
        Initial build of the data base.
        :return:
        """
        self.c.execute('''CREATE TABLE  kill_tally(name text, kills int)''')
        self.c.execute('''CREATE TABLE match_id(id text, checked bool )''')
        self.c.execute('''CREATE TABLE player(name text, account text, matchid text )''')
        self.c.execute('''CREATE TABLE kill_data (killer text victim text match_id text)''')
        self.conn.commit()