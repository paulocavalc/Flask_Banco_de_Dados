class FichaDoacao:
    VALIDATE_FIELDS_REQUIREMENTS = ['nome', 'idade', 'sexo', 'escolaridade', 'estado_civil',
                                    'data_de_nascimento', 'identidade', 'tipo_sanguineo']

    def __init__(self, nome, idade, sexo, escolaridade, estado_civil, data_de_nascimento, identidade,
                 tipo_sanguineo, coleta=None):
        self.id = None
        self.nome = nome
        self.idade = idade
        self.sexo = sexo
        self.escolaridade = escolaridade
        self.estado_civil = estado_civil
        self.data_de_nascimento = data_de_nascimento
        self.identidade = identidade
        self.tipo_sanguineo = tipo_sanguineo
        self.coleta = coleta

    def set_id(self, id):
        self.id = id

    def set_coleta(self, coleta):
        self.coleta = coleta

    def __str__(self):
        return f'Nome: {self.nome} - Idade: {self.idade} - Sexo: {self.sexo} - Escolaridade: {self.escolaridade} - ' \
               f'Estado Civil: {self.estado_civil} - Data de Nascimento: {self.data_de_nascimento} - ' \
               f'Identidade: {self.identidade} - Tipo Sanguineo: {self.tipo_sanguineo}'

    def get_values_save(self):
        return [self.nome, self.idade, self.sexo, self.escolaridade, self.estado_civil, self.data_de_nascimento,
                self.identidade, self.tipo_sanguineo]

    def get_json_formatter(self):
        data = {
            'id': self.id,
            'nome': self.nome,
            'idade': self.idade,
            'sexo': self.sexo,
            'escolaridade': self.escolaridade,
            'estado_civil': self.estado_civil,
            'data_de_nascimento': self.data_de_nascimento,
            'identidade': self.identidade,
            'tipo_sanguineo': self.tipo_sanguineo
        }
        if self.coleta:
            data['coleta'] = {
                'data': self.coleta.data
            }
        return data
