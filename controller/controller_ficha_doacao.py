from flask import Blueprint, request, jsonify, make_response
from modules.ficha_doacao.dao import FichaDoacaoDao
from modules.ficha_doacao.modelo import FichaDoacao
from modules.shared.coleta.dao import ColetaDao
from modules.shared.coleta.modelo import Coleta
from utils.database import ConnectSingletonDB
import traceback

app_ficha_doacao = Blueprint('app_ficha_doacao', __name__)
dao_ficha_doacao = FichaDoacaoDao(database=ConnectSingletonDB())
dao_coleta = ColetaDao(database=ConnectSingletonDB())
app_link = 'ficha-doacao'
app_print = 'Ficha Doação'
app_outra_link = 'coleta'
app_outra_print = 'Coleta'


@app_ficha_doacao.route('/{}/'.format(app_link), methods=['GET'])
def get_ficha_doacao_all():
    ficha_doacao = dao_ficha_doacao.get_all()
    print('Todos da Lista de Doação de Sangue')
    return make_response(jsonify(ficha_doacao), 200)


@app_ficha_doacao.route('/{}/<id>/'.format(app_link), methods=['DELETE'])
def delete_ficha_doacao_id(id):
    ficha_doacao = dao_ficha_doacao.get_by_id(id)
    dao_ficha_doacao.delete_ficha_doacao(id)
    print('{} delete com sucesso!'.format(app_print))
    return make_response(ficha_doacao, 201)


@app_ficha_doacao.route('/{}/<id>/'.format(app_outra_link), methods=['DELETE'])
def delete_coleta_id(id):
    coleta = dao_coleta.get_by_id(id)
    dao_coleta.delete_coleta(id)
    print('{} delete com sucesso!'.format(app_outra_print))
    return make_response(coleta, 201)


@app_ficha_doacao.route('/{}/add/'.format(app_link), methods=['POST'])
def add_ficha_doacao():
    try:
        data = request.form.to_dict(flat=True)
        ficha_doacao = None
        VALIDATE_TEMP(data)
        ficha_doacao = FichaDoacao(nome=data.get('nome'), idade=data.get('idade'), sexo=data.get('sexo'),
                             escolaridade=data.get('escolaridade'), estado_civil=data.get('estado_civil'),
                             data_de_nascimento=data.get('data_de_nascimento'), identidade=data.get('identidade'),
                             tipo_sanguineo=data.get('tipo_sanguineo'))
        ficha_doacao = dao_ficha_doacao.save_ficha_doacao(ficha_doacao)
        if data.get('data'):
            print('{} adicionado com sucesso!'.format(app_outra_print))
            data.pop('nome')
            data.pop('idade')
            data.pop('sexo')
            data.pop('escolaridade')
            data.pop('estado_civil')
            data.pop('data_de_nascimento')
            data.pop('identidade')
            data.pop('tipo_sanguineo')
            coleta = Coleta(**data)
            coleta = dao_coleta.save_coleta(coleta, ficha_doacao.id)
            ficha_doacao.set_coleta(coleta)
    except Exception as e:
        print(traceback.format_exc(), e)
        return make_response(
            {
                'error': True,
                'message': str(e)
            }, 400)
    print('{} adicionado com sucesso!'.format(app_print))
    return make_response({'id': ficha_doacao.id}, 201)


@app_ficha_doacao.route('/{}/<id>/'.format(app_link), methods=['PUT'])
def edit_ficha_doacao(id):
    data = request.form.to_dict(flat=True)
    ficha_doacao = dao_ficha_doacao.get_by_id(id)
    if not ficha_doacao:
        return make_response({'error': 'Erro ao alterar'}, 404)
    dao_ficha_doacao.edit_ficha_doacao(id, data)
    ficha_doacao = dao_ficha_doacao.get_by_id(id)
    print('{} atualizado com sucesso!'.format(app_print))
    return make_response(ficha_doacao, 200)


@app_ficha_doacao.route('/{}/<id>/'.format(app_outra_link), methods=['PUT'])
def edit_coleta(id):
    data = request.form.to_dict(flat=True)
    coleta = dao_coleta.get_by_id(id)
    if not coleta:
        return make_response({'error': 'Erro ao alterar'}, 404)
    dao_coleta.edit_coleta(id, data)
    coleta = dao_coleta.get_by_id(id)
    print('{} atualizado com sucesso!'.format(app_outra_print))
    return make_response(coleta, 200)


@app_ficha_doacao.route('/{}/<id>/'.format(app_link), methods=['GET'])
def get_ficha_doacao_by_id(id):
    ficha_doacao = dao_ficha_doacao.get_by_id(id)
    if not ficha_doacao:
        return make_response({'error': '{} não existe'.format(app_print)}, 404)
    print('{} já existe!'.format(app_print))
    return make_response(ficha_doacao, 201)


def VALIDATE_TEMP(data):
    fields = set(data.keys())
    validate_fields = set(FichaDoacao.VALIDATE_FIELDS_REQUIREMENTS).issubset(fields)
    flag_ir_error = False
    for key, value in data.items():
        if value.strip() in ['', None]:
            flag_ir_error = True
    if not validate_fields or flag_ir_error:
        raise Exception('{} é obrigatório'.format(app_print))

    fields = data.keys()
    flag_is_exists_fiels = any(i in Coleta.VALIDATE_FIELDS_REQUIREMENTS for i in fields)
    if flag_is_exists_fiels:
        fields = set(data.keys())
        fields.remove('nome')
        fields.remove('idade')
        fields.remove('sexo')
        fields.remove('escolaridade')
        fields.remove('estado_civil')
        fields.remove('data_de_nascimento')
        fields.remove('identidade')
        fields.remove('tipo_sanguineo')
        validate_fields = set(Coleta.VALIDATE_FIELDS_REQUIREMENTS).issubset(fields)
        flag_ir_error = False
        for key, value in data.items():
            if value in ['', None]:
                flag_ir_error = True
        if not validate_fields or flag_ir_error:
            raise Exception('{} é obrigatório'.format(app_outra_print))
