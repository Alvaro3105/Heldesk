from flask import Flask, jsonify

from controllers.chamado_controller import chamado_bp
from controllers.usuario_controller import usuario_bp
from database import db


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(
        SQLALCHEMY_DATABASE_URI="sqlite:///helpdesk.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    app.register_blueprint(usuario_bp)
    app.register_blueprint(chamado_bp)

    @app.route("/", methods=["GET"])
    def inicio():
        return jsonify(
            {
                "projeto": "Helpdesk API",
                "descricao": "API REST para gerenciamento de usuários e chamados de suporte.",
                "status": "online",
            }
        ), 200

    @app.errorhandler(404)
    def nao_encontrado(erro):
        return jsonify({"erro": "Recurso não encontrado"}), 404

    @app.errorhandler(405)
    def metodo_nao_permitido(erro):
        return jsonify({"erro": "Método não permitido para este endpoint"}), 405

    with app.app_context():
        from models.chamado import Chamado
        from models.usuario import Usuario

        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
