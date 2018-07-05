import sqlite3

class database:
    """

    """
    def __init__(self):
        """

        """
        self.conn = sqlite3.connect(":memory:")
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE  kill_tally(name text, kills int)''')
        self.c.execute('''CREATE TABLE match_id(id text, checked bool )''')
        self.c.execute('''CREATE TABLE player(name text, account text, matchid text )''')
        self.conn.commit()

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

    def store_name_match(self, match_id, name):
        """
        take a name and match id and store in table
        :param name:
        :param match_id:
        :return:
        """
        self.c.execute('SELECT name FROM player WHERE (name = ?) AND (matchid = ?)', (name, match_id))
        results = self.c.fetchone()
        if results is None:
            self.c.execute('INSERT INTO player (name, matchid) VALUES (?,?)', (name, match_id))
            self.c.execute('UPDATE match_id SET id = ?, checked =?', (match_id, True))
            self.conn.commit()
            return True

    def return_player_names(self):
        """
        return a list of all players in the table
        :return:
        """
        self.c.execute('select name FROM player')
        return self.c.fetchall()

    def return_unchecked_matches(self):
        """
        Find any matches that have been in stered into the database but have yet to be searched for all the players
        in that match
        :return:
        """
        self.c.execute('SELECT id FROM match_id WHERE checked=False')
        l = self.c.fetchall()
        return list(l)