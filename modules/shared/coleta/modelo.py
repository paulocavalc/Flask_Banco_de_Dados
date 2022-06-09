class Coleta:
    VALIDATE_FIELDS_REQUIREMENTS = ['data']

    def __init__(self, data):
        self.id = None
        self.data = data

    def set_id(self, id):
        self.id = id

    def __str__(self):
        return f'Data: {self.data}'

    def get_values_save(self, ficha_doacao_id):
        return [self.data, ficha_doacao_id]
