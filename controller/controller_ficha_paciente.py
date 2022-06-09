from flask import Blueprint, request, jsonify, make_response
from modules.ficha_paciente.dao import FichaPacienteDao
from modules.ficha_paciente.modelo import FichaPaciente
from utils.database import ConnectSingletonDB
import traceback

app_ficha_paciente = Blueprint('app_ficha_paciente', __name__)
dao_ficha_paciente = FichaPacienteDao(database=ConnectSingletonDB())
app_link = 'ficha-paciente'
app_print = 'Ficha Paciente'


@app_ficha_paciente.route('/{}/'.format(app_link), methods=['GET'])
def get_ficha_paciente_all():
    ficha_paciente = dao_ficha_paciente.get_all()
    print('Todos da Lista de Doação de Sangue')
    return make_response(jsonify(ficha_paciente), 200)


@app_ficha_paciente.route('/{}/<id>/'.format(app_link), methods=['DELETE'])
def delete_ficha_paciente(id):
    ficha_paciente = dao_ficha_paciente.get_by_id(id)
    dao_ficha_paciente.delete_ficha_paciente(id)
    print('{} delete com sucesso!'.format(app_print))
    return make_response(ficha_paciente, 201)


@app_ficha_paciente.route('/{}/add/'.format(app_link), methods=['POST'])
def add_ficha_paciente():
    try:
        data = request.form.to_dict(flat=True)
        ficha_paciente = None
        VALIDATE_TEMP(data)
        ficha_paciente = FichaPaciente(nome=data.get('nome'), cpf=data.get('cpf'), medico=data.get('medico'),
                                 tipo_sanguineo=data.get('tipo_sanguineo'),
                                 instituicao_de_saude=data.get('instituicao_de_saude'))
        ficha_paciente = dao_ficha_paciente.save_ficha_paciente(ficha_paciente)
    except Exception as e:
        print(traceback.format_exc(), e)
        return make_response(
            {
                'error': True,
                'message': str(e)
            }, 400)
    print('{} adicionado com sucesso!'.format(app_print))
    return make_response({'id': ficha_paciente.id}, 201)


@app_ficha_paciente.route('/{}/<id>/'.format(app_link), methods=['PUT'])
def edit_ficha_paciente(id):
    data = request.form.to_dict(flat=True)
    ficha_paciente = dao_ficha_paciente.get_by_id(id)
    if not ficha_paciente:
        return make_response({'error': 'Erro ao alterar'}, 404)
    dao_ficha_paciente.edit_ficha_paciente(id, data)
    ficha_paciente = dao_ficha_paciente.get_by_id(id)
    print('{} atualizado com sucesso!'.format(app_print))
    return make_response(ficha_paciente, 200)


@app_ficha_paciente.route('/{}/<id>/'.format(app_link), methods=['GET'])
def get_ficha_paciente_by_id(id):
    ficha_paciente = dao_ficha_paciente.get_by_id(id)
    if not ficha_paciente:
        return make_response({'error': '{} não existe'.format(app_print)}, 404)
    print('{} já existe!'.format(app_print))
    return make_response(ficha_paciente, 201)


def VALIDATE_TEMP(data):
    fields = set(data.keys())
    validate_fields = set(FichaPaciente.VALIDATE_FIELDS_REQUIREMENTS).issubset(fields)
    flag_ir_error = False
    for key, value in data.items():
        if value.strip() in ['', None]:
            flag_ir_error = True
    if not validate_fields or flag_ir_error:
        raise Exception('{} é obrigatório'.format(app_print))
