from modules.shared.triagem.dao import TriagemDao

SQL_INSERT = 'INSERT INTO pre_triagem(peso, altura, pulso, pressao_arterial, hemoglobina) ' \
             'VALUES(%s, %s, %s, %s, %s) returning id'
SQL_SELECT = 'SELECT * FROM pre_triagem'
SQL_BY_ID = 'SELECT * FROM pre_triagem WHERE id = {}'
SQL_DELETE = 'DELETE FROM pre_triagem WHERE id = {}'
SQL_UPDATE = 'UPDATE pre_triagem SET {} WHERE id = {}'


class PreTriagemDao:
    def __init__(self, database):
        self.database = database
        self.dao_triagem = TriagemDao(database=database)

    def save_pre_triagem(self, pre_triagem):
        cursor = self.database.connect.cursor()
        cursor.execute(SQL_INSERT, pre_triagem.get_values_save())
        id = cursor.fetchone()[0]
        self.database.connect.commit()
        cursor.close()
        pre_triagem.set_id(id)
        return pre_triagem

    def edit_pre_triagem(self, id, pre_triagem):
        cursor = self.database.connect.cursor()
        str = []
        for key in pre_triagem.keys():
            str.append('{} = %s'.format(key))
        cursor.execute(SQL_UPDATE.format(','.join(str), id), list(pre_triagem.values()))
        self.database.connect.commit()
        cursor.close()
        return True

    def get_by_id(self, id):
        pre_triagem = self.get_all_or_by_id(SQL_BY_ID.format(id))
        if pre_triagem:
            return pre_triagem[0]
        return None

    def get_all(self):
        pre_triagem = self.get_all_or_by_id(SQL_SELECT)
        return pre_triagem

    def get_all_or_by_id(self, script):
        triagens = []
        cursor = self.database.connect.cursor()
        cursor.execute(script)
        columns_name = [column[0] for column in cursor.description]
        pre_triagem_cursor = cursor.fetchone()
        while pre_triagem_cursor is not None:
            pre_triagem = dict(zip(columns_name, pre_triagem_cursor))
            pre_triagem_cursor = cursor.fetchone()
            triagem = self.dao_triagem.get_by_id(pre_triagem.get('id'))
            if triagem:
                triagem.pop('pre_triagem_id')
            pre_triagem['triagem'] = triagem
            triagens.append(pre_triagem)
        cursor.close()
        return triagens

    def delete_pre_triagem(self, id):
        cursor = self.database.connect.cursor()
        cursor.execute(SQL_DELETE.format(id))
        self.database.connect.commit()
        return True
