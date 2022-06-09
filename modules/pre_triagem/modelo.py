class PreTriagem:
    VALIDATE_FIELDS_REQUIREMENTS = ['peso', 'altura', 'pulso', 'pressao_arterial', 'hemoglobina']

    def __init__(self, peso, altura, pulso, pressao_arterial, hemoglobina, triagem=None):
        self.id = None
        self.peso = peso
        self.altura = altura
        self.pulso = pulso
        self.pressao_arterial = pressao_arterial
        self.hemoglobina = hemoglobina
        self.triagem = triagem

    def set_id(self, id):
        self.id = id

    def set_triagem(self, triagem):
        self.triagem = triagem

    def __str__(self):
        return f'Peso: {self.peso} - Altura: {self.altura} - Pulso: {self.pulso} - Pressão Arterial: ' \
               f'{self.pressao_arterial} - Hemoglobina: {self.hemoglobina}'

    def get_values_save(self):
        return [self.peso, self.altura, self.pulso, self.pressao_arterial, self.hemoglobina]

    def get_json_formatter(self):
        data = {
            'id': self.id,
            'peso': self.peso,
            'altura': self.altura,
            'pulso': self.pulso,
            'pressao_arterial': self.pressao_arterial,
            'hemoglobina': self.hemoglobina
        }
        if self.triagem:
            data['triagem'] = {
                'entrevista': self.triagem.entrevista
            }
        return data
