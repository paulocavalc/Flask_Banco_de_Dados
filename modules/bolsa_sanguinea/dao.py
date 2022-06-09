SQL_INSERT = 'INSERT INTO bolsa_sanguinea(validade, tipo_sanguineo) VALUES(%s, %s) returning id'
SQL_SELECT = 'SELECT * FROM bolsa_sanguinea'
SQL_BY_ID = 'SELECT * FROM bolsa_sanguinea WHERE id = {}'
SQL_DELETE = 'DELETE FROM bolsa_sanguinea WHERE id = {}'
SQL_UPDATE = 'UPDATE bolsa_sanguinea SET {} WHERE id = {}'


class BolsaSanguineaDao:
    def __init__(self, database):
        self.database = database

    def save_bolsa_sanguinea(self, bolsa_sanguinea):
        cursor = self.database.connect.cursor()
        cursor.execute(SQL_INSERT, bolsa_sanguinea.get_values_save())
        id = cursor.fetchone()[0]
        self.database.connect.commit()
        cursor.close()
        bolsa_sanguinea.set_id(id)
        return bolsa_sanguinea

    def edit_bolsa_sanguinea(self, id, bolsa_sanguinea):
        cursor = self.database.connect.cursor()
        str = []
        for key in bolsa_sanguinea.keys():
            str.append('{} = %s'.format(key))
        cursor.execute(SQL_UPDATE.format(','.join(str), id), list(bolsa_sanguinea.values()))
        self.database.connect.commit()
        cursor.close()
        return True

    def get_by_id(self, id):
        bolsa_sanguinea = self.get_all_or_by_id(SQL_BY_ID.format(id))
        if bolsa_sanguinea:
            return bolsa_sanguinea[0]
        return None

    def get_all(self):
        bolsa_sanguinea = self.get_all_or_by_id(SQL_SELECT)
        return bolsa_sanguinea

    def get_all_or_by_id(self, script):
        bolsas = []
        cursor = self.database.connect.cursor()
        cursor.execute(script)
        columns_name = [column[0] for column in cursor.description]
        bolsa_cursor = cursor.fetchone()
        while bolsa_cursor is not None:
            bolsa_sanguinea = dict(zip(columns_name, bolsa_cursor))
            bolsa_cursor = cursor.fetchone()
            bolsas.append(bolsa_sanguinea)
        cursor.close()
        return bolsas

    def delete_bolsa_sanguinea(self, id):
        cursor = self.database.connect.cursor()
        cursor.execute(SQL_DELETE.format(id))
        self.database.connect.commit()
        return True
