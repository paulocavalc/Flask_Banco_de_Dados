SQL_INSERT = 'INSERT INTO ficha_paciente(nome, cpf, medico, tipo_sanguineo, instituicao_de_saude) ' \
             'VALUES(%s, %s, %s, %s, %s) returning id'
SQL_SELECT = 'SELECT * FROM ficha_paciente'
SQL_BY_ID = 'SELECT * FROM ficha_paciente WHERE id = {}'
SQL_DELETE = 'DELETE FROM ficha_paciente WHERE id = {}'
SQL_UPDATE = 'UPDATE ficha_paciente SET {} WHERE id = {}'


class FichaPacienteDao:
    def __init__(self, database):
        self.database = database

    def save_ficha_paciente(self, ficha_paciente):
        cursor = self.database.connect.cursor()
        cursor.execute(SQL_INSERT, ficha_paciente.get_values_save())
        id = cursor.fetchone()[0]
        self.database.connect.commit()
        cursor.close()
        ficha_paciente.set_id(id)
        return ficha_paciente

    def edit_ficha_paciente(self, id, ficha_paciente):
        cursor = self.database.connect.cursor()
        str = []
        for key in ficha_paciente.keys():
            str.append('{} = %s'.format(key))
        cursor.execute(SQL_UPDATE.format(','.join(str), id), list(ficha_paciente.values()))
        self.database.connect.commit()
        cursor.close()
        return True

    def get_by_id(self, id):
        ficha_paciente = self.get_all_or_by_id(SQL_BY_ID.format(id))
        if ficha_paciente:
            return ficha_paciente[0]
        return None

    def get_all(self):
        ficha_paciente = self.get_all_or_by_id(SQL_SELECT)
        return ficha_paciente

    def get_all_or_by_id(self, script):
        pacientes = []
        cursor = self.database.connect.cursor()
        cursor.execute(script)
        columns_name = [column[0] for column in cursor.description]
        paciente_cursor = cursor.fetchone()
        while paciente_cursor is not None:
            ficha_paciente = dict(zip(columns_name, paciente_cursor))
            paciente_cursor = cursor.fetchone()
            pacientes.append(ficha_paciente)
        cursor.close()
        return pacientes

    def delete_ficha_paciente(self, id):
        cursor = self.database.connect.cursor()
        cursor.execute(SQL_DELETE.format(id))
        self.database.connect.commit()
        return True
