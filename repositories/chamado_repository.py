from database import db
from models.chamado import Chamado


class ChamadoRepository:
    @staticmethod
    def listar():
        return Chamado.query.all()

    @staticmethod
    def buscar_por_id(chamado_id):
        return db.session.get(Chamado, chamado_id)

    @staticmethod
    def listar_por_usuario(usuario_id):
        return Chamado.query.filter_by(usuario_id=usuario_id).all()

    @staticmethod
    def listar_abertos():
        return Chamado.query.filter_by(status="Aberto").all()

    @staticmethod
    def listar_por_prioridade(prioridade):
        return Chamado.query.filter_by(prioridade=prioridade).all()

    @staticmethod
    def contar_nao_encerrados_por_prioridade(usuario_id, prioridade):
        return Chamado.query.filter(
            Chamado.usuario_id == usuario_id,
            Chamado.prioridade == prioridade,
            Chamado.status != "Encerrado",
        ).count()

    @staticmethod
    def criar(chamado: Chamado) -> Chamado:
        db.session.add(chamado)
        db.session.commit()
        return chamado

    @staticmethod
    def salvar_alteracoes():
        db.session.commit()

    @staticmethod
    def excluir(chamado: Chamado):
        db.session.delete(chamado)
        db.session.commit()

    @staticmethod
    def contar_total():
        return Chamado.query.count()

    @staticmethod
    def contar_por_status(status):
        return Chamado.query.filter_by(status=status).count()
