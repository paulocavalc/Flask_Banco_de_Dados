SQL_INSERT = 'INSERT INTO triagem(entrevista, pre_triagem_id) VALUES(%s, %s) returning id'
SQL_SELECT = 'SELECT * FROM triagem'
SQL_BY_ID = 'SELECT * FROM triagem WHERE pre_triagem_id = {}'
SQL_DELETE = 'DELETE FROM triagem WHERE pre_triagem_id = {}'
SQL_UPDATE = 'UPDATE triagem SET {} WHERE pre_triagem_id = {}'


class TriagemDao:
    def __init__(self, database):
        self.database = database

    def save_triagem(self, triagem, pre_triagem_id):
        cursor = self.database.connect.cursor()
        cursor.execute(SQL_INSERT, triagem.get_values_save(pre_triagem_id))
        id = cursor.fetchone()[0]
        self.database.connect.commit()
        cursor.close()
        triagem.set_id(id)
        return triagem

    def edit_triagem(self, id, triagem):
        cursor = self.database.connect.cursor()
        str = []
        for key in triagem.keys():
            str.append('{} = %s'.format(key))
        cursor.execute(SQL_UPDATE.format(','.join(str), id), list(triagem.values()))
        self.database.connect.commit()
        cursor.close()
        return True

    def get_by_id(self, id):
        triagem = self.get_all_or_by_id(SQL_BY_ID.format(id))
        if triagem:
            return triagem[0]
        return None

    def get_all(self):
        triagem = self.get_all_or_by_id(SQL_SELECT)
        return triagem

    def get_all_or_by_id(self, script):
        triagens = []
        cursor = self.database.connect.cursor()
        cursor.execute(script)
        columns_name = [column[0] for column in cursor.description]
        triagem_cursor = cursor.fetchone()
        while triagem_cursor is not None:
            triagem = dict(zip(columns_name, triagem_cursor))
            triagem_cursor = cursor.fetchone()
            triagens.append(triagem)
        cursor.close()
        return triagens

    def delete_triagem(self, id):
        cursor = self.database.connect.cursor()
        cursor.execute(SQL_DELETE.format(id))
        self.database.connect.commit()
        return True
