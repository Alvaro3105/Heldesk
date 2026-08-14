from flask import Blueprint, jsonify, request

from services.chamado_service import ChamadoService

chamado_bp = Blueprint("chamado_bp", __name__)


@chamado_bp.route("/chamados", methods=["GET"])
def listar_chamados():
    return jsonify(ChamadoService.listar_chamados()), 200


@chamado_bp.route("/chamados", methods=["POST"])
def criar_chamado():
    dados = request.get_json(silent=True) or {}
    try:
        chamado = ChamadoService.criar_chamado(dados)
        return jsonify(chamado.to_dict()), 201
    except ValueError as erro:
        status = 404 if "não encontrado" in str(erro) else 400
        return jsonify({"erro": str(erro)}), status


@chamado_bp.route("/chamados/<int:chamado_id>", methods=["PUT"])
def atualizar_chamado(chamado_id):
    dados = request.get_json(silent=True) or {}
    try:
        chamado = ChamadoService.atualizar_chamado(chamado_id, dados)
        return jsonify(chamado.to_dict()), 200
    except ValueError as erro:
        status = 404 if "não encontrado" in str(erro) else 400
        return jsonify({"erro": str(erro)}), status


@chamado_bp.route("/chamados/<int:chamado_id>", methods=["DELETE"])
def excluir_chamado(chamado_id):
    try:
        ChamadoService.excluir_chamado(chamado_id)
        return "", 204
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 404


@chamado_bp.route("/chamados/<int:chamado_id>/iniciar", methods=["PATCH"])
def iniciar_chamado(chamado_id):
    try:
        chamado = ChamadoService.iniciar_atendimento(chamado_id)
        return jsonify(chamado.to_dict()), 200
    except ValueError as erro:
        status = 404 if "não encontrado" in str(erro) else 400
        return jsonify({"erro": str(erro)}), status


@chamado_bp.route("/chamados/<int:chamado_id>/encerrar", methods=["PATCH"])
def encerrar_chamado(chamado_id):
    try:
        chamado = ChamadoService.encerrar_chamado(chamado_id)
        return jsonify(chamado.to_dict()), 200
    except ValueError as erro:
        status = 404 if "não encontrado" in str(erro) else 400
        return jsonify({"erro": str(erro)}), status


@chamado_bp.route("/chamados/abertos", methods=["GET"])
def listar_chamados_abertos():
    return jsonify(ChamadoService.listar_abertos()), 200


@chamado_bp.route("/chamados/prioridade/alta", methods=["GET"])
def listar_chamados_prioridade_alta():
    return jsonify(ChamadoService.listar_prioridade_alta()), 200


@chamado_bp.route("/estatisticas", methods=["GET"])
def estatisticas():
    return jsonify(ChamadoService.estatisticas()), 200
