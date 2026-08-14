from flask import Blueprint, jsonify, request

from services.usuario_service import UsuarioService

usuario_bp = Blueprint("usuario_bp", __name__)


@usuario_bp.route("/usuarios", methods=["GET"])
def listar_usuarios():
    return jsonify(UsuarioService.listar_usuarios()), 200


@usuario_bp.route("/usuarios", methods=["POST"])
def criar_usuario():
    dados = request.get_json(silent=True) or {}
    try:
        usuario = UsuarioService.criar_usuario(dados)
        return jsonify(usuario.to_dict()), 201
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400


@usuario_bp.route("/usuarios/<int:usuario_id>", methods=["PUT"])
def atualizar_usuario(usuario_id):
    dados = request.get_json(silent=True) or {}
    try:
        usuario = UsuarioService.atualizar_usuario(usuario_id, dados)
        return jsonify(usuario.to_dict()), 200
    except ValueError as erro:
        status = 404 if "não encontrado" in str(erro) else 400
        return jsonify({"erro": str(erro)}), status


@usuario_bp.route("/usuarios/<int:usuario_id>", methods=["DELETE"])
def excluir_usuario(usuario_id):
    try:
        UsuarioService.excluir_usuario(usuario_id)
        return "", 204
    except ValueError as erro:
        status = 404 if "não encontrado" in str(erro) else 400
        return jsonify({"erro": str(erro)}), status


@usuario_bp.route("/usuarios/<int:usuario_id>/chamados", methods=["GET"])
def listar_chamados_do_usuario(usuario_id):
    try:
        chamados = UsuarioService.listar_chamados_do_usuario(usuario_id)
        return jsonify(chamados), 200
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 404
