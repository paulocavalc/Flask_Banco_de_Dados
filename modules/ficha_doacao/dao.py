from modules.shared.coleta.dao import ColetaDao

SQL_INSERT = 'INSERT INTO ficha_doacao(nome, idade, sexo, escolaridade, estado_civil, data_de_nascimento, ' \
             'identidade, tipo_sanguineo) VALUES(%s, %s, %s, %s, %s, %s, %s, %s) returning id'
SQL_SELECT = 'SELECT * FROM ficha_doacao'
SQL_BY_ID = 'SELECT * FROM ficha_doacao WHERE id = {}'
SQL_DELETE = 'DELETE FROM ficha_doacao WHERE id = {}'
SQL_UPDATE = 'UPDATE ficha_doacao SET {} WHERE id = {}'


class FichaDoacaoDao:
    def __init__(self, database):
        self.database = database
        self.dao_coleta = ColetaDao(database=database)

    def save_ficha_doacao(self, ficha_doacao):
        cursor = self.database.connect.cursor()
        cursor.execute(SQL_INSERT, ficha_doacao.get_values_save())
        id = cursor.fetchone()[0]
        self.database.connect.commit()
        cursor.close()
        ficha_doacao.set_id(id)
        return ficha_doacao

    def edit_ficha_doacao(self, id, ficha_doacao):
        cursor = self.database.connect.cursor()
        str = []
        for key in ficha_doacao.keys():
            str.append('{} = %s'.format(key))
        cursor.execute(SQL_UPDATE.format(','.join(str), id), list(ficha_doacao.values()))
        self.database.connect.commit()
        cursor.close()
        return True

    def get_by_id(self, id):
        ficha_doacao = self.get_all_or_by_id(SQL_BY_ID.format(id))
        if ficha_doacao:
            return ficha_doacao[0]
        return None

    def get_all(self):
        ficha_doacao = self.get_all_or_by_id(SQL_SELECT)
        return ficha_doacao

    def get_all_or_by_id(self, script):
        doacoes = []
        cursor = self.database.connect.cursor()
        cursor.execute(script)
        columns_name = [column[0] for column in cursor.description]
        ficha_doacao_cursor = cursor.fetchone()
        while ficha_doacao_cursor is not None:
            ficha_doacao = dict(zip(columns_name, ficha_doacao_cursor))
            ficha_doacao_cursor = cursor.fetchone()
            coleta = self.dao_coleta.get_by_id(ficha_doacao.get('id'))
            if coleta:
                coleta.pop('ficha_doacao_id')
            ficha_doacao['coleta'] = coleta
            doacoes.append(ficha_doacao)
        cursor.close()
        return doacoes

    def delete_ficha_doacao(self, id):
        cursor = self.database.connect.cursor()
        cursor.execute(SQL_DELETE.format(id))
        self.database.connect.commit()
        return True
