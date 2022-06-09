class BolsaSanguinea:
    VALIDATE_FIELDS_REQUIREMENTS = ['validade', 'tipo_sanguineo']

    def __init__(self, validade, tipo_sanguineo):
        self.id = None
        self.validade = validade
        self.tipo_sanguineo = tipo_sanguineo

    def set_id(self, id):
        self.id = id

    def __str__(self):
        return f'Validade: {self.validade} - Tipo Sanguineo: {self.tipo_sanguineo}'

    def get_values_save(self):
        return [self.validade, self.tipo_sanguineo]

    def get_json_formatter(self):
        data = {
            'id': self.id,
            'validade': self.validade,
            'tipo_sanguineo': self.tipo_sanguineo
        }
        return data
