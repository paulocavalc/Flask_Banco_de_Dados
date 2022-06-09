from flask import Flask
from controller.controller_ficha_doacao import app_ficha_doacao
from controller.controller_ficha_paciente import app_ficha_paciente
from controller.controller_pre_triagem import app_pre_triagem
from controller.controller_bolsa_sanguinea import app_bolsa_sanguinea

app = Flask(__name__)
app.register_blueprint(app_ficha_doacao)
app.register_blueprint(app_ficha_paciente)
app.register_blueprint(app_pre_triagem)
app.register_blueprint(app_bolsa_sanguinea)

if __name__ == '__main__':
    app.run(debug=True)
