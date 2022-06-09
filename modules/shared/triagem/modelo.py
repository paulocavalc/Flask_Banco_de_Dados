class Triagem:
    VALIDATE_FIELDS_REQUIREMENTS = ['entrevista']

    def __init__(self, entrevista):
        self.id = None
        self.entrevista = entrevista

    def set_id(self, id):
        self.id = id

    def __str__(self):
        return f'Entrevista: {self.entrevista}'

    def get_values_save(self, pre_triagem_id):
        return [self.entrevista, pre_triagem_id]
