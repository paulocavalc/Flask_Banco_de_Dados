class FichaPaciente:
    VALIDATE_FIELDS_REQUIREMENTS = ['nome', 'cpf', 'medico', 'tipo_sanguineo', 'instituicao_de_saude']

    def __init__(self, nome, cpf, medico, tipo_sanguineo, instituicao_de_saude):
        self.id = None
        self.nome = nome
        self.cpf = cpf
        self.medico = medico
        self.tipo_sanguineo = tipo_sanguineo
        self.instituicao_de_saude = instituicao_de_saude

    def set_id(self, id):
        self.id = id

    def __str__(self):
        return f'Nome: {self.nome} - CPF: {self.cpf} - Medico: {self.medico} - Tipo Sanguineo: {self.tipo_sanguineo} ' \
               f'- Instituição de Saúde: {self.instituicao_de_saude}'

    def get_values_save(self):
        return [self.nome, self.cpf, self.medico, self.tipo_sanguineo, self.instituicao_de_saude]

    def get_json_formatter(self):
        data = {
            'id': self.id,
            'nome': self.nome,
            'cpf': self.cpf,
            'medico': self.medico,
            'tipo_sanguineo': self.tipo_sanguineo,
            'instituicao_de_saude': self.instituicao_de_saude
        }
        return data
