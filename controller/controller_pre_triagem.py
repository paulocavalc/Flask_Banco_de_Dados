from flask import Blueprint, request, jsonify, make_response
from modules.pre_triagem.dao import PreTriagemDao
from modules.pre_triagem.modelo import PreTriagem
from modules.shared.triagem.dao import TriagemDao
from modules.shared.triagem.modelo import Triagem
from utils.database import ConnectSingletonDB
import traceback

app_pre_triagem = Blueprint('app_pre_triagem', __name__)
dao_pre_triagem = PreTriagemDao(database=ConnectSingletonDB())
dao_triagem = TriagemDao(database=ConnectSingletonDB())
app_link = 'pre-triagem'
app_print = 'Pre Triagem'
app_outra_link = 'triagem'
app_outra_print = 'Triagem'


@app_pre_triagem.route('/{}/'.format(app_link), methods=['GET'])
def get_pre_triagem_all():
    pre_triagem = dao_pre_triagem.get_all()
    print('Todos da Lista de Doação de Sangue')
    return make_response(jsonify(pre_triagem), 200)


@app_pre_triagem.route('/{}/<id>/'.format(app_link), methods=['DELETE'])
def delete_pre_triagem_id(id):
    pre_triagem = dao_pre_triagem.get_by_id(id)
    dao_pre_triagem.delete_pre_triagem(id)
    print('{} delete com sucesso!'.format(app_print))
    return make_response(pre_triagem, 201)


@app_pre_triagem.route('/{}/<id>/'.format(app_outra_link), methods=['DELETE'])
def delete_triagem_id(id):
    triagem = dao_triagem.get_by_id(id)
    dao_triagem.delete_triagem(id)
    print('{} delete com sucesso!'.format(app_outra_print))
    return make_response(triagem, 201)


@app_pre_triagem.route('/{}/add/'.format(app_link), methods=['POST'])
def add_pre_triagem():
    try:
        data = request.form.to_dict(flat=True)
        pre_triagem = None
        VALIDATE_TEMP(data)
        pre_triagem = PreTriagem(peso=data.get('peso'), altura=data.get('altura'), pulso=data.get('pulso'),
                                 pressao_arterial=data.get('pressao_arterial'), hemoglobina=data.get('hemoglobina'))
        pre_triagem = dao_pre_triagem.save_pre_triagem(pre_triagem)
        if data.get('entrevista'):
            print('{} adicionado com sucesso!'.format(app_outra_print))
            data.pop('peso')
            data.pop('altura')
            data.pop('pulso')
            data.pop('pressao_arterial')
            data.pop('hemoglobina')
            triagem = Triagem(**data)
            triagem = dao_triagem.save_triagem(triagem, pre_triagem.id)
            pre_triagem.set_triagem(triagem)
    except Exception as e:
        print(traceback.format_exc(), e)
        return make_response(
            {
                'error': True,
                'message': str(e)
            }, 400)
    print('{} adicionado com sucesso!'.format(app_print))
    return make_response({'id': pre_triagem.id}, 201)


@app_pre_triagem.route('/{}/<id>/'.format(app_link), methods=['PUT'])
def edit_pre_triagem(id):
    data = request.form.to_dict(flat=True)
    pre_triagem = dao_pre_triagem.get_by_id(id)
    if not pre_triagem:
        return make_response({'error': 'Erro ao alterar'}, 404)
    dao_pre_triagem.edit_pre_triagem(id, data)
    pre_triagem = dao_pre_triagem.get_by_id(id)
    print('{} atualizado com sucesso!'.format(app_print))
    return make_response(pre_triagem, 200)


@app_pre_triagem.route('/{}/<id>/'.format(app_outra_link), methods=['PUT'])
def edit_triagem(id):
    data = request.form.to_dict(flat=True)
    triagem = dao_triagem.get_by_id(id)
    if not triagem:
        return make_response({'error': 'Erro ao alterar'}, 404)
    dao_triagem.edit_triagem(id, data)
    triagem = dao_triagem.get_by_id(id)
    print('{} atualizado com sucesso!'.format(app_outra_print))
    return make_response(triagem, 200)


@app_pre_triagem.route('/{}/<id>/'.format(app_link), methods=['GET'])
def get_pre_triagem_by_id(id):
    pre_triagem = dao_pre_triagem.get_by_id(id)
    if not pre_triagem:
        return make_response({'error': '{} não existe'.format(app_print)}, 404)
    print('{} já existe!'.format(app_print))
    return make_response(pre_triagem, 201)


def VALIDATE_TEMP(data):
    fields = set(data.keys())
    validate_fields = set(PreTriagem.VALIDATE_FIELDS_REQUIREMENTS).issubset(fields)
    flag_ir_error = False
    for key, value in data.items():
        if value.strip() in ['', None]:
            flag_ir_error = True
    if not validate_fields or flag_ir_error:
        raise Exception('{} é obrigatório'.format(app_print))

    fields = data.keys()
    flag_is_exists_fiels = any(i in Triagem.VALIDATE_FIELDS_REQUIREMENTS for i in fields)
    if flag_is_exists_fiels:
        fields = set(data.keys())
        fields.remove('peso')
        fields.remove('altura')
        fields.remove('pulso')
        fields.remove('pressao_arterial')
        fields.remove('hemoglobina')
        validate_fields = set(Triagem.VALIDATE_FIELDS_REQUIREMENTS).issubset(fields)
        flag_ir_error = False
        for key, value in data.items():
            if value in ['', None]:
                flag_ir_error = True
        if not validate_fields or flag_ir_error:
            raise Exception('{} é obrigatório'.format(app_outra_print))
