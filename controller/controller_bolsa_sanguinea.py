from flask import Blueprint, request, jsonify, make_response
from modules.bolsa_sanguinea.dao import BolsaSanguineaDao
from modules.bolsa_sanguinea.modelo import BolsaSanguinea
from utils.database import ConnectSingletonDB
import traceback

app_bolsa_sanguinea = Blueprint('app_bolsa_sanguinea', __name__)
dao_bolsa_sanguinea = BolsaSanguineaDao(database=ConnectSingletonDB())
app_link = 'bolsa-sanguinea'
app_print = 'Bolsa Sanguinea'


@app_bolsa_sanguinea.route('/{}/'.format(app_link), methods=['GET'])
def get_bolsa_sanguinea_all():
    bolsa_sanguinea = dao_bolsa_sanguinea.get_all()
    print('Todos da Lista de Doação de Sangue')
    return make_response(jsonify(bolsa_sanguinea), 200)


@app_bolsa_sanguinea.route('/{}/<id>/'.format(app_link), methods=['DELETE'])
def delete_bolsa_sanguinea(id):
    bolsa_sanguinea = dao_bolsa_sanguinea.get_by_id(id)
    dao_bolsa_sanguinea.delete_bolsa_sanguinea(id)
    print('{} delete com sucesso!'.format(app_print))
    return make_response(bolsa_sanguinea, 201)


@app_bolsa_sanguinea.route('/{}/add/'.format(app_link), methods=['POST'])
def add_bolsa_sanguinea():
    try:
        data = request.form.to_dict(flat=True)
        bolsa_sanguinea = None
        VALIDATE_TEMP(data)
        bolsa_sanguinea = BolsaSanguinea(validade=data.get('validade'), tipo_sanguineo=data.get('tipo_sanguineo'))
        bolsa_sanguinea = dao_bolsa_sanguinea.save_bolsa_sanguinea(bolsa_sanguinea)
    except Exception as e:
        print(traceback.format_exc(), e)
        return make_response(
            {
                'error': True,
                'message': str(e)
            }, 400)
    print('{} adicionado com sucesso!'.format(app_print))
    return make_response({'id': bolsa_sanguinea.id}, 201)


@app_bolsa_sanguinea.route('/{}/<id>/'.format(app_link), methods=['PUT'])
def edit_bolsa_sanguinea(id):
    data = request.form.to_dict(flat=True)
    bolsa_sanguinea = dao_bolsa_sanguinea.get_by_id(id)
    if not bolsa_sanguinea:
        return make_response({'error': 'Erro ao alterar'}, 404)
    dao_bolsa_sanguinea.edit_bolsa_sanguinea(id, data)
    bolsa_sanguinea = dao_bolsa_sanguinea.get_by_id(id)
    print('{} atualizado com sucesso!'.format(app_print))
    return make_response(bolsa_sanguinea, 200)


@app_bolsa_sanguinea.route('/{}/<id>/'.format(app_link), methods=['GET'])
def get_bolsa_sanguinea_by_id(id):
    bolsa_sanguinea = dao_bolsa_sanguinea.get_by_id(id)
    if not bolsa_sanguinea:
        return make_response({'error': '{} não existe'.format(app_print)}, 404)
    print('{} já existe!'.format(app_print))
    return make_response(bolsa_sanguinea, 201)


def VALIDATE_TEMP(data):
    fields = set(data.keys())
    validate_fields = set(BolsaSanguinea.VALIDATE_FIELDS_REQUIREMENTS).issubset(fields)
    flag_ir_error = False
    for key, value in data.items():
        if value.strip() in ['', None]:
            flag_ir_error = True
    if not validate_fields or flag_ir_error:
        raise Exception('{} é obrigatório'.format(app_print))
