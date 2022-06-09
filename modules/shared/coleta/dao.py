SQL_INSERT = 'INSERT INTO coleta(data, ficha_doacao_id) VALUES(%s, %s) returning id'
SQL_SELECT = 'SELECT * FROM coleta'
SQL_BY_ID = 'SELECT * FROM coleta WHERE ficha_doacao_id = {}'
SQL_DELETE = 'DELETE FROM coleta WHERE ficha_doacao_id = {}'
SQL_UPDATE = 'UPDATE coleta SET {} WHERE ficha_doacao_id = {}'


class ColetaDao:
    def __init__(self, database):
        self.database = database

    def save_coleta(self, coleta, ficha_doacao_id):
        cursor = self.database.connect.cursor()
        cursor.execute(SQL_INSERT, coleta.get_values_save(ficha_doacao_id))
        id = cursor.fetchone()[0]
        self.database.connect.commit()
        cursor.close()
        coleta.set_id(id)
        return coleta

    def edit_coleta(self, id, coleta):
        cursor = self.database.connect.cursor()
        str = []
        for key in coleta.keys():
            str.append('{} = %s'.format(key))
        cursor.execute(SQL_UPDATE.format(','.join(str), id), list(coleta.values()))
        self.database.connect.commit()
        cursor.close()
        return True

    def get_by_id(self, id):
        coleta = self.get_all_or_by_id(SQL_BY_ID.format(id))
        if coleta:
            return coleta[0]
        return None

    def get_all(self):
        coleta = self.get_all_or_by_id(SQL_SELECT)
        return coleta

    def get_all_or_by_id(self, script):
        coletas = []
        cursor = self.database.connect.cursor()
        cursor.execute(script)
        columns_name = [column[0] for column in cursor.description]
        coleta_cursor = cursor.fetchone()
        while coleta_cursor is not None:
            coleta = dict(zip(columns_name, coleta_cursor))
            coleta_cursor = cursor.fetchone()
            coletas.append(coleta)
        cursor.close()
        return coletas

    def delete_coleta(self, id):
        cursor = self.database.connect.cursor()
        cursor.execute(SQL_DELETE.format(id))
        self.database.connect.commit()
        return True
